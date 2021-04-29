"""
Read in available site data

Written by Ed Oughton

21st April 2020

"""
import os
import csv
import configparser
import pandas as pd
import geopandas as gpd
import xlrd
import numpy as np
from shapely.geometry import MultiPolygon
from shapely.ops import transform, unary_union

from countries import COUNTRY_LIST

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw', 'real_site_data')
DATA_INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')


def process_country_shape(country):
    """
    Creates a single national boundary for the desired country.

    Parameters
    ----------
    country : string
        Three digit ISO country code.

    """
    print('----')

    iso3 = country['iso3']

    path = os.path.join(DATA_INTERMEDIATE, iso3)

    if os.path.exists(os.path.join(path, 'national_outline.shp')):
        return 'Completed national outline processing'

    if not os.path.exists(path):
        print('Creating directory {}'.format(path))
        os.makedirs(path)
    shape_path = os.path.join(path, 'national_outline.shp')

    print('Loading all country shapes')
    path = os.path.join(DATA_RAW, '..', 'gadm36_levels_shp', 'gadm36_0.shp')
    countries = gpd.read_file(path)

    print('Getting specific country shape for {}'.format(iso3))
    single_country = countries[countries.GID_0 == iso3]

    print('Excluding small shapes')
    single_country['geometry'] = single_country.apply(
        exclude_small_shapes, axis=1)

    print('Adding ISO country code and other global information')
    glob_info_path = os.path.join(BASE_PATH, 'global_information.csv')
    load_glob_info = pd.read_csv(glob_info_path, encoding = "ISO-8859-1")
    single_country = single_country.merge(
        load_glob_info,left_on='GID_0', right_on='ISO_3digit')

    print('Exporting processed country shape')
    single_country.to_file(shape_path, driver='ESRI Shapefile')

    return print('Processing country shape complete')


def process_regions(country):
    """
    Function for processing the lowest desired subnational regions for the
    chosen country.

    Parameters
    ----------
    country : string
        Three digit ISO country code.

    """
    regions = []

    iso3 = country['iso3']
    level = country['regional_level']

    for regional_level in range(1, level + 1):

        filename = 'regions_{}_{}.shp'.format(regional_level, iso3)
        folder = os.path.join(DATA_INTERMEDIATE, iso3, 'regions')
        path_processed = os.path.join(folder, filename)

        if os.path.exists(path_processed):
            continue

        print('----')
        print('Working on {} level {}'.format(iso3, regional_level))

        if not os.path.exists(folder):
            os.mkdir(folder)

        filename = 'gadm36_{}.shp'.format(regional_level)
        path_regions = os.path.join(DATA_RAW, '..',  'gadm36_levels_shp', filename)
        regions = gpd.read_file(path_regions)

        print('Subsetting {} level {}'.format(iso3, regional_level))
        regions = regions[regions.GID_0 == iso3]

        print('Excluding small shapes')
        regions['geometry'] = regions.apply(exclude_small_shapes, axis=1)

        try:
            print('Writing global_regions.shp to file')
            regions.to_file(path_processed, driver='ESRI Shapefile')
        except:
            print('Unable to write {}'.format(filename))
            pass

    print('Completed processing of regional shapes level {}'.format(level))

    return print('complete')


def exclude_small_shapes(x):
    """
    Remove small multipolygon shapes.

    Parameters
    ---------
    x : polygon
        Feature to simplify.

    Returns
    -------
    MultiPolygon : MultiPolygon
        Shapely MultiPolygon geometry without tiny shapes.

    """
    # if its a single polygon, just return the polygon geometry
    if x.geometry.geom_type == 'Polygon':
        return x.geometry

    # if its a multipolygon, we start trying to simplify
    # and remove shapes if its too big.
    elif x.geometry.geom_type == 'MultiPolygon':

        area1 = 0.01
        area2 = 50

        # dont remove shapes if total area is already very small
        if x.geometry.area < area1:
            return x.geometry
        # remove bigger shapes if country is really big

        if x['GID_0'] in ['CHL','IDN']:
            threshold = 0.01
        elif x['GID_0'] in ['RUS','GRL','CAN','USA']:
            threshold = 0.01

        elif x.geometry.area > area2:
            threshold = 0.1
        else:
            threshold = 0.001

        # save remaining polygons as new multipolygon for
        # the specific country
        new_geom = []
        for y in x.geometry:
            if y.area > threshold:
                new_geom.append(y)

        return MultiPolygon(new_geom)


