#!/bin/bash/
# http://www.nyc.gov/html/dcp/pdf/bytes/nynta_metadata.pdf?r=15c

# remove files
echo
echo "Removing geo/topo json files from working directory"
rm working/nyc-geo.json
rm working/nyc-topo.json

# TODO should we filter by only boros which participate in citibike?
# -where "BoroName IN ('Brooklyn', 'Manhattan', 'Queens')"
echo
echo "Processing Shapefile into GeoJSON using ogr2ogr.."
ogr2ogr \
    -f GeoJSON \
    working/nyc-geo.json \
    input/nynta_15d/nynta.shp

# TODO find and load shape file for NJ / Hudson county / JC

# list all files to combine after hyphens
echo
echo "Processing GeoJSON into TopoJSON.."
topojson \
    -o working/nyc-topo.json \
    --id-property NTACode \
    --properties name=NTAName \
    -- \
    working/nyc-geo.json

echo
echo "Done!"
