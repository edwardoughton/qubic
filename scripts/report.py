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
OUTPUT = os.path.join(BASE_PATH, '..', 'reports', 'countries')


def generate_report(country):
    """
    Meta function to generate a report.

    """
    iso3 = country['iso3']
    rounding = country['rounding']

    sites = get_sites(iso3)
    tech_costs = get_tech_costs(iso3, rounding)

    tech_percs = get_tech_percentages(iso3, rounding)
    share_percs = get_sharing_data(iso3, rounding)
    policy_percs = get_policy_data(iso3, country['rounding_policy'])

    technology_inputs = get_technology_inputs(iso3)
    policy_inputs = get_policy_inputs(iso3)
    spectrum_bands = get_frequencies(iso3)

    path = os.path.join(BASE_PATH, '..', 'reports', 'templates')
    env = Environment(loader=FileSystemLoader(path))

    template = env.get_template('qubic_template.html')

    template_vars = {
        "css_location": "D:\\Github\\qubic\\reports\\templates\\style_template.css",
        "preferred_name" : country['preferred_name'],
        "country": iso3,
        "total_estimated_sites": sites['total_estimated_sites'],
        # "sites_4G": sites['sites_4G'],
        "backhaul_wireless": sites['backhaul_wireless'],
        "figure_1": os.path.join(IMAGES, iso3, 'social_costs_by_strategy.png'),
        # "upgraded_sites_baseline_10mbps_3g_w": sites['baseline_10mbps_3g_w']['total_upgraded_sites'],
        # "new_sites_baseline_10mbps_3g_w": sites['baseline_10mbps_3g_w']['total_new_sites'],
        # "upgraded_sites_baseline_10mbps_4g_w": sites['baseline_10mbps_4g_w']['total_upgraded_sites'],
        # "new_sites_baseline_10mbps_4g_w": sites['baseline_10mbps_4g_w']['total_new_sites'],
        # "upgraded_sites_baseline_10mbps_5g_w": sites['baseline_10mbps_5g_w']['total_upgraded_sites'],
        # "new_sites_baseline_10mbps_5g_w": sites['baseline_10mbps_5g_w']['total_new_sites'],
        "baseline_10mbps_3g_w": tech_percs['baseline_10mbps_3g_w']['social_cost_bn'],
        "baseline_10mbps_4g_w": tech_percs['baseline_10mbps_4g_w']['social_cost_bn'],
        "baseline_10mbps_5g_w": tech_percs['baseline_10mbps_5g_w']['social_cost_bn'],
        "w_over_fb_3g_10mbps": round(abs(tech_percs['baseline_10mbps_3g_w']['w_over_fb'])),
        "w_over_fb_4g_10mbps": round(abs(tech_percs['baseline_10mbps_4g_w']['w_over_fb'])),
        "w_over_fb_5g_10mbps": round(abs(tech_percs['baseline_10mbps_5g_w']['w_over_fb'])),
        "perc_saving_vs_3g_4g_10mbps": round(abs(tech_percs['baseline_10mbps_4g_w']['perc_saving_vs_3g'])),
        "perc_saving_vs_3g_5g_10mbps": round(abs(tech_percs['baseline_10mbps_5g_w']['perc_saving_vs_3g'])),
        "low_5mbps_3g_w": tech_percs['low_5mbps_3g_w']['social_cost_bn'],
        "low_5mbps_4g_w": tech_percs['low_5mbps_4g_w']['social_cost_bn'],
        "low_5mbps_5g_w": tech_percs['low_5mbps_5g_w']['social_cost_bn'],
        "high_5mbps_3g_w": tech_percs['high_5mbps_3g_w']['social_cost_bn'],
        "high_5mbps_4g_w": tech_percs['high_5mbps_4g_w']['social_cost_bn'],
        "high_5mbps_5g_w": tech_percs['high_5mbps_5g_w']['social_cost_bn'],
        "baseline_5mbps_3g_w": tech_percs['baseline_5mbps_3g_w']['social_cost_bn'],
        "baseline_5mbps_4g_w": tech_percs['baseline_5mbps_4g_w']['social_cost_bn'],
        "baseline_5mbps_5g_w": tech_percs['baseline_5mbps_5g_w']['social_cost_bn'],
        "baseline_2mbps_3g_w": tech_percs['baseline_2mbps_3g_w']['social_cost_bn'],
        "baseline_2mbps_4g_w": tech_percs['baseline_2mbps_4g_w']['social_cost_bn'],
        "baseline_2mbps_5g_w": tech_percs['baseline_2mbps_5g_w']['social_cost_bn'],
        "perc_private_base_5mbps_3g_w":
        tech_costs['baseline_5_5_5_3g_umts_wireless_baseline_baseline_baseline_baseline']['perc_private'],
        "perc_govt_base_5mbps_3g_w":
        tech_costs['baseline_5_5_5_3g_umts_wireless_baseline_baseline_baseline_baseline']['perc_govt'],
        "perc_private_base_5mbps_4g_w":
        tech_costs['baseline_5_5_5_4g_epc_wireless_baseline_baseline_baseline_baseline']['perc_private'],
        "perc_govt_base_5mbps_4g_w":
        tech_costs['baseline_5_5_5_4g_epc_wireless_baseline_baseline_baseline_baseline']['perc_govt'],
        "perc_private_base_5mbps_5g_w":
        tech_costs['baseline_5_5_5_5g_nsa_wireless_baseline_baseline_baseline_baseline']['perc_private'],
        "perc_govt_base_5mbps_5g_w":
        tech_costs['baseline_5_5_5_5g_nsa_wireless_baseline_baseline_baseline_baseline']['perc_govt'],


        "figure_2": os.path.join(IMAGES, iso3, 'private_cost_composition.png'),
        "figure_3": os.path.join(IMAGES, iso3, 'social_costs_by_sharing_strategy.png'),
        "passive_vs_base_4g_5mbps": round(abs(share_percs['baseline_5mbps_passive']['saving_against_baseline'])),
        "passive_vs_base_4g_10mbps": round(abs(share_percs['baseline_10mbps_passive']['saving_against_baseline'])),
        "passive_vs_base_4g_2mbps": round(abs(share_percs['baseline_2mbps_passive']['saving_against_baseline'])),
        "active_vs_base_4g_5mbps": round(abs(share_percs['baseline_5mbps_active']['saving_against_baseline'])),
        "active_vs_base_4g_10mbps": round(abs(share_percs['baseline_10mbps_active']['saving_against_baseline'])),
        "active_vs_base_4g_2mbps": round(abs(share_percs['baseline_2mbps_active']['saving_against_baseline'])),
        "srn_vs_base_4g_5mbps": round(abs(share_percs['baseline_5mbps_srn']['saving_against_baseline'])),
        "srn_vs_base_4g_10mbps": round(abs(share_percs['baseline_10mbps_srn']['saving_against_baseline'])),
        "srn_vs_base_4g_2mbps": round(abs(share_percs['baseline_2mbps_srn']['saving_against_baseline'])),
        "passive_cost_4g_10mbps": share_percs['baseline_10mbps_passive']['social_cost_bn'],
        "active_cost_4g_10mbps": share_percs['baseline_10mbps_active']['social_cost_bn'],
        "srn_cost_4g_10mbps": share_percs['baseline_10mbps_srn']['social_cost_bn'],
        "figure_4": os.path.join(IMAGES, iso3, 'social_costs_by_policy_options.png'),
        "tax_low": int(float(policy_inputs['tax_low'])),
        "tax_baseline": int(float(policy_inputs['tax_baseline'])),
        "tax_high": int(float(policy_inputs['tax_high'])),
        "perc_lowtax": policy_percs['baseline_10mbps_lowtax']['perc_against_baseline'],
        "perc_hightax": policy_percs['baseline_10mbps_hightax']['perc_against_baseline'],
        "lowtax_cost_4g_10mbps": policy_percs['baseline_10mbps_lowtax']['social_cost_bn'],
        "hightax_cost_4g_10mbps": policy_percs['baseline_10mbps_hightax']['social_cost_bn'],
        "baselinetax_cost_4g_10mbps": policy_percs['baseline_10mbps_baseline']['social_cost_bn'],
        "profit_margin": int(float(policy_inputs['profit_margin'])),
        "spectrum_coverage_baseline_usd_mhz_pop": policy_inputs['spectrum_coverage_baseline_usd_mhz_pop'],
        "spectrum_capacity_baseline_usd_mhz_pop": policy_inputs['spectrum_capacity_baseline_usd_mhz_pop'],
        "spectrum_cost_low": int(float(policy_inputs['spectrum_cost_low'])),
        "spectrum_cost_high": int(float(policy_inputs['spectrum_cost_high'])),
        "perc_lowspectrum": policy_percs['baseline_10mbps_lowspectrumfees']['perc_against_baseline'],
        "perc_highspectrum": policy_percs['baseline_10mbps_highspectrumfees']['perc_against_baseline'],
        "lowspectrum_cost_4g_10mbps": policy_percs['baseline_10mbps_lowspectrumfees']['social_cost_bn'],
        "highspectrum_cost_4g_10mbps": policy_percs['baseline_10mbps_highspectrumfees']['social_cost_bn'],

        ###Method note
        "figure_m1": os.path.join(FIGURES, '..', '..', 'clustering', 'figures', 'cluster_panel.png'),
        "figure_m2": os.path.join(FIGURES, '..', '..', 'method', 'figures', 'method_box_diagram.jpg'),
        "figure_m3": os.path.join(IMAGES, iso3, 'demand_graphic.png'),
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
        "confidence": technology_inputs['confidence'][0],
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

        ##Spectrum
        "bands_3G": spectrum_bands['3G']['bands_3G'][0],
        "bandwidth_3G": spectrum_bands['3G']['bandwidth_3G'][0],
        "bands_4G": spectrum_bands['4G']['bands_4G'][0],
        "bandwidth_4G": spectrum_bands['4G']['bandwidth_4G'][0],
        "bands_5G": spectrum_bands['5G']['bands_5G'][0],
        "bandwidth_5G": spectrum_bands['5G']['bandwidth_5G'][0],

        ##Appendix
        "figure_a1": os.path.join(IMAGES, iso3, '{}_by_pop_density.png'.format(iso3)),
        "figure_a2": os.path.join(IMAGES, iso3, 'financial_cost_sq_km_2_mbps.png'),
        "figure_a3": os.path.join(IMAGES, iso3, 'financial_cost_sq_km_5_mbps.png'),
        "figure_a4": os.path.join(IMAGES, iso3, 'financial_cost_sq_km_10_mbps.png'),
        "figure_a5": os.path.join(IMAGES, iso3, 'financial_cost_sq_km_20_mbps.png'),
        "figure_a6": os.path.join(IMAGES, iso3, 'financial_cost_per_user_2_mbps.png'),
        "figure_a7": os.path.join(IMAGES, iso3, 'financial_cost_per_user_5_mbps.png'),
        "figure_a8": os.path.join(IMAGES, iso3, 'financial_cost_per_user_10_mbps.png'),
        "figure_a9": os.path.join(IMAGES, iso3, 'financial_cost_per_user_20_mbps.png'),
    }

    html_out = template.render(template_vars)

    # with open(os.path.join(OUTPUT, "my_new_file.html"), "w", encoding="utf-8") as fh:
    #     fh.write(html_out)

    name = '{} - Quantified Universal Broadband Investment by Country (Qubic).pdf'.format(
        country['preferred_name'])
    path = os.path.join(OUTPUT, name)

    pisa.showLogging()
    convert_html_to_pdf(html_out, path)


