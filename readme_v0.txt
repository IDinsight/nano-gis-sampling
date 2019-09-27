**Authors:** Nate Vernon and Valentina Brailovskaya

**Documentation:** Please reference the IDinsight blog post here: ADD LINK ONCE BLOG POST IS UPLOADED

**This repository provides the Python portion of code to implement Nano's geographical segmentation strategy.** There are 5 key steps in this notebook:<br>
1) Put all the shapefiles on the map, <br>
2) Divide the total area into smaller cells (we call them enumeration areas - EAs), <br>
3) Determine areas with high probability of household presence, <br>
4) Identify EAs with non-zero probability of household presence, <br>
5) Create shapefiles for all objects used in plots.

**This analysis requires the following shapefiles:**<br>
1) Boundary of study area (Mukobela Chiefdom in our case), <br>
2) Population estimates (Facebook and roofs dataset in our case), <br>
3) Any other relevant boundaries to separate EAs (roads and rivers in our case).

**Folder structure**<br>
1) geographic_segmentation.py: the main python script, which runs the entire analysis,<br>
2) geographic_segmentation.ipynb: the main python script as a Jupyter Notebook,<br>
3) functions/clean_data.py: user built functions to clean data,<br>
4) functions/mapping.py: user built functions to create maps,<br>
5) shapefiles: folder to contain all Shapefiles used in analysis,<br>
6) plots: folder to save all plots created in analysis,<br>
7) data: folder to contain the output from analysis (see below).

**The key output** is a CSV with all EAs coordinates and population estimates. It is saved at this file path: *data/EA_information.csv.*

**Other notes:**<br>
1) The code relies on many user built functions stored in the functions folder,<br>
2) The boundary of the study area should be in a coordinate system using meters (e.g. EPSG: 32735 for southern Africa). The other shapefiles and data should be in the standard longitude and latitude coordinate system (EPSG: 4326),<br>
3) Facebook's geospatial population estimates are available here: https://data.humdata.org/dataset/highresolutionpopulationdensitymaps,<br>
4) Rooftop GPS coordinates are available here: https://data.humdata.org/search?q=OpenStreetMap+buildings&ext_search_source=main-nav,<br>
5) Road and waterway data are available here: https://data.humdata.org/search?q=openstreetmaps+roads&ext_search_source=main-nav and https://data.humdata.org/search?q=openstreetmaps+waterways&ext_search_source=main-nav.
