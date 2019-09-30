# Nano Sampling with Geographic Segmentation

## Introduction

Gathering accurate information in rural areas is often costly and difficult, which means local leaders may lack important knowledge on their constituents’ needs required to inform evidence-based decisions. Given IDinsight’s focus on data-driven decisions in the social sector, we see this as an important information gap.

Further, we identified the need to collect household-level data from a representative sample of households. However, there was a lack of reliable and up-to-date list of households (or villages) that we could use as a sampling frame (and from which to draw a sample). An additional challenge is Nano’s mandate to be scalable and provide information at low cost, so censusing the whole chiefdom to create a sampling frame was not an option. Therefore, we strove to create a sampling methodology that was economical, scalable and easy for surveyors to implement.

This notebook contains code to implement the geographic segmentation portion of Nano's sampling strategy. A more detailed description is contained in the corresponding blog post (LINK).

## Geographic Segmentation Steps

The geographic segmentation is implemented in Python as follows:
1) Plot all relevant boundaries and population/structure datasets to visualize the study area, boundaries (e.g. rivers and roads) and population (e.g. Facebook and OpenStreetMap datasets) information and ensure that the data makes sense.
2) Divide the study area into smaller cells (we call them enumeration areas - EAs). We use 500 by 500 meter squares as EAs, but other shapes are possible, such as village cluster boundaries.
3) Determine areas with high probability of household presence, using the Facebook population and OpenStreetMap buildings datasets.
4) Identify EAs with non-zero probability of household presence. We assume these are EAs that have a non-zero population from Facebook and/or buildings from OpenStreetMaps. Other rules could be used.


## Getting Started

The code requires a number of python packages, file structure and input/output information. These are described below.

**Packages:** os, pandas, numpy, matplotlib, shapely, shapefile, functools, pyproj.

**File structure:**
1) *geographical_segmentation.ipynb*: the main python script as a Jupyter Notebook,
2) *geographical_segmentation.py*: the main python script (idential to geographical_segmentation.ipynb),
3) *functions/clean_data.py*: user built functions to clean data,
4) *functions/mapping.py*: user built functions to create maps,
5) *shapefiles*: folder to contain all Shapefiles used in analysis,
6) *plots*: folder to save all plots created in analysis,
7) *data*: folder to contain the primary output from analysis (see 1 of the Outputs section below).

**Inputs (all saved as shapefiles in shapefiles folder):**
1) *Boundary of study area* (Mukobela Chiefdom in our case). This should be in a coordinate reference system (CRS) using meters so that the EAs can be constructed using a width and length specified in meters. The CRS system for meters in southern africa is EPSG: 32735, and one can change a shapefiles CRS in QGIS, 
2) *Population estimates* (Facebook and roofs dataset in our case). This should be in the CRS using latitude and longitude, which is EPSG: 4326, 
3) *Any other relevant boundaries to separate EAs* (roads and rivers in our case). This should be in the CRS using latitude and longitude, which is EPSG: 4326.

**Outputs:**
1) *data/EA_information.csv*: a CSV with all EAs coordinates and population estimates. This file allows us to construct our sampling frame.
2) *shapefiles*: there are 4 new shapefiles saved to the shapefiles folder. There are described below:<br>
 2a) *study_area_4326.shp*: the study area converted into the latitude and longitude coordinate reference system.<br>
 2b) *grids_final_4326.shp*: the EAs with an unique identify and whether the EA contains a non-zero Facebook population estimate and/or OpenStreetMap buildings.<br>
 2c) *roads_final_4326.shp*: the roads used as a boundary to construct the EAs. This only includes "large" roads.<br>
 2d) *rivers_final_4326.shp*: the rivers used as a boundary to construct the EAs. This only includes "large" rivers.

### Installing Prerequisites

To install all prequisites, you first need to download python and Jupyter Notebook. An easy way to do so is to download these through [Anaconda](https://www.anaconda.com/distribution/).

Then, each package used in the analysis can be downloaded by entering the command below in the python terminal.

```
pip install package_name
```

### Assembling Input Files

The input files with pre-processing instructed are listed below. All of these files should be saved in the shapefiles folder. 
1) *study_area_32735.shp*: boundary of study area. We created this by drawing the boundary on QGIS. If the study area is an administrative region (e.g. country, state, district) then there are possibly publicly available shapefiles. A good place to look for such files is the [HumData website](https://data.humdata.org/).<br>
 1a) This should be in a CRS using meters, which is EPSG: 32735 for southern africa. One can change a shapefiles CRS in QGIS3 by importing the shapefile into QGIS3 and then right-click the imported shapefile, select export, select save features as, and change the CRS in the drop-down.<br>
 1b) A description of CRS is [here](https://docs.qgis.org/testing/en/docs/gentle_gis_introduction/coordinate_reference_systems.html).<br>
 1c) Line 90 of geographical_segmentation.py contains the original CRS. The CRS for the study area shapefile should be reflected in this line of code.<br>
2) *roofs_4326.shp* and *fb_roofs_4326.shp*: shapefiles with [OpenStreetMaps buildings](https://data.humdata.org/search?q=OpenStreetMap+buildings&ext_search_source=main-nav) and [Facebook’s population](https://data.humdata.org/dataset/highresolutionpopulationdensitymaps) datasets.<br>
 2a) Save the datasets in shapefiles using the longitude and latitude CRS (EPSG: 4326).<br>
3) *roads_4326.shp* and *rivers_4326.shp*: shapefiles with [roads](https://data.humdata.org/search?q=openstreetmaps+roads&ext_search_source=main-nav) and [rivers](https://data.humdata.org/search?q=openstreetmaps+waterways&ext_search_source=main-nav) boundaries in your study area.<br>
 3a) Save the datasets in shapefiles using the longitude and latitude CRS (EPSG: 4326).<br>

## Running the code

The code can be ran from the python terminal or Jupyter Notebook. 

To run the code from the ptyhon terminal, open the python terminal, navigate to the local directory with the GitHub repo, and enter the code below:

```
cd enter_local_directory
python geographic_segmentation.py
```

To run the Jupyter Notebook, open Jupyter Notebook, navigate to the local directory with the GitHub repo, and open the Notebook. Then, select Cells and Run All.

## Authors

* [**Nate Vernon**](https://www.idinsight.org/full-team-1/nate-vernon)
* [**Valentina Brailovskaya**](https://www.idinsight.org/full-team-1/valentina-brailovskaya)


## License

This project is licensed under the GPLv3 license - see the [LICENSE.md](LICENSE.md) file for details.