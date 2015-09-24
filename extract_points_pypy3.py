#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import multiprocessing
import os
import sys

from shapely.geometry import shape
from shapely.geometry import Point

from functools import partial
from itertools import islice

def row_in_poly(poly, row):
    p = Point(float(row[1]), float(row[2]))
    return poly.contains(p)

def grab_points(points, polygon, job_id, output_file=None):
    lon, lat = 1, 2
    xn, yn, xx, yx = polygon.bounds
    points = [p.replace('\\n', '').split(',') for p in points]
    points = filter(lambda df: not (float(df[lon]) >= xx or float(df[lon]) <= xn or float(df[lat]) >= yx or float(df[lat]) <= yn), points)
    within_func = partial(row_in_poly, polygon)
    contains_points = list(filter(within_func, points))
    contains_points = ['{},{},{},{}'.format(*p) for p in contains_points]
    return job_id, contains_points, output_file

def worker_callback(results):
    job_id, points, output_file = results
    with open(output_file, 'a') as output_f: 
        output_f.writelines(points)
    print('job {} : {} records'.format(job_id, len(points)))

def main(input_csv, input_geojson, aoi_field, aoi_id, output_file):

    if os.path.exists(output_file):
        os.remove(output_file)

    pool = multiprocessing.Pool()
    with open(input_geojson, 'r') as poly_file:
        feature_collection = json.loads(poly_file.read())['features']
        filtered = filter(lambda f: f['properties'][aoi_field] == aoi_id, feature_collection)
        job_id = 0
        results = []
        for feature in filtered:
            poly = shape(feature['geometry'])
            with open(input_csv) as f:
                is_more = True
                while is_more:
                    job_id += 1
                    chunksize = 25000
                    chunk = list(islice(f, chunksize))
                    results.append(pool.apply_async(grab_points, args=(chunk, poly, job_id, output_file)))
                    if len(chunk) < chunksize:
                        is_more = False
        
        for r in results:
            worker_callback(r.get())

if __name__ == '__main__':
    '''
    python extract_points.py input_csv input_shapefile shapefile_field, field_value, output_csv_path

    Example:
    pypy3 extract_points.py ../BRIntegrator/ind_results.csv /Users/bcollins/Downloads/IDN_Grid_Masks/IDN_10km.shp Name IDN extracted_points.csv
    '''
    if len(sys.argv) > 1:
        main(*sys.argv[1:])
    else:
        input_file = 'extract_test_data.csv'
        input_shape = '/Users/bcollins/Downloads/IDN_Grid_Masks/IDN_10km.geojson'
        field = 'Name'
        val = 'IDN'
        output = 'test_extract_points_out.csv'
        main(input_file, input_shape, field, val, output)
