"""
Generate country reports.

Written by Ed Oughton.

May 2021

"""
import os
import configparser
import pandas as pd
import glob

from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa             # import python module

from countries import COUNTRY_LIST

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

RESULTS = os.path.join(BASE_PATH, '..', 'results')
FIGURES = "D:\\Github\\qubic\\reports\\figures" #unfortunately needs hard coding
IMAGES = "D:\\Github\\qubic\\reports\\images" #unfortunately needs hard coding
OUTPUT = os.path.join(BASE_PATH, '..', 'reports', 'method')


def generate_method(country):
    """
    Meta function to generate a report.

    """
    iso3 = country['iso3']

    technology_inputs = get_technology_inputs(iso3)

    path = os.path.join(BASE_PATH, '..', 'reports', 'templates')
    env = Environment(loader=FileSystemLoader(path))

    template = env.get_template('method_template.html')

    template_vars = {
        "css_location": "D:\\Github\\qubic\\reports\\templates\\style_template.css",
        "preferred_name" : country['preferred_name'],
        "country": iso3,
        "figure_1": os.path.join(FIGURES, '..', '..', 'clustering', 'figures', 'cluster_panel.png'),
        "figure_2": os.path.join(FIGURES, '..', '..', 'method', 'figures', 'method_box_diagram.jpg'),
        "figure_3": os.path.join(IMAGES, iso3, 'demand_graphic.png'),
        "iso3": technology_inputs['iso3'],
        "iso2": technology_inputs['iso2'],
        "global_region": technology_inputs['region'],
        "regional_node_level": technology_inputs['regional_node_level'],
        "core_node_level": technology_inputs['core_node_level'],
        "pop_density_km2": technology_inputs['pop_density_km2'],
        "settlement_size": technology_inputs['settlement_size'],
        "core_node_size": technology_inputs['core_node_size'],
        "cluster": technology_inputs['cluster'],
        "wacc": int(float(technology_inputs['wacc'])),
        "profit_margin": int(float(technology_inputs['profit_margin'])),
        "spectrum_coverage_baseline_usd_mhz_pop": technology_inputs['spectrum_coverage_baseline_usd_mhz_pop'],
        "spectrum_capacity_baseline_usd_mhz_pop": technology_inputs['spectrum_capacity_baseline_usd_mhz_pop'],
        "spectrum_cost_low": int(float(technology_inputs['spectrum_cost_low'])),
        "spectrum_cost_high": int(float(technology_inputs['spectrum_cost_high'])),
        "tax_baseline": int(float(technology_inputs['tax_baseline'])),
        "tax_low": int(float(technology_inputs['tax_low'])),
        "tax_high": int(float(technology_inputs['tax_high'])),
        "administration_percentage_of_network_cost": int(float(technology_inputs['administration_percentage_of_network_cost'])),
        "overbooking_factor": technology_inputs['overbooking_factor'],
        "return_period": technology_inputs['return_period'],
        "discount_rate": technology_inputs['discount_rate'],
        "opex_percentage_of_capex": technology_inputs['opex_percentage_of_capex'],
        "confidence": technology_inputs['confidence'],
        "tdd_dl_to_ul": technology_inputs['tdd_dl_to_ul'],
        "equipment": int(float(technology_inputs['equipment'])),
        "site_build": int(float(technology_inputs['site_build'])),
        "installation": int(float(technology_inputs['installation'])),
        "operation_and_maintenance": int(float(technology_inputs['operation_and_maintenance'])),
        "power": int(float(technology_inputs['power'])),
        "site_rental_urban": int(float(technology_inputs['site_rental_urban'])),
        "site_rental_suburban": int(float(technology_inputs['site_rental_suburban'])),
        "site_rental_rural": int(float(technology_inputs['site_rental_rural'])),
        "fiber_urban_m": int(float(technology_inputs['fiber_urban_m'])),
        "fiber_suburban_m": int(float(technology_inputs['fiber_suburban_m'])),
        "fiber_rural_m": int(float(technology_inputs['fiber_rural_m'])),
        "wireless_small": int(float(technology_inputs['wireless_small'])),
        "wireless_medium": int(float(technology_inputs['wireless_medium'])),
        "wireless_large": int(float(technology_inputs['wireless_large'])),
        "core_node": int(float(technology_inputs['core_node'])),
        "core_edge": int(float(technology_inputs['core_edge'])),
        "regional_node": int(float(technology_inputs['regional_node'])),
        "regional_edge": int(float(technology_inputs['regional_edge'])),
    }

    html_out = template.render(template_vars)

    name = '{} - Qubic Method.pdf'.format(country['preferred_name'])
    path = os.path.join(OUTPUT, name)

    pisa.showLogging()
    convert_html_to_pdf(html_out, path)


