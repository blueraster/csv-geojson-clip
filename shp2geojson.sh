#!/usr/bin/env bash
#ogr2ogr -f geoJSON /tmp/Africa_05km_buff.geojson ~/Downloads/Africa_Masks/Africa_05km_buff.shp

ogr2ogr -f geoJSON ${1} ${2}