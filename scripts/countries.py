"""
Country Assessment list

"""

COUNTRY_LIST = [
    {
        'country_name': 'Gambia (the)',
        'iso3': 'GMB',
        'iso2': 'GM',
        'regional_level': 2,
        'region': 'Africa',
        'coverage_4G': 70,
        'pop_density_km2': 100,
        'settlement_size': 200,
        'subs_growth_low': 2,
        'subs_growth_baseline': 3,
        'subs_growth_high': 4,
        'sp_growth_low_urban': 2,
        'sp_growth_baseline_urban': 3,
        'sp_growth_high_urban': 4,
        'sp_growth_low_rural': 2,
        'sp_growth_baseline_rural': 3,
        'sp_growth_high_rural': 4,
        'phone_ownership_male': 54,
        'phone_ownership_female': 46,
    }
]


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
            'spectrum_cost_high': 200,
            'tax_low': 10,
            'tax_baseline': 31,
            'tax_high': 45,
            'administration_percentage_of_network_cost': 20,
            },
        },
    }