def get_sites(iso3):
    """
    Load data.

    """
    output = {}

    filename = 'national_market_results_technology_options.csv'
    path = os.path.join(RESULTS, 'model_results', iso3, filename)
    data = pd.read_csv(path)

    data.loc[data['scenario'].str.endswith('2_2_2', na=False), 'capacity'] = '2 Mbps'
    data.loc[data['scenario'].str.endswith('5_5_5', na=False), 'capacity'] = '5 Mbps'
    data.loc[data['scenario'].str.endswith('10_10_10', na=False), 'capacity'] = '10 Mbps'
    data.loc[data['scenario'].str.endswith('20_20_20', na=False), 'capacity'] = '20 Mbps'

    data.loc[data['scenario'].str.startswith('low', na=False), 'scenario'] = 'Low'
    data.loc[data['scenario'].str.startswith('baseline', na=False), 'scenario'] = 'Baseline'
    data.loc[data['scenario'].str.startswith('high', na=False), 'scenario'] = 'High'

    data['strategy'] = data['strategy'].replace(['3G_umts_wireless_baseline_baseline_baseline_baseline'], '3G (W)')
    data['strategy'] = data['strategy'].replace(['3G_umts_fiber_baseline_baseline_baseline_baseline'], '3G (FB)')
    data['strategy'] = data['strategy'].replace(['4G_epc_wireless_baseline_baseline_baseline_baseline'], '4G (W)')
    data['strategy'] = data['strategy'].replace(['4G_epc_fiber_baseline_baseline_baseline_baseline'], '4G (FB)')
    data['strategy'] = data['strategy'].replace(['5G_nsa_wireless_baseline_baseline_baseline_baseline'], '5G (W)')
    data['strategy'] = data['strategy'].replace(['5G_nsa_fiber_baseline_baseline_baseline_baseline'], '5G (FB)')

    data['generation'] = data['strategy'].str.split(' ').str[0]
    data['backhaul'] = data['strategy'].str.split(' ').str[1]

    for idx, row in data.iterrows():

        key = '{}_{}_{}_{}'.format(
            row['scenario'].lower(),
            row['capacity'].lower().replace(' ', ''),
            row['generation'].lower(),
            row['backhaul'].lower().replace('(','').replace(')',''),
        )

        output[key] = {
            'total_upgraded_sites': row['total_upgraded_sites'],
            'total_new_sites': row['total_new_sites'],
        }

    return output


def get_technology_inputs(iso3):
    """

    """
    output = {}

    filename = 'parameters_technology_options_*.csv'
    path = os.path.join(RESULTS, 'model_results', iso3, filename)
    files = glob.glob(path)
    latest_file_path = max(files, key=os.path.getctime)

    data = pd.read_csv(latest_file_path)

    for idx, row in data.iterrows():

        output[row['parameter'].lower()] = row['value']

    return output


def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err


if __name__ == '__main__':

    if not os.path.exists(os.path.join(OUTPUT)):
        os.makedirs(os.path.join(OUTPUT))

    for country in COUNTRY_LIST:

        if not country['iso3'] == 'BGD':
            continue

        print('Reporting for {}'.format(country['iso3']))

        generate_method(country)