def process_coverage_shapes(country):
    """
    Load in coverage maps, process and export for each country.

    Parameters
    ----------
    country : string
        Three digit ISO country code.

    """
    iso3 = country['iso3']
    iso2 = country['iso2']

    technologies = [
        'GSM',
        '3G',
        '4G'
    ]

    for tech in technologies:

        folder_coverage = os.path.join(DATA_INTERMEDIATE, iso3, 'coverage')
        filename = 'coverage_{}.shp'.format(tech)
        path_output = os.path.join(folder_coverage, filename)

        if os.path.exists(path_output):
            continue

        print('----')
        print('Working on {} in {}'.format(tech, iso3))

        filename = 'Inclusions_201812_{}.shp'.format(tech)
        folder = os.path.join(DATA_RAW, '..', 'mobile_coverage_explorer',
            'Data_MCE')
        inclusions = gpd.read_file(os.path.join(folder, filename))

        if iso2 in inclusions['CNTRY_ISO2']:

            filename = 'MCE_201812_{}.shp'.format(tech)
            folder = os.path.join(DATA_RAW, '..', 'mobile_coverage_explorer',
                'Data_MCE')
            coverage = gpd.read_file(os.path.join(folder, filename))

            coverage = coverage.loc[coverage['CNTRY_ISO3'] == iso3]

        else:

            filename = 'OCI_201812_{}.shp'.format(tech)
            folder = os.path.join(DATA_RAW, '..', 'mobile_coverage_explorer',
                'Data_OCI')
            coverage = gpd.read_file(os.path.join(folder, filename))

            coverage = coverage.loc[coverage['CNTRY_ISO3'] == iso3]

        if len(coverage) > 0:

            print('Dissolving polygons')
            coverage['dissolve'] = 1
            coverage = coverage.dissolve(by='dissolve', aggfunc='sum')

            coverage = coverage.to_crs({'init': 'epsg:3857'})

            print('Excluding small shapes')
            coverage['geometry'] = coverage.apply(clean_coverage,axis=1)

            print('Removing empty and null geometries')
            coverage = coverage[~(coverage['geometry'].is_empty)]
            coverage = coverage[coverage['geometry'].notnull()]

            print('Simplifying geometries')
            coverage['geometry'] = coverage.simplify(
                tolerance = 0.005,
                preserve_topology=True).buffer(0.0001).simplify(
                tolerance = 0.005,
                preserve_topology=True
            )

            coverage = coverage.to_crs({'init': 'epsg:4326'})

            if not os.path.exists(folder_coverage):
                os.makedirs(folder_coverage)

            coverage.to_file(path_output, driver='ESRI Shapefile')

    print('Processed coverage shapes')


def clean_coverage(x):
    """
    Cleans the coverage polygons by remove small multipolygon shapes.

    Parameters
    ---------
    x : polygon
        Feature to simplify.

    Returns
    -------
    MultiPolygon : MultiPolygon
        Shapely MultiPolygon geometry without tiny shapes.

    """
    # if its a single polygon, just return the polygon geometry
    if x.geometry.geom_type == 'Polygon':
        if x.geometry.area > 1e7:
            return x.geometry

    # if its a multipolygon, we start trying to simplify and
    # remove shapes if its too big.
    elif x.geometry.geom_type == 'MultiPolygon':

        threshold = 1e7

        # save remaining polygons as new multipolygon for
        # the specific country
        new_geom = []
        for y in x.geometry:

            if y.area > threshold:
                new_geom.append(y)

        return MultiPolygon(new_geom)


def load_regions(path):

    regions = gpd.read_file(path, crs='epsg:4326')

    return regions