def get_sites(iso3):
    """
    Load data.

    """
    output = {}

    path = os.path.join(BASE_PATH, 'intermediate', iso3, 'sites', 'sites.csv')
    data = pd.read_csv(path)

    data = data[['sites_4G', 'total_estimated_sites', 'backhaul_wireless']]
    data = data.sum()

    output['sites_4G'] = data['sites_4G']
    output['total_estimated_sites'] = data['total_estimated_sites']
    output['backhaul_wireless'] = int(round(
        (data['backhaul_wireless'] / data['total_estimated_sites']) *100))

    return output


def get_tech_costs(iso3, rounding):
    """
    Load data.

    """
    output = {}

    filename = 'national_market_cost_results_technology_options.csv'
    path = os.path.join(RESULTS, 'model_results', iso3, filename)
    data = pd.read_csv(path)

    for idx, row in data.iterrows():

        key = '{}_{}'.format(
            row['scenario'].lower(),
            row['strategy'].lower(),
        )

        private_cost_bn = round(row['private_cost'] / 1e9, rounding)
        government_cost_bn = round(row['government_cost'] / 1e9, rounding)
        societal_cost_bn = round(row['societal_cost'] / 1e9, rounding)

        perc_private = int(round((private_cost_bn / societal_cost_bn) * 100, 1))
        if perc_private > 100:
            perc_private = 100

        perc_govt = int(round((government_cost_bn / societal_cost_bn) * 100, 1))
        if perc_govt < 0:
            perc_govt = 0

        output[key] = {
            'perc_private': perc_private,
            'perc_govt': perc_govt,
        }

    return output


