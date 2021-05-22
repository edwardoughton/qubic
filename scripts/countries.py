"""
Country Assessment list

"""

COUNTRY_LIST = [
        {
        'country_name': 'El Salvador',
        'preferred_name': 'El Salvador',
        'iso3': 'SLV',
        'iso2': 'SV',
        'regional_level': 2,
        'region': 'LAC',
        'coverage_4G': 70,
        'pop_density_km2': 500,
        'settlement_size': 500,
        'core_node_size': 2000,
        'subs_growth_low': 2,
        'sp_growth_low_urban': 2,
        'sp_growth_low_rural': 2,
        'subs_growth_baseline': 4,
        'sp_growth_baseline_urban': 4,
        'sp_growth_baseline_rural': 4,
        'subs_growth_high': 6,
        'sp_growth_high_urban': 6,
        'sp_growth_high_rural': 6,
        'phone_ownership_male': 50,
        'phone_ownership_female': 50,
    },
    {
        'country_name': 'Costa Rica',
        'preferred_name': 'Costa Rica',
        'iso3': 'CRI',
        'iso2': 'CR',
        'regional_level': 2,
        'region': 'LAC',
        # 'coverage_4G': 70,
        'pop_density_km2': 100,
        'settlement_size': 200,
        'core_node_size': 2000,
        'subs_growth_low': 2,
        'sp_growth_low_urban': 2,
        'sp_growth_low_rural': 2,
        'subs_growth_baseline': 4,
        'sp_growth_baseline_urban': 4,
        'sp_growth_baseline_rural': 4,
        'subs_growth_high': 6,
        'sp_growth_high_urban': 6,
        'sp_growth_high_rural': 6,
        'phone_ownership_male': 50,
        'phone_ownership_female': 50,
    },
    {
        'country_name': 'Gambia (the)',
        'preferred_name': 'The Gambia',
        'iso3': 'GMB',
        'iso2': 'GM',
        'regional_level': 2,
        'region': 'SSA',
        'coverage_4G': 70,
        'pop_density_km2': 100,
        'settlement_size': 200,
        'core_node_size': 0,
        'subs_growth_low': 2,
        'sp_growth_low_urban': 2,
        'sp_growth_low_rural': 2,
        'subs_growth_baseline': 4,
        'sp_growth_baseline_urban': 4,
        'sp_growth_baseline_rural': 4,
        'subs_growth_high': 6,
        'sp_growth_high_urban': 6,
        'sp_growth_high_rural': 6,
        'phone_ownership_male': 50,
        'phone_ownership_female': 50,
    },
    {
        'country_name': 'Senegal',
        'preferred_name': 'Senegal',
        'iso3': 'SEN',
        'iso2': 'SN',
        'regional_level': 3,
        'region': 'SSA',
        'coverage_4G': 70,
        'pop_density_km2': 100,
        'settlement_size': 200,
        'core_node_size': 2000,
        'subs_growth_low': 2,
        'sp_growth_low_urban': 2,
        'sp_growth_low_rural': 2,
        'subs_growth_baseline': 4,
        'sp_growth_baseline_urban': 4,
        'sp_growth_baseline_rural': 4,
        'subs_growth_high': 6,
        'sp_growth_high_urban': 6,
        'sp_growth_high_rural': 6,
        'phone_ownership_male': 50,
        'phone_ownership_female': 50,
    }
]


