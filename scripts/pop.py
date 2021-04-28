"""
Collect all population related regional data, including
an estimation of the population < 10 years of age.

Written by Ed Oughton.

March 2021.

"""
import os
import configparser
import json
import csv
import geopandas as gpd
import pandas as pd
import glob
import pyproj
from shapely.geometry import MultiPolygon, mapping, MultiLineString
from shapely.ops import transform, unary_union, nearest_points
import fiona
from fiona.crs import from_epsg
import rasterio
from rasterio.mask import mask
from rasterstats import zonal_stats
from countries import country_list

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')


def find_country_list(continent_list):
    """
    This function produces country information by continent.

    Parameters
    ----------
    continent_list : list
        Contains the name of the desired continent, e.g. ['Africa']

    Returns
    -------
    countries : list of dicts
        Contains all desired country information for countries in
        the stated continent.

    """
    # print('Loading all countries')
    path = os.path.join(DATA_RAW, 'gadm36_levels_shp', 'gadm36_0.shp')
    countries = gpd.read_file(path)

    # print('Adding continent information to country shapes')
    glob_info_path = os.path.join(BASE_PATH, 'global_information.csv')
    load_glob_info = pd.read_csv(glob_info_path, encoding = "ISO-8859-1",
        keep_default_na=False)
    countries = countries.merge(load_glob_info, left_on='GID_0',
        right_on='ISO_3digit')

    subset = countries.loc[countries['continent'].isin(continent_list)]

    countries = []

    for index, country in subset.iterrows():

        if country['GID_0'] in ['COM','CPV','ESH','LBY','LSO','MUS','MYT','SYC'] :
            regional_level =  1
        else:
            regional_level = 2

        countries.append({
            'country_name': country['country'],
            'iso3': country['GID_0'],
            'iso2': country['ISO_2digit'],
            'regional_level': regional_level,
            'region': country['continent']
        })

    return countries


def get_cluster(country):
    """
    Gets the country cluster.

    Parameters
    ----------
    country : dict
        Contains all desired country information.

    Returns
    -------
    country : dict
        Contains all desired country information.

    """
    path = os.path.join(DATA_INTERMEDIATE, 'data_clustering_results.csv')
    data = pd.read_csv(path)

    data = data.to_dict('records')

    for item in data:

        if country['iso3'] == item['ISO_3digit']:

            country['cluster'] = item['cluster']

            return country


def process_country_shapes(country):
    """
    Creates a single national boundary for the desired country.

    Parameters
    ----------
    country : dict
        Contains all desired country information.

    """
    iso3 = country['iso3']

    path = os.path.join(DATA_INTERMEDIATE, iso3)

    if os.path.exists(os.path.join(path, 'national_outline.shp')):
        return 'Completed national outline processing'

    if not os.path.exists(path):
        os.makedirs(path)

    shape_path = os.path.join(path, 'national_outline.shp')

    # print('Loading all country shapes')
    path = os.path.join(DATA_RAW, 'gadm36_levels_shp', 'gadm36_0.shp')
    countries = gpd.read_file(path)

    # print('Getting specific country shape for {}'.format(iso3))
    single_country = countries[countries.GID_0 == iso3]

    # print('Excluding small shapes')
    single_country['geometry'] = single_country.apply(
        remove_small_shapes, axis=1)

    # print('Adding ISO country code and other global information')
    glob_info_path = os.path.join(BASE_PATH, 'global_information.csv')
    load_glob_info = pd.read_csv(glob_info_path, encoding = "ISO-8859-1",
        keep_default_na=False)
    single_country = single_country.merge(
        load_glob_info,left_on='GID_0', right_on='ISO_3digit')

    # print('Exporting processed country shape')
    single_country.to_file(shape_path, driver='ESRI Shapefile')

    return print('Processing country shape complete')