def get_tech_percentages(iso3, rounding):
    """
    Load data.

    """
    output = {}

    filename = 'percentages_technologies_{}.csv'.format(iso3)
    path = os.path.join(RESULTS, 'percentages', filename)
    data = pd.read_csv(path)

    for idx, row in data.iterrows():

        key = '{}_{}_{}_{}'.format(
            row['scenario'].lower(),
            row['capacity'].lower().replace(' ', ''),
            row['generation'].lower(),
            row['backhaul'].lower().replace('(','').replace(')',''),
        )

        social_cost_bn = round(row['social_cost'] / 1e9, rounding)
        perc_saving_vs_3g = round(row['perc_saving_vs_3G'], 1)
        w_over_fb = round(row['w_over_fb'], 1)

        if rounding == 0:
            social_cost_bn = int(social_cost_bn)

        output[key] = {
            'social_cost_bn': social_cost_bn,
            'perc_saving_vs_3g': perc_saving_vs_3g,
            'w_over_fb': w_over_fb,
        }

    return output


def get_sharing_data(iso3, rounding):
    """
    Load data.

    """
    output = {}

    filename = 'percentages_sharing_{}.csv'.format(iso3)
    path = os.path.join(RESULTS, 'percentages', filename)
    data = pd.read_csv(path)

    for idx, row in data.iterrows():

        key = '{}_{}_{}'.format(
            row['scenario'].lower(),
            row['capacity'].lower().replace(' ', ''),
            row['strategy_x'].lower(),
        )

        social_cost_bn = round(row['social_cost_x'] / 1e9, rounding)
        if rounding == 0:
            social_cost_bn = int(social_cost_bn)

        output[key] = {
            'social_cost_bn': social_cost_bn,
            'saving_against_baseline': round(row['saving_against_baseline'], 1),
        }

    return output


