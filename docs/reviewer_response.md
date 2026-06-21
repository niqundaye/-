# Suggested Response to Reviewer Comment 4

Comment:

> Regarding Figure 4, is this based on real data? I strongly suggest the authors provide their source code and raw datasets for verification.

Response:

Thank you for this important suggestion. Figure 4 is based on the real spatial-unit dataset constructed for Xi Ujimqin Banner, rather than on simulated or manually drawn curves. Specifically, the PDP and ICE curves in Figure 4 were generated from the fitted LST prediction model using the spatial-unit variables derived from Landsat LST, Landsat surface reflectance/NDVI, land-use composition, SVF-related openness, terrain, road accessibility, and nighttime-light/economic proxy data.

To improve transparency and reproducibility, we have created a public GitHub repository containing the source code, data schema, preprocessing notes, public-data acquisition workflow, and supplementary monitoring data. The repository includes the script `src/figure4_pdp_ice.py`, which retrains the LST prediction model and regenerates Figure 4 from `data/raw/spatial_units_xi_ujimqin_2023.csv`. The repository also includes scripts for model-performance comparison, feature-importance calculation, spatial optimization-potential classification, multi-objective allocation scenario evaluation, objective trade-off analysis, and water-quality monitoring summary.

In addition, we provide a Google Earth Engine script and data-source documentation for reconstructing the public remote-sensing layers, including Landsat 8/9 Collection 2 Level-2 data, ESA WorldCover, DEM, VIIRS nighttime light, and related spatial predictors. The original water-quality monitoring appendix has also been converted into a long-format CSV table and included as supplementary environmental-monitoring evidence.

Revision made:

We added a data-and-code availability statement to the revised manuscript and clarified in the Figure 4 caption/method section that the PDP/ICE curves were calculated from the fitted model using real spatial-unit observations.

Repository:

`https://github.com/niqundaye/-`
