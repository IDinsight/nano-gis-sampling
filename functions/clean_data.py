import pandas as pd
import numpy as np
from shapely.geometry import shape, MultiLineString
from shapely.ops import polygonize
import shapefile


def create_shape_df_shp(shapefiles):
    '''
    purpose
    # create dataframe from the shape files
    
    inputs
    # shapefiles: shapefiles in a pandas column
    
    outputs
    # df_shapes: dataframe with three columns (name of area, shape of area, points on boundary of area)
    '''
    
    field_names = [i[0] for i in shapefiles.fields] 
    field_data = [i[0:] for i in shapefiles.records()]
    
    df_shapes = pd.DataFrame(field_data, columns = field_names[1:])
    df_shapes['shape'] = [shape(x) for x in shapefiles.shapes()]
    
    return(df_shapes) # return the dataframe
    

def create_grids(shape, meters):
    '''
    purpose
    # create grids within a shape
    
    inputs
    # shape: the shape that forms the exterior of grids
    # meters: the width and heigh of each grid
    
    outputs
    pd.DataFrame(grids): a dataframe with all the grids
    '''
    
    x_grids = np.arange(shape.bounds[0] - meters, shape.bounds[2] + meters, meters)
    y_grids = np.arange(shape.bounds[1] - meters, shape.bounds[3] + meters, meters)

    x_lines = [((x1, yi), (x2, yi)) for x1, x2 in zip(x_grids[:-1], x_grids[1:]) for yi in y_grids]
    y_lines = [((xi, y1), (xi, y2)) for y1, y2 in zip(y_grids[:-1], y_grids[1:]) for xi in x_grids]
    
    grids = list(polygonize(MultiLineString(x_lines + y_lines)))

    return(pd.DataFrame.from_dict({'shape': grids}))
    
def split_grids_polygon(grids, boundaries):
    '''
    purpose
    # allocate grids to specific boundaries and only keep portion within a boundary
    
    inputs
    # grids: a column of grids from a dataframe
    # boundaries: a column of boundaries from a dataframe
    
    outputs
    # pd.DataFrame(grid_list): a dataframe containing the new list of grids
    '''
    grid_list = []
    
    for index, grid in grids.iteritems():    
        for bd_index, bd_shape in boundaries.iteritems():
            
            # if the grid intersects the EA then split into 2 and add both to the list
            if grid.intersects(bd_shape) == True:                
                grid_inside = grid.intersection(bd_shape) # inside grid
                
                if grid_inside.geom_type == 'Polygon':
                    grid_list.append({'index': index,
                                      'shape': grid_inside,
                                      'bd_index': bd_index})
                
                if grid_inside.geom_type == 'MultiPolygon':
                    for ele in [x for x in list(grid_inside)]:
                        grid_list.append({'index': index,
                                          'shape': ele,
                                          'bd_index': bd_index})
    
    return(pd.DataFrame(grid_list))

def split_grids_line(grids, shape_name, index_name, boundaries):
    '''
    purpose
    # split grids that intersect any line
    
    inputs
    # grids: a dataframe that contains grids/EAs
    # shape_name: the column name for the grids/EAs within the dataframe
    # index_name: the column name for the primary index of the grids/EAs within the dataframe
    # boundaries: a series with all lines that you want to use to split the grids/EAs
    
    outputs
    pd.DataFrame(grid_list): a dataframe with the split grids and indexes
    '''
    
    grid_list = []
    
    for index, grid in grids.iterrows():    
        for bd_index, bd_shape in boundaries.iteritems():
            grid_outside = grid[shape_name].difference(bd_shape.buffer(1e-6))
            
            if (grid[shape_name].intersects(bd_shape) == True) & (grid_outside.geom_type == 'MultiPolygon'):
                for ele in [x for x in list(grid_outside)]:
                        grid_list.append({'index': grid['index'],
                                          'shape': ele,
                                          'bd_index': grid[index_name]}) 
    
    return(pd.DataFrame(grid_list))
    

def split_multiline(df, shape_name):
    '''
    purpose
    # create individual lines from any multilines in a dataframe
    
    inputs
    # df: the dataframe that may contain multilines
    # shape_name: the column name for the shapes (which may contain multilines)
    
    outputs
    line_df_final: a dataframe with all shapes (including split multilines and shapes that were not originally multilines)
    '''
    
    line_list = []
    
    for index, row in df.iterrows():
        if row[shape_name].geom_type == 'MultiLineString':
            for ele in [x for x in list(row[shape_name])]:
                        line_list.append({'index': index,
                                          'shape': ele})
        else:
            line_list.append({'index': index,
                              'shape': row[shape_name]})
    
    line_df = pd.DataFrame.from_dict(line_list)
    line_df_final = line_df.merge(df.drop(shape_name, axis = 1), 
                                  right_index = True, left_on = 'index')
    
    return(line_df_final)
    
