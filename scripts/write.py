"""
Functions for writing to .csv

September 2020

Written by Ed Oughton

"""
import os
import pandas as pd
import datetime

def define_deciles(regions):
    """
    Allocate deciles to regions.

    """
    regions = regions.sort_values(by='population_km2', ascending=True)

    regions['decile'] = regions.groupby([
        'GID_0',
        'scenario',
        'strategy',
        'confidence'
    ], as_index=True).population_km2.apply( #cost_per_sp_user
        pd.qcut, q=11, precision=0,
        labels=[100,90,80,70,60,50,40,30,20,10,0],
        duplicates='drop') #   [0,10,20,30,40,50,60,70,80,90,100]

    return regions


def write_demand(regional_annual_demand, folder):
    """
    Write all annual demand results.

    """
    print('Writing annual_mno_demand')
    regional_annual_demand = pd.DataFrame(regional_annual_demand)
    regional_annual_demand = regional_annual_demand.loc[
        regional_annual_demand['scenario'] == 'baseline_10_10_10']
    # regional_annual_mno_demand = regional_annual_demand[[
    #     'GID_0', 'GID_id', 'scenario', 'strategy',
    #     'confidence', 'year', 'population', 'area_km2', 'population_km2',
    #     'geotype', 'arpu_discounted_monthly',
    #     'penetration', 'population_with_phones','phones_on_network',
    #     'smartphone_penetration', 'smartphones_on_network', 'revenue'
    # ]]
    # filename = 'regional_annual_mno_demand.csv'
    # path = os.path.join(folder, filename)
    # regional_annual_mno_demand.to_csv(path, index=False)

    print('Writing annual_market_demand')
    regional_annual_market_demand = regional_annual_demand[[
        'GID_0', 'GID_id', 'scenario', 'strategy',
        'confidence', 'year', 'population',
        # 'population_f_over_10', 'population_m_over_10',
        'area_km2', 'population_km2',
        'geotype', 'arpu_discounted_monthly',
        # 'penetration_female',
        # 'penetration_male',
        'penetration',
        'population_with_phones',
        # 'population_with_phones_f_over_10',
        # 'population_with_phones_m_over_10',
        'smartphone_penetration',
        'population_with_smartphones',
        # 'population_with_smartphones_f_over_10',
        # 'population_with_smartphones_m_over_10',
        'revenue'
    ]]
    filename = 'regional_annual_market_demand.csv'
    path = os.path.join(folder, filename)
    regional_annual_market_demand.to_csv(path, index=False)