def process_regions(country):
    """
    Function for processing the lowest desired subnational
    regions for the chosen country.

    Parameters
    ----------
    country : dict
        Contains all desired country information.

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

        print('Working on {} level {}'.format(iso3, regional_level))

        if not os.path.exists(folder):
            os.mkdir(folder)

        filename = 'gadm36_{}.shp'.format(regional_level)
        path_regions = os.path.join(DATA_RAW, 'gadm36_levels_shp', filename)
        regions = gpd.read_file(path_regions)

        print('Subsetting {} level {}'.format(iso3, regional_level))
        regions = regions[regions.GID_0 == iso3]

        print('Excluding small shapes')
        regions['geometry'] = regions.apply(remove_small_shapes, axis=1)

        try:
            print('Writing global_regions.shp to file')
            regions.to_file(path_processed, driver='ESRI Shapefile')
        except:
            print('Unable to write {}'.format(filename))
            pass

    print('Completed processing of regional shapes level {}'.format(level))

    return print('Completed processing of regions')


def process_settlement_layer(country):
    """
    Clip the settlement layer to the chosen country boundary
    and place in desired country folder.

    Parameters
    ----------
    country : dict
        Contains all desired country information.

    """
    iso3 = country['iso3']
    regional_level = country['regional_level']

    path_settlements = os.path.join(DATA_RAW,'settlement_layer',
        'ppp_2020_1km_Aggregated.tif')

    settlements = rasterio.open(path_settlements, 'r+')
    settlements.nodata = 255
    settlements.crs = {"init": "epsg:4326"}

    iso3 = country['iso3']
    path_country = os.path.join(DATA_INTERMEDIATE, iso3,
        'national_outline.shp')

    if os.path.exists(path_country):
        country = gpd.read_file(path_country)
    else:
        print('Must generate national_outline.shp first' )

    path_country = os.path.join(DATA_INTERMEDIATE, iso3)
    shape_path = os.path.join(path_country, 'settlements.tif')

    if os.path.exists(shape_path):
        return print('Completed settlement layer processing')

    print('----')
    print('Working on {} level {}'.format(iso3, regional_level))

    bbox = country.envelope
    geo = gpd.GeoDataFrame()

    geo = gpd.GeoDataFrame({'geometry': bbox})

    coords = [json.loads(geo.to_json())['features'][0]['geometry']]

    out_img, out_transform = mask(settlements, coords, crop=True)

    out_meta = settlements.meta.copy()

    out_meta.update({"driver": "GTiff",
                    "height": out_img.shape[1],
                    "width": out_img.shape[2],
                    "transform": out_transform,
                    "crs": 'epsg:4326'})

    with rasterio.open(shape_path, "w", **out_meta) as dest:
            dest.write(out_img)

    return print('Completed processing of settlement layer')


def process_age_sex_structure(country):
    """
    Clip each demographic layer to the chosen country boundary
    and place in desired country folder.

    Parameters
    ----------
    country : dict
        Contains all desired country information.

    """
    iso3 = country['iso3']

    path = os.path.join(DATA_RAW, 'settlement_layer')
    all_paths = glob.glob(path + '/*.tif')

    for path in all_paths:

        # if os.path.basename(path).startswith('ppp_2020_1km_Aggregated'):
        #     continue

        directory_out = os.path.join(DATA_INTERMEDIATE, iso3, 'age_sex_structure')

        if not os.path.exists(directory_out):
            os.makedirs(directory_out)

        filename = os.path.basename(path)
        path_out = os.path.join(directory_out, filename)

        if os.path.exists(path_out):
            continue

        settlements = rasterio.open(path, 'r+')
        settlements.nodata = 0
        settlements.crs = {"init": "epsg:4326"}

        filename = 'national_outline.shp'
        path_country = os.path.join(DATA_INTERMEDIATE, iso3, filename)

        if os.path.exists(path_country):
            country = gpd.read_file(path_country)
        else:
            print('Must generate national_outline.shp first' )

        geo = gpd.GeoDataFrame({'geometry': country['geometry']})

        coords = [json.loads(geo.to_json())['features'][0]['geometry']]

        #chop on coords
        out_img, out_transform = mask(settlements, coords, crop=True)

        # Copy the metadata
        out_meta = settlements.meta.copy()

        out_meta.update({"driver": "GTiff",
                        "height": out_img.shape[1],
                        "width": out_img.shape[2],
                        "transform": out_transform,
                        "crs": 'epsg:4326'})

        with rasterio.open(path_out, "w", **out_meta) as dest:
                dest.write(out_img)

    return print('Completed processing of settlement layer')


def get_regional_data(country):
    """
    Extract regional data including luminosity and population.

    Parameters
    ----------
    country : dict
        Contains all desired country information.

    """
    iso3 = country['iso3']
    level = country['regional_level']
    gid_level = 'GID_{}'.format(level)

    filename = 'regional_data.csv'
    path_output = os.path.join(DATA_INTERMEDIATE, iso3, filename)

    if os.path.exists(path_output):
        return print('Regional data already exists')

    path_country = os.path.join(DATA_INTERMEDIATE, iso3,
        'national_outline.shp')

    single_country = gpd.read_file(path_country)

    path_night_lights = os.path.join(DATA_INTERMEDIATE, iso3,
        'night_lights.tif')

    filename = 'regions_{}_{}.shp'.format(level, iso3)
    folder = os.path.join(DATA_INTERMEDIATE, iso3, 'regions')
    path = os.path.join(folder, filename)
    regions = gpd.read_file(path)#[:1]

    results = []

    for index, region in regions.iterrows():

        with rasterio.open(path_night_lights) as src:

            affine = src.transform
            array = src.read(1)
            array[array <= 0] = 0

            luminosity_summation = [d['sum'] for d in zonal_stats(
                region['geometry'],
                array,
                stats=['sum'],
                nodata=0,
                affine=affine)][0]

        pop = get_pop_dict(iso3, region)

        area_km2 = round(area_of_polygon(region['geometry']) / 1e6)

        if luminosity_summation == None:
            luminosity_summation = 0

        if area_km2 == 0:
            continue

        results.append({
            'GID_0': region['GID_0'],
            'GID_id': region[gid_level],
            'GID_level': gid_level,
            'population_total': pop['population_summation'],
            'population_over_10': (pop['population_f_over_10'] +
                pop['population_m_over_10']),
            'population_f_over_10': pop['population_f_over_10'],
            'population_m_over_10': pop['population_m_over_10'],
            'area_km2': area_km2,
            'population_km2': (pop['population_summation'] /
                area_km2 if pop['population_summation'] else 0),
            'population_over_10km2': (
                (pop['population_f_over_10'] + pop['population_m_over_10']) /
                area_km2 if pop['population_summation'] else 0),
            'mean_luminosity_km2': (luminosity_summation /
                area_km2 if luminosity_summation else 0)
        })

    results_df = pd.DataFrame(results)

    results_df.to_csv(path_output, index=False)

    print('Completed {}'.format(single_country.NAME_0.values[0]))

    return print('Completed night lights data querying')


def get_pop_dict(iso3, region):
    """
    Build a population dictionary.

    """
    interim = {}

    interim['population_summation'] = find_pop('all', 'all', region, iso3)

    interim['population_f_0'] = find_pop('f', 0, region, iso3)
    interim['population_f_1'] = find_pop('f', 1, region, iso3)
    interim['population_f_5'] = find_pop('f', 5, region, iso3)
    interim['population_f_10'] = find_pop('f', 10, region, iso3)
    interim['population_f_15'] = find_pop('f', 15, region, iso3)
    interim['population_f_20'] = find_pop('f', 20, region, iso3)
    interim['population_f_25'] = find_pop('f', 25, region, iso3)
    interim['population_f_30'] = find_pop('f', 30, region, iso3)
    interim['population_f_35'] = find_pop('f', 35, region, iso3)
    interim['population_f_40'] = find_pop('f', 40, region, iso3)
    interim['population_f_45'] = find_pop('f', 45, region, iso3)
    interim['population_f_50'] = find_pop('f', 50, region, iso3)
    interim['population_f_55'] = find_pop('f', 55, region, iso3)
    interim['population_f_60'] = find_pop('f', 60, region, iso3)
    interim['population_f_65'] = find_pop('f', 65, region, iso3)
    interim['population_f_70'] = find_pop('f', 70, region, iso3)
    interim['population_f_75'] = find_pop('f', 75, region, iso3)
    interim['population_f_80'] = find_pop('f', 80, region, iso3)
    interim['population_m_0'] = find_pop('m', 0, region, iso3)
    interim['population_m_1'] = find_pop('m', 1, region, iso3)
    interim['population_m_5'] = find_pop('m', 5, region, iso3)
    interim['population_m_10'] = find_pop('m', 10, region, iso3)
    interim['population_m_15'] = find_pop('m', 15, region, iso3)
    interim['population_m_20'] = find_pop('m', 20, region, iso3)
    interim['population_m_25'] = find_pop('m', 25, region, iso3)
    interim['population_m_30'] = find_pop('m', 30, region, iso3)
    interim['population_m_35'] = find_pop('m', 35, region, iso3)
    interim['population_m_40'] = find_pop('m', 40, region, iso3)
    interim['population_m_45'] = find_pop('m', 45, region, iso3)
    interim['population_m_50'] = find_pop('m', 50, region, iso3)
    interim['population_m_55'] = find_pop('m', 55, region, iso3)
    interim['population_m_60'] = find_pop('m', 60, region, iso3)
    interim['population_m_65'] = find_pop('m', 65, region, iso3)
    interim['population_m_70'] = find_pop('m', 70, region, iso3)
    interim['population_m_75'] = find_pop('m', 75, region, iso3)
    interim['population_m_80'] = find_pop('m', 80, region, iso3)

    pop = {}

    population_total = 0
    population_f_over_10 = 0
    population_m_over_10 = 0

    for key, value in interim.items():

        if key == 'population_summation':
            pop['population_summation'] = round(value)
            continue

        population_total += value

        if key.split('_')[1] == 'f':
            if int(key.split('_')[2]) >= 10:
                population_f_over_10 += value
        elif key.split('_')[1] == 'm':
            if int(key.split('_')[2]) >= 10:
                population_m_over_10 += value
        else:
            print('Did not recognize population key')

    pop['population_total'] = round(population_total)
    pop['population_f_over_10'] = round(population_f_over_10)
    pop['population_m_over_10'] = round(population_m_over_10)

    return pop


def find_pop(gender, age, region, iso3):
    """
    Find the estimated population.

    """
    folder = os.path.join(DATA_INTERMEDIATE, iso3, 'age_sex_structure')

    if not gender == 'all' and not age == 'all':
        filename = 'global_{}_{}_2020_1km.tif'.format(gender, age)
    else:
        filename = 'ppp_2020_1km_Aggregated.tif'

    path = os.path.join(folder, filename)

    with rasterio.open(path) as src:

        affine = src.transform
        array = src.read(1)
        array[array <= 0] = 0

        population_summation = [d['sum'] for d in zonal_stats(
            region['geometry'],
            array,
            stats=['sum'],
            nodata=0,
            affine=affine)][0]

        if population_summation is not None:
            return population_summation
        else:
            return 0


def area_of_polygon(geom):
    """
    Returns the area of a polygon. Assume WGS84 as crs.

    """
    geod = pyproj.Geod(ellps="WGS84")

    poly_area, poly_perimeter = geod.geometry_area_perimeter(
        geom
    )

    return abs(poly_area)


def remove_small_shapes(x):
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


def get_points_inside_country(nodes, iso3):
    """
    Check settlement locations lie inside target country.

    Parameters
    ----------
    nodes : dataframe
        A geopandas dataframe containing settlement nodes.
    iso3 : string
        ISO 3 digit country code.

    Returns
    -------
    nodes : dataframe
        A geopandas dataframe containing settlement nodes.

    """
    filename = 'national_outline.shp'
    path = os.path.join(DATA_INTERMEDIATE, iso3, filename)

    national_outline = gpd.read_file(path)

    bool_list = nodes.intersects(national_outline.unary_union)

    nodes = pd.concat([nodes, bool_list], axis=1)

    nodes = nodes[nodes[0] == True].drop(columns=0)

    return nodes


def forecast_subscriptions(country):
    """
    Forecast the number of unique cellular subscriptions.

    Parameters
    ----------
    country : dict
        Contains all country specfic information.

    """
    iso3 = country['iso3']

    path = os.path.join(DATA_RAW, 'gsma', 'gsma_unique_subscribers.csv')
    historical_data = load_subscription_data(path, country['iso3'])

    start_point = 2021
    end_point = 2030
    horizon = 4

    forecast = forecast_linear(
        country,
        historical_data,
        start_point,
        end_point,
        horizon
    )

    forecast_df = pd.DataFrame(historical_data + forecast)

    path = os.path.join(DATA_INTERMEDIATE, iso3, 'subscriptions')

    if not os.path.exists(path):
        os.mkdir(path)

    forecast_df.to_csv(os.path.join(path, 'subs_forecast.csv'), index=False)

    path = os.path.join(BASE_PATH, '..', 'vis', 'subscriptions', 'data_inputs')
    forecast_df.to_csv(os.path.join(path, '{}.csv'.format(iso3)), index=False)

    return print('Completed subscription forecast')


def load_subscription_data(path, iso3):
    """
    Load in itu cell phone subscription data.

    Parameters
    ----------
    path : string
        Location of itu data as .csv.
    iso3 : string
        ISO3 digital country code.

    Returns
    -------
    output : list of dicts
        Time series data of cell phone subscriptions.

    """
    output = []

    historical_data = pd.read_csv(path, encoding = "ISO-8859-1")
    historical_data = historical_data.to_dict('records')

    scenarios = ['low', 'baseline', 'high']

    for scenario in scenarios:
        for year in range(2010, 2021):
            year = str(year)
            for item in historical_data:
                if item['iso3'] == iso3:
                    output.append({
                        'scenario': scenario,
                        'country': iso3,
                        'penetration': float(item[year]) * 100,
                        'year':  year,
                    })

    return output


def forecast_linear(country, historical_data, start_point, end_point, horizon):
    """
    Forcasts subscription adoption rate.

    Parameters
    ----------
    historical_data : list of dicts
        Past penetration data.
    start_point : int
        Starting year of forecast period.
    end_point : int
        Final year of forecast period.
    horizon : int
        Number of years to use to estimate mean growth rate.

    Returns
    -------
    output : list of dicts
        Time series data of cell phone subscriptions.

    """
    output = []

    scenarios = ['low', 'baseline', 'high']

    for scenario in scenarios:

        scenario_data = []

        subs_growth = country['subs_growth_{}'.format(scenario)]

        year_0 = sorted(historical_data, key = lambda i: i['year'], reverse=True)[0]

        for year in range(start_point, end_point + 1):
            if year == start_point:

                penetration = year_0['penetration'] * (1 + (subs_growth/100))
            else:
                penetration = penetration * (1 + (subs_growth/100))

            if year not in [item['year'] for item in scenario_data]:

                scenario_data.append({
                    'scenario': scenario,
                    'country': country['iso3'],
                    'year': year,
                    'penetration': round(penetration, 2),
                })

        output = output + scenario_data

    return output


def forecast_smartphones(country):
    """
    Forecast smartphone adoption.

    Parameters
    ----------
    country : dict
        Contains all country specfic information.

    """
    iso3 = country['iso3']

    filename = 'wb_smartphone_survey.csv'
    path = os.path.join(DATA_RAW, 'wb_smartphone_survey', filename)
    survey_data = load_smartphone_data(path, country)

    start_point = 2020
    end_point = 2030

    forecast = forecast_smartphones_linear(
        survey_data,
        country,
        start_point,
        end_point
    )

    forecast_df = pd.DataFrame(forecast)

    path = os.path.join(DATA_INTERMEDIATE, iso3, 'subscriptions')

    if not os.path.exists(path):
        os.mkdir(path)

    forecast_df.to_csv(os.path.join(path, 'smartphone_forecast.csv'), index=False)

    path = os.path.join(BASE_PATH, '..', 'vis', 'smartphones', 'data_inputs')
    if not os.path.exists(path):
        os.mkdir(path)
    forecast_df.to_csv(os.path.join(path, '{}.csv'.format(iso3)), index=False)

    return print('Completed subscription forecast')


def load_smartphone_data(path, country):
    """
    Load smartphone adoption survey data.

    Parameters
    ----------
    path : string
        Location of data as .csv.
    country : string
        ISO3 digital country code.

    """
    survey_data = pd.read_csv(path)

    survey_data = survey_data.to_dict('records')

    countries_with_data = [i['iso3'] for i in survey_data]

    output = []

    if country['iso3']  in countries_with_data:
        for item in survey_data:
                if item['iso3'] == country['iso3']:
                    output.append({
                        'country': item['iso3'],
                        'cluster': item['cluster'],
                        'settlement_type': item['Settlement'],
                        'smartphone_penetration': item['Smartphone']
                    })

    else:
        for item in survey_data:
            if item['cluster'] == country['cluster']:
                output.append({
                    'country': country['iso3'],
                    'cluster': item['cluster'],
                    'settlement_type': item['Settlement'],
                    'smartphone_penetration': item['Smartphone']
                })

    return output


def forecast_smartphones_linear(data, country, start_point, end_point):
    """
    Forecast smartphone adoption.

    Parameters
    ----------
    data : list of dicts
        Survey data.
    country : string
        ISO3 digital country code.
    start_point : int
        Starting year of forecast period.
    end_point : int
        Final year of forecast period.

    Returns
    -------
    output : list of dicts
        Time series forecast of smartphone penetration.

    """
    output = []

    scenarios = ['low', 'baseline', 'high']
    settlement_types = ['urban', 'rural']

    for scenario in scenarios:
        for settlement_type in settlement_types:

            smartphone_growth = country['sp_growth_{}_{}'.format(scenario, settlement_type)]

            for item in data:

                if not item['settlement_type'].lower() == settlement_type:
                    continue

                for year in range(start_point, end_point + 1):

                    if year == start_point:

                        penetration = item['smartphone_penetration']

                    else:

                        penetration = penetration * (1 + (smartphone_growth/100))

                    if penetration > 95:
                        penetration = 95

                    output.append({
                        'scenario': scenario,
                        'country': item['country'],
                        'settlement_type': item['settlement_type'].lower(),
                        'year': year,
                        'penetration': round(penetration, 2),
                    })

    return output


if __name__ == '__main__':

    # countries = find_country_list(['Africa'])
    # countries = countries#[::-1]

    for country in country_list:#[:1]:

        # if not country['iso3'] == 'COD':
        #     continue

        print('----')
        print('-- Working on {}'.format(country['country_name']))

        country = get_cluster(country)

        print('Processing country boundary')
        process_country_shapes(country)

        print('Processing regions')
        process_regions(country)

        print('Processing settlement layers')
        process_settlement_layer(country)

        print('Processing age/sex structure')
        process_age_sex_structure(country)

        print('Getting regional data')
        get_regional_data(country)

        print('Create subscription forcast')
        forecast_subscriptions(country)

        print('Forecasting smartphones')
        forecast_smartphones(country)

    print('--Completed regional population data estimation')