def count_within_grid(grid_shapes, check_shapes, 
                      append_names, limit_check = 100, 
                      check_shape = True, check_others = pd.DataFrame()):
    '''
    purpose
    # create dataframe that counts how many Points or Shapes are within within a column of Shapes
    
    inputs
    # grid_shapes: a series of grids, formatted as Polygons
    # df_check: a series of Polygons or Points, the function checks whether these fall within the grid_shapes
    # append_names: suffix for all dataframe column names
    # check_shape: whether the check object is a Polygon (if false then assumed ot be a Point) 
    
    outputs
    # intersect_df: a dataframe listing whether any check_shapes falls within each grid
    '''
    
    ## list to store all results
    intersect_list = []
    others_list = []
    
    ## loop through shapes of grid
    for index_grid, grid in grid_shapes.iteritems():
                
        ## reset object so that loop works properly
        intersect = False
        
        ## representative points from grid
        x_grid = grid.representative_point().x
        y_grid = grid.representative_point().y
        
        ## sort based on on the current loop
        ### distance from representative - separate for Polygon vs. Point
        x_check_dist = check_shapes.apply(lambda x: abs(x.representative_point().x - x_grid))
        y_check_dist = check_shapes.apply(lambda x: abs(x.representative_point().y - y_grid))
                
        ### sort the dataframe
        xy_check_dist = x_check_dist + y_check_dist
        xy_check_sorted = xy_check_dist.sort_values().index
        
        check_shapes_sorted = check_shapes.reindex(xy_check_sorted)
        
        ## counters
        loop_outside_count = 0
        loop_inside_count = 0
        loop_others = []
        
        ## loop through all shapes/points of check
        for index_check, check in check_shapes_sorted.iteritems():
            
            ## if a shape then
            if check_shape == True:
                intersect = grid.intersects(check)
            
            ## if a point then
            if check_shape == False:
                intersect = check.within(grid)
            
            ## add to inside or outside counters
            loop_inside_count += np.where(intersect == True, 1, 0)
                            
            ### if no intercept then add to loop counter
            loop_outside_count += np.where(intersect == True, 0, 1)
                
            ### add count information to the list
            if (intersect == True) & (check_others.shape[0] != 0):
                loop_others.append(list(check_others.loc[index_check]))
            
            ### end loop and add to dictionary
            if (index_check == xy_check_sorted[-1]) or (loop_outside_count == limit_check):  
                
                ### add up all elements of each list
                if (len(loop_others) == 0) & (check_others.shape[0] != 0):
                    loop_others = [0] * check_others.shape[1]
                    
                elif check_others.shape[0] != 0:
                    loop_others = list(map(sum, zip(*loop_others)))
                
                ### add list to the bigger count list
                if check_others.shape[0] != 0:
                    others_list.append({'index': index_grid,
                        'values': loop_others})
                
                intersect_list.append({'index': index_grid,
                    'intersect_count': loop_inside_count, 
                    'intersect_no_count': loop_outside_count,
                    'intersect': np.where(loop_inside_count > 0, True, False)})
                
                break
    
    ## generate dataframe
    intersect_df = pd.DataFrame.from_dict(intersect_list)
    index_to_append = intersect_df['index']
    
    if check_others.shape[0] != 0:
        count_df = pd.DataFrame.from_dict(others_list)
    else:
        count_df = pd.DataFrame.from_dict({'index': index_to_append})
        
    ## create consistent index
    intersect_df.set_index('index', inplace = True)
    count_df.set_index('index', inplace = True)
    
    ## expand to multiple columns
    if check_others.shape[0] != 0:
        count_df_final = pd.DataFrame(count_df['values'].values.tolist(), index = count_df.index)
        count_df_final.columns = list(check_others.loc[index_check].index)
    else:
        count_df_final = count_df.copy()
    
    ## concat
    if check_others.shape[0] != 0:
        intersect_df.reset_index(drop=True, inplace=True)
        count_df_final.reset_index(drop=True, inplace=True)
    
        intersect_df_final = pd.concat([intersect_df, count_df_final], axis = 1)
    else:
        intersect_df_final = intersect_df.copy()
    
    ## append the column names
    intersect_df_final = intersect_df_final.add_suffix(append_names)
    intersect_df_final['index'] = index_to_append
        
    return(intersect_df_final)
    

def export_shapefile(df, shape_name, field_names, file_name):
    '''
    purpose
    # export a shapefile using a dataframe what holds shapes
    
    inputs
    # df: dataframe with shapes
    # shape_name: name of column that holds the shapes
    # field_names: list of column names and type of field (string, integer, etc.)
    # file_name
    
    outputs
    # a shapefile
    '''
    
    # save shapefiles
    w = shapefile.Writer(file_name)
    
    # shapefile fields
    for x in field_names:
        w.field(x[0], x[1])
    
    # loop through all grids and save
    for index, row in df.iterrows():
        rec = row[[x[0] for x in field_names]]
        
        w.record(*rec.values)
        w.shape(row[shape_name])
    
    w.balance()
    w.close()