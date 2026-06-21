# Reproducibility Standard

This repository is organized to satisfy a high-standard journal review of data and code availability.

## What Must Be Public

- Source code for every result table and figure.
- The harmonized spatial-unit table used in the models.
- Data dictionary and preprocessing notes.
- Public source URLs or dataset identifiers for Landsat, WorldCover, DEM, VIIRS, OSM, and boundary layers.
- Random seeds and package versions.
- A single command that regenerates all reproducible outputs.

## What May Be Restricted

Some local planning or socioeconomic layers may be restricted by licensing, privacy, or government-data access conditions. If those layers are used, the repository should provide:

- a clear restricted-data note,
- variable-level metadata,
- the aggregation method,
- a checksum for the derived spatial-unit table,
- and a public proxy-only fallback workflow.

## Review-Safe Statement

Do not write that all raw data are public if local planning, industrial-land, GDP, or high-resolution morphology layers are not publicly redistributable. A safer wording is:

> All public remote-sensing datasets and source code are provided. The harmonized spatial-unit dataset required to reproduce the figures and tables is released in the repository. Restricted local planning/statistical layers, if any, are documented with source metadata and reproduced through aggregated variables to comply with data-use restrictions.