def process_the_gambia():

    print('Processing The Gambia')
    folder = os.path.join(DATA_INTERMEDIATE, 'GMB', 'sites')
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(DATA_INTERMEDIATE, 'GMB', 'regions', 'regions_2_GMB.shp')
    regions = load_regions(path)

    path = os.path.join(DATA_RAW, 'GMB', 'Gambia Network_Africell.xlsx')
    process_all_sites_the_gambia(path, regions, folder)

    sites_lut = sites_lut_the_gambia(path, regions, folder)

    print('Writing The Gambia csv data')
    sites_lut.to_csv(os.path.join(folder, 'sites.csv'), index=False)


def process_all_sites_the_gambia(path, regions, folder):

    df = pd.read_excel(path, 'Sites', skiprows=1)

    df = df[['Site_ID', 'site_name', 'Longitude', 'Latitude',
        '2G, 3G, 4G, Wifi etc', #technology?
        'Fibre, microwave', #backhaul type?
        'Yes / No', #main grid?
    ]]
    df.columns = ['site_id', 'site_name', 'longitude', 'latitude',
        'technology', 'backhaul', 'on_grid']
    df = df.dropna()

    df = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

    df = df.drop_duplicates(['site_id'])

    output = []

    for idx, point in df.iterrows():
        for idx, region in regions.iterrows():
            if point['geometry'].intersects(region['geometry']):
                output.append({
                    'type': 'Feature',
                    'geometry': point['geometry'],
                    'properties': {
                        'site_id': point['site_id'],
                        'site_name': point['site_name'],
                        'technology': point['technology'],
                        'backhaul': point['backhaul'],
                        'on_grid': point['on_grid'],
                        'GID_2': region['GID_2'],
                    }
                })

    df = gpd.GeoDataFrame().from_features(output, crs='epsg:4326')

    filename = 'sites.shp'
    df.to_file(os.path.join(folder, filename), crs='epsg:4326')

    return df


def sites_lut_the_gambia(path, regions, folder):
    """

    """
    df = pd.read_excel(path, 'Sites', skiprows=1)

    df = df[['Site_ID', 'site_name', 'Longitude', 'Latitude',
        '2G, 3G, 4G, Wifi etc', #technology?
        'Fibre, microwave', #backhaul type?
        'Yes / No', #main grid?
    ]]
    df.columns = ['site_id', 'site_name', 'longitude', 'latitude',
        'technology', 'backhaul', 'on_grid']
    df = df.dropna()

    df = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

    df = df.drop_duplicates(['site_id'])

    output = []

    for idx, region in regions.iterrows():

        sites_2G = 0
        sites_3G = 0
        sites_4G = 0
        wireless = 0
        fiber = 0
        on_grid = 0
        off_grid = 0

        for idx, point in df.iterrows():
            if region['geometry'].intersects(point['geometry']):

                if '2G' in point['technology']:
                    sites_2G += 1
                if '3G' in point['technology']:
                    sites_3G += 1
                if '4G' in point['technology']:
                    sites_4G += 1
                if 'Microwave' in point['backhaul']:
                    wireless += 1
                if 'Fibre' in point['backhaul']:
                    fiber += 1
                if 'Yes' in point['on_grid']:
                    on_grid += 1
                if 'No' in point['on_grid']:
                    off_grid += 1

        output.append({
            # 'type': 'Feature',
            # 'geometry': region['geometry'],
            # 'properties': {
            'GID_0': region['GID_0'],
            'GID_2': region['GID_2'],
            'sites_2G': sites_2G,
            'sites_3G': sites_3G,
            'sites_4G': sites_4G,
            'total_estimated_sites': sites_2G + sites_3G + sites_4G,
            'backhaul_wireless': wireless ,
            'backhaul_fiber':  fiber / (wireless + fiber) * 100 if fiber else 0,
            'on_grid': on_grid ,
            'off_grid': off_grid,
        })

    output = pd.DataFrame(output)

    return output


if __name__ == "__main__":

    for country in COUNTRY_LIST:

        print('Processing country boundary')
        process_country_shape(country)

        print('Processing regions')
        process_regions(country)

        print('Processing coverage shapes')
        process_coverage_shapes(country)

        if country['iso3'] == 'GMB':
            process_the_gambia()