def write_results(regional_results, folder, metric):
    """
    Write all results.

    """
    print('Writing national MNO results')
    national_results = pd.DataFrame(regional_results)
    national_results = national_results[[
        'GID_0', 'scenario', 'strategy', 'confidence', 'population_total', 'area_km2',
        'phones_on_network', 'smartphones_on_network', 'total_estimated_sites',
        'existing_mno_sites', 'upgraded_mno_sites', 'new_mno_sites',
        'total_mno_revenue', 'total_mno_cost',
    ]]
    national_results = national_results.drop_duplicates()
    national_results = national_results.groupby([
        'GID_0', 'scenario', 'strategy', 'confidence'], as_index=True).sum()
    national_results['cost_per_network_user'] = (
        national_results['total_mno_cost'] / national_results['phones_on_network'])
    national_results['cost_per_smartphone_user'] = (
        national_results['total_mno_cost'] / national_results['smartphones_on_network'])
    path = os.path.join(folder,'national_mno_results_{}.csv'.format(metric))
    national_results.to_csv(path, index=True)


    print('Writing national cost composition results')
    national_cost_results = pd.DataFrame(regional_results)
    national_cost_results = national_cost_results[[
        'GID_0', 'scenario', 'strategy', 'confidence', 'population_total',
        'phones_on_network', 'smartphones_on_network', 'total_mno_revenue',
        'ran', 'backhaul_fronthaul', 'civils', 'core_network',
        'administration', 'spectrum_cost', 'tax', 'profit_margin',
        'total_mno_cost', 'available_cross_subsidy', 'deficit',
        'used_cross_subsidy', 'required_state_subsidy',
    ]]
    national_cost_results = national_cost_results.drop_duplicates()
    national_cost_results = national_cost_results.groupby([
        'GID_0', 'scenario', 'strategy', 'confidence'], as_index=True).sum()
    national_cost_results['cost_per_network_user'] = (
        national_cost_results['total_mno_cost'] /
        national_cost_results['phones_on_network'])
    national_cost_results['cost_per_smartphone_user'] = (
        national_cost_results['total_mno_cost'] /
        national_cost_results['smartphones_on_network'])
    #Calculate private, govt and societal costs
    national_cost_results['private_cost'] = national_cost_results['total_mno_cost']
    national_cost_results['government_cost'] = (
        national_cost_results['required_state_subsidy'] -
            (national_cost_results['spectrum_cost'] + national_cost_results['tax']))
    national_cost_results['societal_cost'] = (
        national_cost_results['private_cost'] + national_cost_results['government_cost'])
    path = os.path.join(folder,'national_mno_cost_results_{}.csv'.format(metric))
    national_cost_results.to_csv(path, index=True)


    print('Writing general decile results')
    decile_results = pd.DataFrame(regional_results)
    decile_results = define_deciles(decile_results)
    decile_results = decile_results[[
        'GID_0', 'scenario', 'strategy', 'decile', 'confidence',
        'population_total', 'area_km2', 'phones_on_network',
        'smartphones_on_network', 'total_estimated_sites',
        'existing_mno_sites', 'upgraded_mno_sites', 'new_mno_sites',
        'total_mno_revenue', 'total_mno_cost',
    ]]
    decile_results = decile_results.drop_duplicates()
    decile_results = decile_results.groupby([
        'GID_0', 'scenario', 'strategy', 'confidence', 'decile'], as_index=True).sum()
    decile_results['population_km2'] = (
        decile_results['population_total'] / decile_results['area_km2'])
    decile_results['phone_density_on_network_km2'] = (
        decile_results['phones_on_network'] / decile_results['area_km2'])
    decile_results['sp_density_on_network_km2'] = (
        decile_results['smartphones_on_network'] / decile_results['area_km2'])
    decile_results['total_estimated_sites_km2'] = (
        decile_results['total_estimated_sites'] / decile_results['area_km2'])
    decile_results['existing_mno_sites_km2'] = (
        decile_results['existing_mno_sites'] / decile_results['area_km2'])
    decile_results['cost_per_network_user'] = (
        decile_results['total_mno_cost'] / decile_results['phones_on_network'])
    decile_results['cost_per_smartphone_user'] = (
        decile_results['total_mno_cost'] / decile_results['smartphones_on_network'])
    path = os.path.join(folder,'decile_mno_results_{}.csv'.format(metric))
    decile_results.to_csv(path, index=True)


    print('Writing cost decile results')
    decile_cost_results = pd.DataFrame(regional_results)
    decile_cost_results = define_deciles(decile_cost_results)
    decile_cost_results = decile_cost_results[[
        'GID_0', 'scenario', 'strategy', 'decile', 'confidence',
        'population_total', 'area_km2', 'phones_on_network', 'smartphones_on_network',
        'total_mno_revenue', 'ran', 'backhaul_fronthaul', 'civils', 'core_network',
        'administration', 'spectrum_cost', 'tax', 'profit_margin', 'total_mno_cost',
        'available_cross_subsidy', 'deficit', 'used_cross_subsidy',
        'required_state_subsidy',
    ]]
    decile_cost_results = decile_cost_results.drop_duplicates()
    decile_cost_results = decile_cost_results.groupby([
        'GID_0', 'scenario', 'strategy', 'confidence', 'decile'], as_index=True).sum()
    decile_cost_results['cost_per_network_user'] = (
        decile_cost_results['total_mno_cost'] / decile_cost_results['phones_on_network'])
    decile_cost_results['cost_per_smartphone_user'] = (
        decile_cost_results['total_mno_cost'] / decile_cost_results['smartphones_on_network'])
    path = os.path.join(folder,'decile_mno_cost_results_{}.csv'.format(metric))
    decile_cost_results.to_csv(path, index=True)


    print('Writing regional results')
    regional_mno_results = pd.DataFrame(regional_results)
    regional_mno_results = define_deciles(regional_mno_results)
    regional_mno_results = regional_mno_results[[
        'GID_0', 'GID_id', 'scenario', 'strategy', 'decile',
        'confidence', 'population_total', 'area_km2',
        'phones_on_network', 'smartphones_on_network',
        'total_estimated_sites', 'existing_mno_sites',
        'upgraded_mno_sites', 'new_mno_sites',
        'total_mno_revenue', 'total_mno_cost',
    ]]
    regional_mno_results = regional_mno_results.drop_duplicates()
    regional_mno_results['cost_per_network_user'] = (
        regional_mno_results['total_mno_cost'] / regional_mno_results['phones_on_network'])
    regional_mno_results['cost_per_smartphone_user'] = (
        regional_mno_results['total_mno_cost'] / regional_mno_results['smartphones_on_network'])
    path = os.path.join(folder,'regional_mno_results_{}.csv'.format(metric))
    regional_mno_results.to_csv(path, index=True)


    print('Writing national market results')
    national_results = pd.DataFrame(regional_results)
    national_results = national_results[[
        'GID_0', 'scenario', 'strategy', 'confidence',
        'population_total', 'area_km2',
        'total_phones', 'total_smartphones',
        'total_estimated_sites',
        'total_upgraded_sites',
        'total_new_sites',
        'total_market_revenue', 'total_market_cost',
        'total_spectrum_cost', 'total_tax',
        'total_required_state_subsidy',
    ]]
    national_results = national_results.drop_duplicates()
    national_results = national_results.groupby([
        'GID_0', 'scenario', 'strategy', 'confidence'], as_index=True).sum()
    national_results['cost_per_network_user'] = (
        national_results['total_market_cost'] / national_results['total_phones'])
    national_results['cost_per_smartphone_user'] = (
        national_results['total_market_cost'] / national_results['total_smartphones'])
    national_results['private_cost'] = (
        national_results['total_market_cost'])
    national_results['government_cost'] = (
        national_results['total_required_state_subsidy'] -
            (national_results['total_spectrum_cost'] + national_results['total_tax']))
    national_results['social_cost'] = (
        national_results['private_cost'] + national_results['government_cost'])
    path = os.path.join(folder,'national_market_results_{}.csv'.format(metric))
    national_results.to_csv(path, index=True)


    #=cost / market share * 100
    print('Writing national market cost composition results')
    national_cost_results = pd.DataFrame(regional_results)
    national_cost_results = national_cost_results[[
        'GID_0', 'scenario', 'strategy', 'confidence', 'population_total',
        'total_phones', 'total_smartphones',
        'total_market_revenue', 'total_ran', 'total_backhaul_fronthaul',
        'total_civils', 'total_core_network',
        'total_administration', 'total_spectrum_cost',
        'total_tax', 'total_profit_margin',
        'total_market_cost', 'total_available_cross_subsidy',
        'total_deficit', 'total_used_cross_subsidy',
        'total_required_state_subsidy',
    ]]
    national_cost_results = national_cost_results.drop_duplicates()
    national_cost_results = national_cost_results.groupby([
        'GID_0', 'scenario', 'strategy', 'confidence'], as_index=True).sum()
    national_cost_results['cost_per_network_user'] = (
        national_cost_results['total_market_cost'] / national_cost_results['total_phones'])
    national_cost_results['cost_per_smartphone_user'] = (
        national_cost_results['total_market_cost'] / national_cost_results['total_smartphones'])
    #Calculate private, govt and societal costs
    national_cost_results['private_cost'] = (
        national_cost_results['total_market_cost'])
    national_cost_results['government_cost'] = (
        national_cost_results['total_required_state_subsidy'] -
            (national_cost_results['total_spectrum_cost'] + national_cost_results['total_tax']))
    national_cost_results['societal_cost'] = (
        national_cost_results['private_cost'] + national_cost_results['government_cost'])
    path = os.path.join(folder,'national_market_cost_results_{}.csv'.format(metric))
    national_cost_results.to_csv(path, index=True)


    print('Writing general decile results')
    decile_results = pd.DataFrame(regional_results)
    decile_results = define_deciles(decile_results)
    decile_results = decile_results[[
        'GID_0', 'scenario', 'strategy', 'decile', 'confidence',
        'population_total', 'area_km2', 'total_phones', 'total_smartphones',
        'total_market_revenue', 'total_market_cost',
    ]]
    decile_results = decile_results.drop_duplicates()
    decile_results = decile_results.groupby([
        'GID_0', 'scenario', 'strategy', 'confidence', 'decile'], as_index=True).sum()
    decile_results['population_km2'] = (
        decile_results['population_total'] / decile_results['area_km2'])
    decile_results['cost_per_network_user'] = (
        decile_results['total_market_cost'] / decile_results['total_phones'])
    decile_results['cost_per_smartphone_user'] = (
        decile_results['total_market_cost'] / decile_results['total_smartphones'])
    path = os.path.join(folder,'decile_market_results_{}.csv'.format(metric))
    decile_results.to_csv(path, index=True)


    print('Writing cost decile results')
    decile_cost_results = pd.DataFrame(regional_results)
    decile_cost_results = define_deciles(decile_cost_results)
    decile_cost_results = decile_cost_results[[
        'GID_0', 'scenario', 'strategy', 'decile', 'confidence',
        'population_total', 'area_km2', 'total_phones', 'total_smartphones',
        'total_market_revenue', 'total_ran', 'total_backhaul_fronthaul',
        'total_civils', 'total_core_network',
        'total_administration', 'total_spectrum_cost', 'total_tax',
        'total_profit_margin', 'total_market_cost',
        'total_available_cross_subsidy', 'total_deficit',
        'total_used_cross_subsidy', 'total_required_state_subsidy'
    ]]
    decile_cost_results = decile_cost_results.drop_duplicates()
    decile_cost_results = decile_cost_results.groupby([
        'GID_0', 'scenario', 'strategy', 'confidence', 'decile'], as_index=True).sum()
    decile_cost_results['cost_per_network_user'] = (
        decile_cost_results['total_market_cost'] /
        decile_cost_results['total_phones'])
    decile_cost_results['cost_per_smartphone_user'] = (
        decile_cost_results['total_market_cost'] /
        decile_cost_results['total_smartphones'])
    path = os.path.join(folder,'decile_market_cost_results_{}.csv'.format(metric))
    decile_cost_results.to_csv(path, index=True)


    print('Writing regional results')
    regional_market_results = pd.DataFrame(regional_results)
    regional_market_results = define_deciles(regional_market_results)
    regional_market_results = regional_market_results[[
        'GID_0', 'GID_id', 'scenario', 'strategy', 'decile', 'geotype',
        'confidence', 'population_total', 'area_km2',
        'total_phones', 'total_smartphones',
        'total_upgraded_sites','total_new_sites',
        'total_required_state_subsidy', 'total_spectrum_cost',
        'total_tax', 'total_market_revenue', 'total_market_cost',
    ]]
    regional_market_results = regional_market_results.drop_duplicates()

    regional_market_results['total_private_cost'] = regional_market_results['total_market_cost']
    regional_market_results['total_government_cost'] = (
        regional_market_results['total_required_state_subsidy'] -
            (regional_market_results['total_spectrum_cost'] +
            regional_market_results['total_tax']))
    regional_market_results['total_societal_cost'] = (
        regional_market_results['total_private_cost'] +
        regional_market_results['total_government_cost'])

    regional_market_results['private_cost_per_network_user'] = (
        regional_market_results['total_private_cost'] /
        regional_market_results['total_phones'])
    regional_market_results['government_cost_per_network_user'] = (
        regional_market_results['total_government_cost'] /
        regional_market_results['total_phones'])
    regional_market_results['societal_cost_per_network_user'] = (
        regional_market_results['total_societal_cost'] /
        regional_market_results['total_phones'])

    regional_market_results['private_cost_per_smartphone_user'] = (
        regional_market_results['total_private_cost'] /
        regional_market_results['total_smartphones'])
    regional_market_results['government_cost_per_smartphone_user'] = (
        regional_market_results['total_government_cost'] /
        regional_market_results['total_smartphones'])
    regional_market_results['societal_cost_per_network_user'] = (
        regional_market_results['total_societal_cost'] /
        regional_market_results['total_smartphones'])

    path = os.path.join(folder,'regional_market_results_{}.csv'.format(metric))
    regional_market_results.to_csv(path, index=True)


