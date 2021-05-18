"""
Generate country reports.

Written by Ed Oughton.

May 2021

"""
import os
import configparser
# import numpy as np
# import pandas as pd

from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa             # import python module
# from weasyprint import HTML

from countries import COUNTRY_LIST

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

RESULTS = os.path.join(BASE_PATH, '..', 'results', 'percentages')
OUTPUT = os.path.join(BASE_PATH, '..', 'reports', 'countries')


# Utility function
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

        iso3 = country['iso3']

        if not iso3 == 'GMB':
            continue

        path = os.path.join(BASE_PATH, '..', 'reports', 'templates')
        env = Environment(loader=FileSystemLoader(path))

        template = env.get_template('qubic_template.html')

        template_vars = {
            "country_name" : country['country_name'],
            "country": iso3,
            "figure": 'social_costs_by_strategy.png'
        }

        html_out = template.render(template_vars)

        path = os.path.join(OUTPUT, '{}.pdf'.format(iso3))

        pisa.showLogging()
        convert_html_to_pdf(html_out, path)
