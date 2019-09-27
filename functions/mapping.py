
import matplotlib.pyplot as plt
import numpy as np

def plot_set_up(plot_title, x_label = '', y_label = '', 
                plot_height = 7, plot_width = 7, plot_aspect = 'equal'):
    '''
    purpose
    # make a figure and axis object with titles
    
    inputs
    # plot_title: the title of the plot
    # x_label: the x-axis label for the plot
    # y_label: the y-axis label for the plot
    # plot_height: the height of the plot in inches
    # plot_width: the width of the plot in inches
    # plot_aspect: the aspect ratio of the plot
    
    outputs
    # fig: the figure object for the plot
    # ax: the axis object for the plot
    '''
    
    # create the plot object
    fig, ax = plt.subplots(figsize = (plot_height, plot_width)) 
    
    # title and set size of the plot objext
    ax.set_title(plot_title)    # plot title
    ax.set_aspect(plot_aspect)  # aspect ratio
    ax.set_xlabel(x_label)      # x axis label
    ax.set_ylabel(y_label)      # y axis label
    
    # return the plot object
    return(fig, ax)
 
def plot_final(ax_object, fig_object, save_file, file_name, 
               dpi_level = None, columns = 1):
    '''
    purpose
    # set up the legend and ticks for the plot and save if selected
    
    inputs
    # ax_object: the axis object for the plot
    # fig_object: the figure object for the plot
    # save_file: true / false for whether you want to save the file
    # file_name: the file name if the file is saved
    
    outputs - none    
    '''
    
    ax_object.legend(bbox_to_anchor = (1, 0.75), ncol = columns) # include the legend in the plot
    ax_object.ticklabel_format(useOffset = False, style = 'plain') # fix tick format
    fig_object.tight_layout()  # tight figure layout
    
    if save_file == True:
        plt.savefig(file_name, bbox_inches='tight', dpi = dpi_level)        
    
def shape_plot(axis, shape_object, alpha = 1, color = 'red', 
               include_label = False, label_name = None, line = False):
    '''
    purpose
    # plot a shape
    
    inputs
    # axis: the axis object for the plot
    # shape_object: a shape in shapely Polygon format
    # color: the color of the shape plot
    # include_label: whether to include the label of the shape in the legend
    # label_name: the label of the shape --- for example, the name of the village cluster
    
    outputs - none, the plot is shown    
    '''

    # extract the x and y coordindates for ths shape
    if line == False:
        x, y = shape_object.exterior.xy        
    else:
        x, y = shape_object.xy
    
    # plot the shape
    if include_label == True:
        axis.plot(x, y, color = color, label = label_name, alpha = alpha)
    else:
        axis.plot(x, y, color = color, alpha = alpha)

def shape_plot_df(axis, shapes, include_label, label_name, alpha = 1, color = 'red', line = False):
    '''
    purpose
    # loop through all shapes in a dataframe and plot them
    
    inputs
    # axis: the axis object for the plot
    # shapes: the column of shapes that will be plotted
    # include_label: whether to include the label of the shape in the legend
    # label_name: the label of the shape --- for example, the name of the village cluster
    # alpha: alpha of the shape plot 
    # color: the color of the shape plot 
    # line: boolean for whether the shape is a line (or Polygon), True if line
    
    outputs
    # a plot with all of the shapes
    
    '''
    
    
    for index, row in shapes.iteritems():
        label = np.where(index == shapes.index[-1], label_name, '') 
        include = np.where((index == shapes.index[-1]) & (include_label), True, False)
        
        shape_plot(axis = axis, shape_object = row, 
                   color = color, alpha = alpha, 
                   label_name = label, include_label = include, line = line)

def loop_many_shapes(grouped_df, colors = 30, shape_column = None, shape_name_column = None):
    
    '''
    purpose
    # iterate through rows of a column and assign colors to each unique value in the column
    
    inputs
    # grouped_df: a groupby dataframe, grouped by the column that you want each unique value to be a different color 
    # shape_column: the name of the column that cntains shapes
    # shape_name_column: the name of the shape --- for example, the enumeration area name
    # X_column: the x column of the scatter 
    # Y_column: the y column of the scatter
    
    outputs
    # graph_input_list: a list of inputs that will be used to graph the shapes    
    '''

    graph_input_list = [] # list to create dataframe with all graph inputs
    
    ## colors for the plot
    colors = iter(plt.get_cmap('rainbow')(np.linspace(0, 1, colors)))
    
    ### loop through all groups of label
    for label, df in grouped_df:
        color = next(colors) # return the next color in the list        
        loop_count = 0 ## loop counter
        
        ### loop through all rows
        for index, row in df.iterrows():
    
            ### only include label if it is the first enumeration area in the DF
            label_flag = True if loop_count == 0 else False
            loop_count += 1
            
            # add to list
            graph_input_list.append({'area': np.nan if shape_name_column == None else row[shape_name_column],
                                     'shape': np.nan if shape_column == None else row[shape_column],
                                     'label': label,
                                     'include_label': label_flag,
                                     'color': color})
    
    return(graph_input_list)