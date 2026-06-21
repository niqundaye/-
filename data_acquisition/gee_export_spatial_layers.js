// Google Earth Engine export script for Xi Ujimqin Banner spatial-unit variables.
//
// Before running:
// 1. Upload the study boundary as an Earth Engine asset and replace BOUNDARY_ASSET.
// 2. Upload spatial units as an Earth Engine asset and replace UNITS_ASSET.
// 3. Inspect scenes and cloud coverage before final export.

var BOUNDARY_ASSET = 'users/YOUR_GEE_USERNAME/xi_ujimqin_boundary';
var UNITS_ASSET = 'users/YOUR_GEE_USERNAME/xi_ujimqin_spatial_units';

var boundary = ee.FeatureCollection(BOUNDARY_ASSET);
var units = ee.FeatureCollection(UNITS_ASSET);
var start = '2023-06-01';
var end = '2023-09-30';

function maskLandsatL2(image) {
  var qa = image.select('QA_PIXEL');
  var fill = qa.bitwiseAnd(1 << 0).eq(0);
  var dilatedCloud = qa.bitwiseAnd(1 << 1).eq(0);
  var cirrus = qa.bitwiseAnd(1 << 2).eq(0);
  var cloud = qa.bitwiseAnd(1 << 3).eq(0);
  var cloudShadow = qa.bitwiseAnd(1 << 4).eq(0);
  var snow = qa.bitwiseAnd(1 << 5).eq(0);
  var water = qa.bitwiseAnd(1 << 7).eq(0);
  return image.updateMask(fill)
    .updateMask(dilatedCloud)
    .updateMask(cirrus)
    .updateMask(cloud)
    .updateMask(cloudShadow)
    .updateMask(snow)
    .updateMask(water);
}

function addLandsatVariables(image) {
  var sr = image.select(['SR_B4', 'SR_B5']).multiply(0.0000275).add(-0.2);
  var ndvi = sr.normalizedDifference(['SR_B5', 'SR_B4']).rename('ndvi');
  var lst = image.select('ST_B10')
    .multiply(0.00341802)
    .add(149.0)
    .subtract(273.15)
    .rename('lst_c');
  return image.addBands([ndvi, lst]);
}

var l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2');
var l9 = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2');
var landsat = l8.merge(l9)
  .filterBounds(boundary)
  .filterDate(start, end)
  .filter(ee.Filter.eq('PROCESSING_LEVEL', 'L2SP'))
  .map(maskLandsatL2)
  .map(addLandsatVariables);

var landsatComposite = landsat.select(['lst_c', 'ndvi']).median().clip(boundary);

var worldCover = ee.ImageCollection('ESA/WorldCover/v200').first().select('Map').clip(boundary);
var grassland = worldCover.eq(30).rename('grassland');
var builtup = worldCover.eq(50).rename('builtup');
var bare = worldCover.eq(60).rename('bare_land');
var waterWetland = worldCover.eq(80).or(worldCover.eq(90)).rename('water_wetland');

var dem = ee.Image('USGS/SRTMGL1_003').select('elevation').clip(boundary);
var slope = ee.Terrain.slope(dem).rename('slope_deg');

var viirs = ee.ImageCollection('NOAA/VIIRS/DNB/ANNUAL_V22')
  .filterDate('2023-01-01', '2024-01-01')
  .select('average_masked')
  .median()
  .rename('night_light')
  .clip(boundary);

var predictors = landsatComposite
  .addBands([grassland, builtup, bare, waterWetland, dem.rename('elevation_m'), slope, viirs]);

var reducers = ee.Reducer.mean()
  .combine({reducer2: ee.Reducer.stdDev(), sharedInputs: true});

var table = predictors.reduceRegions({
  collection: units,
  reducer: reducers,
  scale: 30,
  tileScale: 4
});

Export.table.toDrive({
  collection: table,
  description: 'xi_ujimqin_spatial_units_public_remote_sensing_2023',
  fileFormat: 'CSV'
});
