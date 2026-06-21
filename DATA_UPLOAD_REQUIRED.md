# Data Files Still To Upload

The repository source code, data dictionary, public-data acquisition workflow, and reproduction documentation have been uploaded.

Two generated local data files should still be uploaded through GitHub web upload, Git LFS, or a local `git`/`gh` workflow:

```text
data/raw/water_quality_monitoring_long.csv
data/example/spatial_units_demo.csv
```

The complete local package is available as:

```text
paper_reproducibility_package_github_ready.zip
```

Important notes for reviewers:

- `water_quality_monitoring_long.csv` is the extracted real water-quality monitoring table from the supplied monitoring appendix DOCX. It contains 7560 records.
- `spatial_units_demo.csv` is only a smoke-test dataset. It is not the manuscript spatial-unit dataset.
- Full manuscript reproduction requires the real spatial-unit dataset at `data/raw/spatial_units_xi_ujimqin_2023.csv`.

The code can regenerate the water-quality CSV from the original DOCX using:

```bash
python src/extract_water_quality_docx.py --input path/to/monitoring_appendix.docx
```

The public remote-sensing part can be reconstructed using:

```text
data_acquisition/gee_export_spatial_layers.js
```
