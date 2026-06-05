# 4D-Earth-Dynamic-Admittance
This project generates large‑scale numerical Earth models on (surface and CMB) dynamic topography, geoid and gravity anomalies using ASPECT and then calculates dynamic admittance (gravity anomaly/dynamic topography). In addition, sensitivity tests across different mantle viscsoity structures are performed to evaluate the dependencies of those fields with varying mantle structure. These high-volume datasets are then processed to analyze and reveal geospatial patterns.

A. FILES TO PREPARE BEFORE RUNNING ASPECT

(A.1) parameter file

Here 2 parameter files are used: for 1-layered viscosity (.prm) and 2-layered viscosity (2L.prm) profiles. See sample parameter files.
	  
(A.2) geoid_selfg.cc plug-in, which is a modified plug-in (geoid.cc) from ASPECT 2.4.0

B. FOR POST-PROCESSING (i.e., data treatment, plotting)

ReadData.py = This code treats all the high-volume datasets (getting max, min, average), and summarizes all the amplitudes for each depth in one file. Remember to always CHANGE the 'dataset' line.