COUNTRY_PARAMETERS = {
    'CRI': {
        'luminosity': {
            'high': 5,
            'medium': 1,
        },
        'arpu': {
            'high': 6,
            'medium': 4,
            'low': 2,
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
                    'frequency': 850,
                    'bandwidth': '2x10',
                    # 'status': 'active',
                },
                {
                    'frequency': 2100,
                    'bandwidth': '2x10',
                    # 'status': 'inactive',
                },
            ],
            '4G': [
                {
                    'frequency': 1800,
                    'bandwidth': '2x10',
                    # 'status': 'active',
                },
                {
                    'frequency': 2600,
                    'bandwidth': '2x10',
                    # 'status': 'inactive',
                },
            ],
            '5G': [
                {
                    'frequency': 700,
                    'bandwidth': '2x10',
                    # 'status': 'inactive',
                },
                {
                    'frequency': 3500,
                    'bandwidth': '1x50',
                    # 'status': 'inactive',
                },
            ]
        },
        'financials': {
            'wacc': 9.5, #http://www.waccexpert.com/
            'profit_margin': 20,
            'spectrum_coverage_baseline_usd_mhz_pop': 0.3, #refine
            'spectrum_capacity_baseline_usd_mhz_pop': 0.2,
            'spectrum_cost_low': 25,
            'spectrum_cost_high': 200,
            'tax_low': 10,
            'tax_baseline': 30,
            'tax_high': 45,
            'administration_percentage_of_network_cost': 20,
            },
        },
    'GMB': {
        'luminosity': {
            'high': 5,
            'medium': 1,
        },
        'arpu': {
            'high': 6,
            'medium': 4,
            'low': 2,
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
                    # 'status': 'active',
                },
                {
                    'frequency': 2100,
                    'bandwidth': '2x10',
                    # 'status': 'active',
                },
            ],
            '4G': [
                {
                    'frequency': 800,
                    'bandwidth': '2x10',
                    # 'status': 'active',
                },
                {
                    'frequency': 1800,
                    'bandwidth': '2x10',
                    # 'status': 'inactive',
                },
            ],
            '5G': [
                {
                    'frequency': 700,
                    'bandwidth': '2x10',
                    # 'status': 'inactive',
                },
                {
                    'frequency': 3500,
                    'bandwidth': '1x50',
                    # 'status': 'inactive',
                },
            ]
        },
        'financials': {
            'wacc': 15,
            'profit_margin': 20,
            'spectrum_coverage_baseline_usd_mhz_pop': 0.03,
            'spectrum_capacity_baseline_usd_mhz_pop': 0.02,
            'spectrum_cost_low': 25,
            'spectrum_cost_high': 200,
            'tax_low': 10,
            'tax_baseline': 31,
            'tax_high': 45,
            'administration_percentage_of_network_cost': 20,
            },
        },
    'SLV': {
        'luminosity': {
            'high': 5,
            'medium': 1,
        },
        'arpu': {
            'high': 8,
            'medium': 6,
            'low': 2,
        },
        'networks': {
            'baseline_urban': 3,
            'baseline_suburban': 3,
            'baseline_rural': 3,
            'srn_urban': 3,
            'srn_suburban': 3,
            'srn_rural': 1,
        },
        'frequencies': {
            '3G': [
                {
                    'frequency': 1700,
                    'bandwidth': '2x10',
                    # 'status': 'active',
                },
                {
                    'frequency': 1900,
                    'bandwidth': '2x10',
                    # 'status': 'inactive',
                },
            ],
            '4G': [
                {
                    'frequency': 850,
                    'bandwidth': '2x10',
                    # 'status': 'active',
                },
                {
                    'frequency': 1800,
                    'bandwidth': '2x10',
                    # 'status': 'inactive',
                },
            ],
            '5G': [
                {
                    'frequency': 700,
                    'bandwidth': '2x10',
                    # 'status': 'inactive',
                },
                {
                    'frequency': 3500,
                    'bandwidth': '1x50',
                    # 'status': 'inactive',
                },
            ],
        },
        'financials': {
            'wacc': 15,
            'profit_margin': 10,
            'spectrum_coverage_baseline_usd_mhz_pop': 0.1,
            'spectrum_capacity_baseline_usd_mhz_pop': 0.08,
            'spectrum_cost_low': 25,
            'spectrum_cost_high': 200,
            'tax_low': 10,
            'tax_baseline': 30,
            'tax_high': 40,
            'administration_percentage_of_network_cost': 20,
            },
        },
    'SEN': {
        'luminosity': {
            'high': 5,
            'medium': 1,
        },
        'arpu': {
            'high': 8,
            'medium': 6,
            'low': 2,
        },
        'networks': {
            'baseline_urban': 3,
            'baseline_suburban': 3,
            'baseline_rural': 3,
            'srn_urban': 3,
            'srn_suburban': 3,
            'srn_rural': 1,
        },
        'frequencies': {
            '3G': [
                {
                    'frequency': 1800,
                    'bandwidth': '2x10',
                    # 'status': 'active',
                },
                {
                    'frequency': 2100,
                    'bandwidth': '2x10',
                    # 'status': 'active',
                },
            ],
            '4G': [
                {
                    'frequency': 800,
                    'bandwidth': '2x10',
                    # 'status': 'active',
                },
                {
                    'frequency': 1800,
                    'bandwidth': '2x10',
                    # 'status': 'active',
                },
            ],
            '5G': [
                {
                    'frequency': 700,
                    'bandwidth': '2x10',
                    # 'status': 'inactive',
                },
                {
                    'frequency': 3500,
                    'bandwidth': '1x50',
                    # 'status': 'inactive',
                },
            ],
        },
        'financials': {
            'wacc': 15,
            'profit_margin': 10,
            'spectrum_coverage_baseline_usd_mhz_pop': 0.04,
            'spectrum_capacity_baseline_usd_mhz_pop': 0.03,
            'spectrum_cost_low': 25,
            'spectrum_cost_high': 200,
            'tax_low': 10,
            'tax_baseline': 30,
            'tax_high': 40,
            'administration_percentage_of_network_cost': 20,
            },
        },
    }