def get_policy_data(iso3, rounding):
    """
    Load data.

    """
    output = {}

    filename = 'percentages_policy_{}.csv'.format(iso3)
    path = os.path.join(RESULTS, 'percentages', filename)
    data = pd.read_csv(path)

    rounding = rounding + 1

    for idx, row in data.iterrows():

        key = '{}_{}_{}'.format(
            row['scenario'].lower(),
            row['capacity'].lower().replace(' ', ''),
            row['strategy_x'].lower().replace(' ', ''),
        )

        social_cost_bn = round(row['social_cost_x'] / 1e9, rounding)
        if rounding == 0:
            social_cost_bn = int(social_cost_bn)

        output[key] = {
            'social_cost_bn': social_cost_bn,
            'perc_against_baseline': round(row['saving_against_baseline'], 1),
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


def get_policy_inputs(iso3):
    """

    """
    output = {}

    filename = 'parameters_policy_options_*.csv'
    path = os.path.join(RESULTS, 'model_results', iso3, filename)
    files = glob.glob(path)
    latest_file_path = max(files, key=os.path.getctime)

    data = pd.read_csv(latest_file_path)

    for idx, row in data.iterrows():

        output[row['parameter'].lower()] = row['value']

    return output


def get_frequencies(iso3):
    """

    """
    output = {}

    filename = 'parameters_frequencies_technology_options_*.csv'
    path = os.path.join(RESULTS, 'model_results', iso3, filename)
    files = glob.glob(path)
    latest_file_path = max(files, key=os.path.getctime)

    data = pd.read_csv(latest_file_path)

    generations = ['3G', '4G', '5G']

    for generation in generations:

        my_dict = {}

        all_bands = []
        all_bandwidths = []

        for idx, row in data.iterrows():
            if row['generation'] == generation:

                all_bands.append(row['frequency'])
                all_bandwidths.append(row['bandwidth'])

        bands = 'bands_{}'.format(generation)
        bandwidths = 'bandwidth_{}'.format(generation)

        my_dict[bands] = all_bands
        my_dict[bandwidths] = all_bandwidths

        output[generation] = my_dict

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

        if not country['iso3'] == 'COL':
            continue

        print('Reporting for {}'.format(country['iso3']))

        generate_report(country)