def write_inputs(folder, country, country_parameters, global_parameters,
    costs, decision_option):
    """
    Write model inputs.

    """
    country_info = pd.DataFrame(country.items(),
        columns=['parameter', 'value'])
    country_info['source'] = 'country_info'

    country_params = pd.DataFrame(
        country_parameters['financials'].items(),
        columns=['parameter', 'value'])
    country_params['source'] = 'country_parameters'

    global_parameters = pd.DataFrame(global_parameters.items(),
        columns=['parameter', 'value'])
    global_parameters['source'] = 'global_parameters'

    costs = pd.DataFrame(costs.items(),
        columns=['parameter', 'value'])
    costs['source'] = 'costs'

    parameters = country_info.append(country_params)
    parameters = parameters.append(global_parameters)
    parameters = parameters.append(costs)
    parameters = parameters[['source', 'parameter', 'value']]

    timenow = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    filename = 'parameters_{}_{}.csv'.format(decision_option, timenow)
    path = os.path.join(folder, filename)
    parameters.to_csv(path, index=False)

    ###write out spectrum frequencies
    frequencies = country_parameters['frequencies']
    generations = ['3G', '4G', '5G']
    all_frequencies = []
    for generation in generations:
        for key, item in frequencies.items():
            if generation == key:
                all_frequencies.append({
                    'generation': generation,
                    'frequency': item[0]['frequency'],
                    'bandwidth': item[0]['bandwidth'],
                })
    frequency_lut = pd.DataFrame(all_frequencies)

    timenow = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    filename = 'parameters_frequencies_{}_{}.csv'.format(decision_option, timenow)
    path = os.path.join(folder, filename)
    frequency_lut.to_csv(path, index=False)
