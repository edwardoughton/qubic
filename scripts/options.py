"""
Options consisting of scenarios and strategies.

Country parameters consist of those parameters which are specific
to each country.

Written by Ed Oughton, based on work from the pytal and podis repositories.

April 2021

#strategy is defined based on generation_core_backhaul_sharing_networks_spectrum_tax

generation: technology generation, so 3G or 4G
core: type of core data transport network, eg. evolved packet core (4G)
backhaul: type of backhaul, so fiber or wireless
sharing: the type of infrastructure sharing, active, passive etc..
network: relates to the number of networks, as defined in country parameters
spectrum: type of spectrum strategy, so baseline, high or low
tax: type of taxation strategy, so baseline, high or low
"""

def generate_tech_options():
    """
    Generate technology strategy options.

    """
    output = []

    scenarios = ['low_50_25_5', 'baseline_50_25_5', 'high_50_25_5']
    generation_core_types = ['3G_umts', '4G_epc', '5G_nsa']
    backhaul_types = ['wireless', 'fiber']
    sharing_types = ['baseline']
    networks_types = ['baseline']
    spectrum_types = ['baseline']
    tax_types = ['baseline']

    for scenario in scenarios:
        for generation_core_type in generation_core_types:
                for backhaul in backhaul_types:
                    for sharing in sharing_types:
                        for network in networks_types:
                            for spectrum in spectrum_types:
                                for tax in tax_types:
                                    strategy = '{}_{}_{}_{}_{}_{}'.format(
                                        generation_core_type,
                                        backhaul,
                                        sharing,
                                        network,
                                        spectrum,
                                        tax
                                    )
                                    output.append({
                                        'scenario': scenario,
                                        'strategy': strategy
                                    })

    return output


def generate_business_model_options():
    """
    Generate business model strategy options.

    """
    output = []

    scenarios = ['low_50_25_5', 'baseline_50_25_5', 'high_50_25_5']
    generation_core_types = ['3G_umts', '4G_epc', '5G_nsa']
    backhaul_types = ['wireless', 'fiber']
    sharing_types = ['baseline', 'passive', 'active', 'srn']
    networks_types = ['baseline']
    spectrum_types = ['baseline']
    tax_types = ['baseline']

    for scenario in scenarios:
        for generation_core_type in generation_core_types:
                for backhaul in backhaul_types:
                    for sharing in sharing_types:
                        for network in networks_types:
                            for spectrum in spectrum_types:
                                for tax in tax_types:
                                    strategy = '{}_{}_{}_{}_{}_{}'.format(
                                        generation_core_type,
                                        backhaul,
                                        sharing,
                                        network,
                                        spectrum,
                                        tax
                                    )
                                    output.append({
                                        'scenario': scenario,
                                        'strategy': strategy
                                    })

    return output


def generate_policy_options():
    """
    Generate policy strategy options.

    """
    output = []

    scenarios = ['low_50_25_5', 'baseline_50_25_5', 'high_50_25_5']
    generation_core_types = ['3G_umts', '4G_epc', '5G_nsa']
    backhaul_types = ['wireless', 'fiber']
    sharing_types = ['baseline', 'passive', 'active', 'srn']
    networks_types = ['baseline']
    spectrum_types = ['baseline', 'low', 'high']
    tax_types = ['baseline', 'low', 'high']

    for scenario in scenarios:
        for generation_core_type in generation_core_types:
                for backhaul in backhaul_types:
                    for sharing in sharing_types:
                        for network in networks_types:
                            for spectrum in spectrum_types:
                                for tax in tax_types:
                                    strategy = '{}_{}_{}_{}_{}_{}'.format(
                                        generation_core_type,
                                        backhaul,
                                        sharing,
                                        network,
                                        spectrum,
                                        tax
                                    )
                                    output.append({
                                        'scenario': scenario,
                                        'strategy': strategy
                                    })

    return output


def generate_mixed_options():
    """
    Generate policy strategy options.

    """
    output = []

    scenarios = ['low_50_25_5', 'baseline_50_25_5', 'high_50_25_5']
    generation_core_types = ['3G_umts', '4G_epc', '5G_nsa']
    backhaul_types = ['wireless', 'fiber']
    sharing_types = ['srn']
    networks_types = ['baseline']
    spectrum_types = ['low']
    tax_types = ['low']

    for scenario in scenarios:
        for generation_core_type in generation_core_types:
                for backhaul in backhaul_types:
                    for sharing in sharing_types:
                        for network in networks_types:
                            for spectrum in spectrum_types:
                                for tax in tax_types:
                                    strategy = '{}_{}_{}_{}_{}_{}'.format(
                                        generation_core_type,
                                        backhaul,
                                        sharing,
                                        network,
                                        spectrum,
                                        tax
                                    )
                                    output.append({
                                        'scenario': scenario,
                                        'strategy': strategy
                                    })

    return output


OPTIONS = {
    'technology_options': generate_tech_options(),
    'business_model_options': generate_business_model_options(),
    'policy_options': generate_policy_options(),
    'mixed_options': generate_mixed_options(),
}


COUNTRY_PARAMETERS = {
    'GMB': {
        'luminosity': {
            'high': 20,
            'medium': 15,
        },
        'arpu': {
            'high': 3.5,
            'medium': 2.5,
            'low': 1,
        },
        'networks': {
            'baseline_urban': 3,
            'baseline_suburban': 3,
            'baseline_rural': 3,
            'shared_urban': 3,
            'shared_suburban': 3,
            'shared_rural': 1,
        },
        'frequencies': {
            '3G': [
                {
                    'frequency': 900,
                    'bandwidth': '2x10',
                    'status': 'active',
                },
                {
                    'frequency': 2100,
                    'bandwidth': '2x10',
                    'status': 'active',
                },
            ],
            '4G': [
                {
                    'frequency': 800,
                    'bandwidth': '2x10',
                    'status': 'active',
                },
                {
                    'frequency': 1800,
                    'bandwidth': '2x10',
                    'status': 'inactive',
                },
            ],
            '5G': [
                {
                    'frequency': 700,
                    'bandwidth': '2x10',
                    'status': 'inactive',
                },
                {
                    'frequency': 3500,
                    'bandwidth': '1x50',
                    'status': 'inactive',
                },
            ]
        },
        'financials': {
            'wacc': 15,
            'profit_margin': 20,
            'spectrum_coverage_baseline_usd_mhz_pop': 0.02,
            'spectrum_capacity_baseline_usd_mhz_pop': 0.01,
            'spectrum_cost_low': 25,
            'spectrum_cost_high': 100,
            'tax_low': 10,
            'tax_baseline': 30,
            'tax_high': 40,
            'administration_percentage_of_network_cost': 20,
            },
        },
    }


COSTS = {
    #all costs in $USD
    'equipment': 40000,
    'site_build': 30000,
    'installation': 30000,
    'operation_and_maintenance': 7400,
    'power': 3000,
    'site_rental_urban': 10000,
    'site_rental_suburban': 5000,
    'site_rental_rural': 3000,
    'fiber_urban_m': 25,
    'fiber_suburban_m': 15,
    'fiber_rural_m': 10,
    'wireless_small': 15000,
    'wireless_medium': 20000,
    'wireless_large': 45000,
    'core_node': 500000,
    'core_edge': 25,
    'regional_node': 200000,
    'regional_edge': 25,
}

GLOBAL_PARAMETERS = {
    'overbooking_factor': 20,
    'return_period': 10,
    'discount_rate': 5,
    'opex_percentage_of_capex': 10,
    'confidence': [50],#[5, 50, 95]
    'tdd_dl_to_ul': '80:20',
    }
