###VISUALISE MODEL OUTPUTS###
# install.packages('tidyverse')
library(tidyverse)
# install.packages('ggpubr')
library(ggpubr)

my_list = list(
  c("AFG", 1, -.3, 1, -.4, 2, -.3),
  c("AGO", 1, -.3, 1, -.4, 2, -.3),
  c("BGD", 0, -.2, 0, -.5, 1, -.42),
  c("BTN", 1, -.3, 1, -.4, 2, -.3),
  c("CMR", 0, -.2, 0, -.5, 1, -.42),
  c("CRI", 1, -.3, 1, -.4, 2, -.3),
  c("EGY", 0, -.2, 0, -.7, 1, -.42),
  c("SLV", 1, -.3, 1, -.7, 1, -.4),
  c("GMB", 2, -.2, 2, -.5, 2, -.42),
  c("HND", 2, -.2, 2, -.5, 2, -.42),
  c("IND", 1, -.3, 1, -.4, 2, -.3),
  c("KEN", 0, -.2, 0, -.6, 1, -.42),
  c("LKA", 1, -.3, 1, -.4, 2, -.3),
  c("MAR", 0, -.2, 0, -.7, 2, -.42),
  c("MDG", 0, -.2, 0, -.7, 2, -.42),
  c("MDV", 2, -.2, 2, -.5, 2, -.42),
  c("MOZ", 2, -.2, 2, -.5, 2, -.42),
  c("MWI", 1, -.2, 1, -.5, 1, -.42),
  c("NPL", 1, -.2, 1, -.5, 1, -.42),
  c("NGA", 1, -.2, 1, -.5, 1, -.42),
  c("PAK", 1, -.2, 1, -.5, 1, -.42),
  c("SEN", 0, -.2, 1, -.7, 1, -.42)
)

for(i in 1:length(my_list)) {
  print(i)
  iso3 = my_list[[i]][1]
  decimal_places_a = as.numeric(my_list[[i]][2])
  hjust_a = as.numeric(my_list[[i]][3])
  decimal_places_b = as.numeric(my_list[[i]][4])
  hjust_b = as.numeric(my_list[[i]][5])
  decimal_places_c = as.numeric(my_list[[i]][6])
  hjust_c = as.numeric(my_list[[i]][7])
  print(iso3)

  # iso3 = 'CRI'
  # decimal_places_a = 2
  # hjust_a = -.2
  # decimal_places_b = 2
  # hjust_b = -.5
  # decimal_places_c = 2
  # hjust_c = -.42
  # print(iso3)
  
  folder <- dirname(rstudioapi::getSourceEditorContext()$path)
  
  filename = 'national_market_cost_results_technology_options.csv'
  data <- read.csv(file.path(folder, '..', 'results', 'model_results', iso3, filename))
  
  names(data)[names(data) == 'GID_0'] <- 'country'
  
  data$scenario_adopt[grep("low", data$scenario)] = 'Low (2% Adoption Growth)'
  data$scenario_adopt[grep("baseline", data$scenario)] = 'Baseline (4% Adoption Growth)'
  data$scenario_adopt[grep("high", data$scenario)] = 'High (6% Adoption Growth)'
  
  data$scenario_capacity = ''
  data$scenario_capacity[grep("2_2_2", data$scenario)] = '~2 Mbps Per User'
  data$scenario_capacity[grep("5_5_5", data$scenario)] = '~5 Mbps Per User'
  data$scenario_capacity[grep("10_10_10", data$scenario)] = '~10 Mbps Per User'
  # data$scenario_capacity[grep("20_20_20", data$scenario)] = '~20 Mbps Per User'
  
  data$strategy_short = ''
  data$strategy_short[grep("3G_umts_fiber", data$strategy)] = '3G (F)'
  data$strategy_short[grep("3G_umts_wireless", data$strategy)] = '3G (W)'
  data$strategy_short[grep("4G_epc_fiber", data$strategy)] = '4G (F)'
  data$strategy_short[grep("4G_epc_wireless", data$strategy)] = '4G (W)'
  data$strategy_short[grep("5G_nsa_fiber", data$strategy)] = '5G (F)'
  data$strategy_short[grep("5G_nsa_wireless", data$strategy)] = '5G (W)'
  
  data$strategy_short = factor(data$strategy_short, levels=c(
                                       "3G (F)",
                                       "4G (F)",
                                       '5G (F)',
                                       "3G (W)",
                                       "4G (W)",
                                       '5G (W)'
                                       ))
  
  data$scenario_capacity = factor(data$scenario_capacity, 
                                  levels=c("~2 Mbps Per User",
                                           "~5 Mbps Per User",
                                           "~10 Mbps Per User"#,
                                           # "~20 Mbps Per User"
                                           ))
  
  data = data[complete.cases(data), ]
  
  data$scenario_adopt = factor(data$scenario_adopt,
                               levels=c("Low (2% Adoption Growth)",
                                        "Baseline (4% Adoption Growth)",
                                        "High (6% Adoption Growth)"))
  
  data <- data[(data$confidence == 50),]
  
  data <- select(data, scenario_adopt, scenario_capacity, strategy_short,
                 cost_per_network_user, cost_per_smartphone_user,
                 private_cost, government_cost, societal_cost)
  
  totals <- data %>%
    group_by(scenario_adopt, scenario_capacity, strategy_short) %>%
    summarize(social_cost = round(
      (societal_cost)/1e9, decimal_places_a))
  
  min_value = min(round(data$societal_cost/ 1e9,2))
  max_value = max(round(data$societal_cost/ 1e9,2))
  min_value[min_value > 0] = 0
  
  colnames(data)[colnames(data) == 'private_cost'] <- 'Private Cost ($USD)'
  colnames(data)[colnames(data) == 'government_cost'] <- 'Government Cost ($USD)'
  colnames(data)[colnames(data) == 'societal_cost'] <- 'Social Cost ($USD)'
  
  data <- data %>% gather(key="Cost_Type", value = "value",
                          'Private Cost ($USD)',
                          'Government Cost ($USD)',
  )
  
  data$value = round(data$value/1e9, 3)
  
  vis1 = ggplot(data, aes(y=value, x=strategy_short, fill=Cost_Type)) +
  geom_bar(position="stack", stat="identity") +
  geom_text(aes(strategy_short, social_cost, label = social_cost, fill = NULL),
            size = 2.5, data = totals, hjust=hjust_a) +
  coord_flip() +
  scale_fill_manual(values=c("#E1BE6A", "#40B0A6"), name=NULL) +
  theme(legend.position = "bottom",
        axis.text.x = element_text(angle = 45, hjust=1)) +
  labs(title = "NPV of the Social Cost by Technology (2020-2030)",
       colour=NULL,
       subtitle = "The Private Cost is invested by operators. The Government Cost is invested by Government.",
       x = NULL, y = "Social Cost (Billions $USD)") +
  scale_y_continuous(expand = c(0, 0), limits = c(0, max_value+(max_value/6))) +
  theme(panel.spacing = unit(0.6, "lines")) +
  guides(fill=guide_legend(ncol=3, reverse = TRUE)) +
  facet_grid(scenario_capacity~scenario_adopt)
  
  dir.create(file.path(folder, 'figures', iso3), showWarnings = FALSE)
  path = file.path(folder, 'figures', iso3, 'social_costs_by_strategy.png')
  ggsave(path, plot = last_plot(), units="in", width=8, height=7, dpi=300)
  dir.create(file.path(folder, '..', 'reports', 'images', iso3), showWarnings = FALSE)
  path = file.path(folder, '..', 'reports', 'images', iso3, 'social_costs_by_strategy.png')
  ggsave(path, plot = last_plot(), units="in", width=8, height=7, dpi=300)

  ################################################################################
  folder <- dirname(rstudioapi::getSourceEditorContext()$path)

  filename = 'national_market_cost_results_business_model_options.csv'
  data <- read.csv(file.path(folder, '..', 'results', 'model_results', iso3, filename))

  names(data)[names(data) == 'GID_0'] <- 'country'

  data$scenario_adopt[grep("low", data$scenario)] = 'Low (2% Adoption Growth)'
  data$scenario_adopt[grep("baseline", data$scenario)] = 'Baseline (4% Adoption Growth)'
  data$scenario_adopt[grep("high", data$scenario)] = 'High (6% Adoption Growth)'

  data$scenario_capacity = ''
  data$scenario_capacity[grep("2_2_2", data$scenario)] = '~2 Mbps Per User'
  data$scenario_capacity[grep("5_5_5", data$scenario)] = '~5 Mbps Per User'
  data$scenario_capacity[grep("10_10_10", data$scenario)] = '~10 Mbps Per User'
  # data$scenario_capacity[grep("20_20_20", data$scenario)] = '~20 Mbps Per User'

  # data = data[!grepl(c("low_2_2_2"), data$scenario),]
  # data = data[!grepl(c("baseline_2_2_2"), data$scenario),]
  # data = data[!grepl(c("high_2_2_2"), data$scenario),]
  data = data[!grepl(c("low_20_20_20"), data$scenario),]
  data = data[!grepl(c("baseline_20_20_20"), data$scenario),]
  data = data[!grepl(c("high_20_20_20"), data$scenario),]

  data$strategy_short = ''
  data$strategy_short[grep("4G_epc_wireless", data$strategy)] = '4G (W)'

  data = data %>% filter(data$strategy_short == '4G (W)')

  data$strategy = factor(data$strategy, levels=c(
    "4G_epc_wireless_active_baseline_baseline_baseline",
    "4G_epc_wireless_passive_baseline_baseline_baseline",
    "4G_epc_wireless_srn_baseline_baseline_baseline",
    "4G_epc_wireless_baseline_baseline_baseline_baseline"
  ),
  labels=c(
    "Active",
    "Passive",
    "SRN",
    "Baseline"
  ))

  data$scenario_capacity = factor(data$scenario_capacity,
                                  levels=c("~2 Mbps Per User",
                                           "~5 Mbps Per User",
                                           "~10 Mbps Per User"#,
                                           # "~20 Mbps Per User"
                                  ))

  data$scenario_adopt = factor(data$scenario_adopt,
                               levels=c("Low (2% Adoption Growth)",
                                        "Baseline (4% Adoption Growth)",
                                        "High (6% Adoption Growth)"))

  data <- data[(data$confidence == 50),]

  data <- select(data, scenario_adopt, scenario_capacity, strategy,
                 cost_per_network_user, cost_per_smartphone_user,
                 private_cost, government_cost, societal_cost)

  totals <- data %>%
    group_by(scenario_adopt, scenario_capacity, strategy) %>%
    summarize(social_cost = round(
      (societal_cost)/1e9, decimal_places_b))

  min_value = min(round(data$societal_cost/ 1e9,2))
  max_value = max(round(data$societal_cost/ 1e9,2))
  min_value[min_value > 0] = 0

  data$social_cost = data$private_cost + data$government_cost
  # write.csv(data, file.path(folder, 'business_model_percentages.csv'))

  colnames(data)[colnames(data) == 'private_cost'] <- 'Private Cost ($USD)'
  colnames(data)[colnames(data) == 'government_cost'] <- 'Government Cost ($USD)'
  colnames(data)[colnames(data) == 'societal_cost'] <- 'Social Cost ($USD)'

  data <- data %>% gather(key="Cost_Type", value = "value",
                          'Private Cost ($USD)',
                          'Government Cost ($USD)',
  )

  data$value = round(data$value/1e9, 3)

  vis2 = ggplot(data, aes(y=value, x=strategy, fill=Cost_Type)) +
    geom_bar(position="stack", stat="identity") +
    geom_text(aes(strategy, social_cost, label = social_cost, fill = NULL),
              size = 2.5, data = totals, hjust=hjust_b) +
    coord_flip() +
    scale_fill_manual(values=c("#E1BE6A", "#40B0A6"), name=NULL) +
    theme(legend.position = "bottom",
          axis.text.x = element_text(angle = 45, hjust=1)) +
    labs(title = "NPV of the Social Cost for Infrastructure Sharing Strategies using 4G (W) (2020-2030)",
         colour=NULL,
         subtitle = "The Private Cost is invested by operators. The Government Cost is invested by Government.",
         x = NULL, y = "Social Cost (Billions $USD)") +
    scale_y_continuous(expand = c(0, 0), limits = c(-min_value, max_value+(max_value/6))) +
    theme(panel.spacing = unit(0.6, "lines")) +
    guides(fill=guide_legend(ncol=3, reverse = TRUE)) +
    facet_grid(scenario_capacity~scenario_adopt)

  path = file.path(folder, 'figures', iso3, 'social_costs_by_sharing_strategy.png')
  ggsave(path, plot = last_plot(), units="in", width=8, height=7, dpi=300)
  path = file.path(folder, '..', 'reports', 'images', iso3, 'social_costs_by_sharing_strategy.png')
  ggsave(path, plot = last_plot(), units="in", width=8, height=7, dpi=300)


  ################################################################################

  folder <- dirname(rstudioapi::getSourceEditorContext()$path)

  filename = 'national_market_cost_results_policy_options.csv'
  data <- read.csv(file.path(folder, '..', 'results', 'model_results', iso3, filename))

  names(data)[names(data) == 'GID_0'] <- 'country'

  data$scenario_adopt[grep("low", data$scenario)] = 'Low (2% Adoption Growth)'
  data$scenario_adopt[grep("baseline", data$scenario)] = 'Baseline (4% Adoption Growth)'
  data$scenario_adopt[grep("high", data$scenario)] = 'High (6% Adoption Growth)'

  data$scenario_capacity = ''
  data$scenario_capacity[grep("2_2_2", data$scenario)] = '~2 Mbps Per User'
  data$scenario_capacity[grep("5_5_5", data$scenario)] = '~5 Mbps Per User'
  data$scenario_capacity[grep("10_10_10", data$scenario)] = '~10 Mbps Per User'
  # data$scenario_capacity[grep("20_20_20", data$scenario)] = '~20 Mbps Per User'

  # data = data[!grepl(c("low_2_2_2"), data$scenario),]
  # data = data[!grepl(c("baseline_2_2_2"), data$scenario),]
  # data = data[!grepl(c("high_2_2_2"), data$scenario),]
  data = data[!grepl(c("low_20_20_20"), data$scenario),]
  data = data[!grepl(c("baseline_20_20_20"), data$scenario),]
  data = data[!grepl(c("high_20_20_20"), data$scenario),]

  data$strategy_short = ''
  data$strategy_short[grep("4G_epc_wireless", data$strategy)] = '4G (W)'

  data = data %>% filter(data$strategy_short == '4G (W)')

  data$strategy = factor(data$strategy, levels=c(
    "4G_epc_wireless_baseline_baseline_high_baseline",
    "4G_epc_wireless_baseline_baseline_low_baseline",
    "4G_epc_wireless_baseline_baseline_baseline_high",
    "4G_epc_wireless_baseline_baseline_baseline_low",
    "4G_epc_wireless_baseline_baseline_baseline_baseline"
    ),
  labels=c(
    "High Spectrum\nFees",
    "Low Spectrum\nFees",
    "High Tax",
    "Low Tax",
    "Baseline"
    ))

  data = data[complete.cases(data),]

  data$scenario_capacity = factor(data$scenario_capacity,
                                  levels=c("~2 Mbps Per User",
                                           "~5 Mbps Per User",
                                           "~10 Mbps Per User"#,
                                           # "~20 Mbps Per User"
                                  ))

  data$scenario_adopt = factor(data$scenario_adopt,
                               levels=c("Low (2% Adoption Growth)",
                                        "Baseline (4% Adoption Growth)",
                                        "High (6% Adoption Growth)"))

  data <- data[(data$confidence == 50),]

  data <- select(data, scenario_adopt, scenario_capacity, strategy,
                 cost_per_network_user, cost_per_smartphone_user,
                 private_cost, government_cost, societal_cost)

  totals <- data %>%
    group_by(scenario_adopt, scenario_capacity, strategy) %>%
    summarize(social_cost = round(
      (societal_cost)/1e9, decimal_places_c))

  min_value = min(round(data$societal_cost/ 1e9, 2))
  max_value = max(round(data$societal_cost/ 1e9, 2))
  min_value[min_value > 0] = 0

  colnames(data)[colnames(data) == 'private_cost'] <- 'Private Cost ($USD)'
  colnames(data)[colnames(data) == 'government_cost'] <- 'Government Cost ($USD)'
  colnames(data)[colnames(data) == 'societal_cost'] <- 'Social Cost ($USD)'

  data <- data %>% gather(key="Cost_Type", value = "value",
                          'Private Cost ($USD)',
                          'Government Cost ($USD)',
  )

  data$value = round(data$value/1e9, 2)

  vis3 = ggplot(data, aes(y=value, x=strategy, fill=Cost_Type)) +
    geom_bar(position="stack", stat="identity") +
    geom_text(aes(strategy, social_cost, label = social_cost, fill = NULL),
              size = 2.5, data = totals, hjust=hjust_c) +
    coord_flip() +
    scale_fill_manual(values=c("#E1BE6A", "#40B0A6"), name=NULL) +
    theme(legend.position = "bottom",
          axis.text.x = element_text(angle = 45, hjust=1)) +
    labs(title = "NPV of the Social Cost by Policy Strategy using 4G (W) (2020-2030)",
         colour=NULL,
         subtitle = "The Private Cost is invested by operators. The Government Cost is invested by Government.",
         x = NULL, y = "Social Cost (Billions $USD)") +
    scale_y_continuous(expand = c(0, 0), limits = c(-0,max_value+(max_value/5))) +
    theme(panel.spacing = unit(0.6, "lines")) +
    guides(fill=guide_legend(ncol=3, reverse = TRUE)) +
    facet_grid(scenario_capacity~scenario_adopt)

  path = file.path(folder, 'figures', iso3, 'social_costs_by_policy_options.png')
  ggsave(path, plot = last_plot(), units="in", width=8, height=7, dpi=300)
  path = file.path(folder, '..', 'reports', 'images', iso3, 'social_costs_by_policy_options.png')
  ggsave(path, plot = last_plot(), units="in", width=8, height=7, dpi=300)

  ################################################################################

  folder <- dirname(rstudioapi::getSourceEditorContext()$path)

  filename = 'national_market_cost_results_technology_options.csv'
  data <- read.csv(file.path(folder, '..', 'results', 'model_results', iso3, filename))

  data <- data[(data$confidence == 50),]

  names(data)[names(data) == 'GID_0'] <- 'country'

  names(data)[names(data) == 'GID_0'] <- 'country'

  data$scenario_adopt[grep("low", data$scenario)] = 'Low (2% Adoption Growth)'
  data$scenario_adopt[grep("baseline", data$scenario)] = 'Baseline (4% Adoption Growth)'
  data$scenario_adopt[grep("high", data$scenario)] = 'High (6% Adoption Growth)'

  data$scenario_capacity = ''
  data$scenario_capacity[grep("2_2_2", data$scenario)] = '~2 Mbps Per User'
  data$scenario_capacity[grep("5_5_5", data$scenario)] = '~5 Mbps Per User'
  data$scenario_capacity[grep("10_10_10", data$scenario)] = '~10 Mbps Per User'
  # data$scenario_capacity[grep("20_20_20", data$scenario)] = '~20 Mbps Per User'

  # data = data[!grepl(c("low_2_2_2"), data$scenario),]
  # data = data[!grepl(c("baseline_2_2_2"), data$scenario),]
  # data = data[!grepl(c("high_2_2_2"), data$scenario),]
  data = data[!grepl(c("low_20_20_20"), data$scenario),]
  data = data[!grepl(c("baseline_20_20_20"), data$scenario),]
  data = data[!grepl(c("high_20_20_20"), data$scenario),]

  data$strategy_short = ''
  data$strategy_short[grep("3G_umts_fiber", data$strategy)] = '3G (F)'
  data$strategy_short[grep("3G_umts_wireless", data$strategy)] = '3G (W)'
  data$strategy_short[grep("4G_epc_fiber", data$strategy)] = '4G (F)'
  data$strategy_short[grep("4G_epc_wireless", data$strategy)] = '4G (W)'
  data$strategy_short[grep("5G_nsa_fiber", data$strategy)] = '5G (F)'
  data$strategy_short[grep("5G_nsa_wireless", data$strategy)] = '5G (W)'

  data$strategy_short = factor(data$strategy_short, levels=c(
    "3G (F)",
    "4G (F)",
    '5G (F)',
    "3G (W)",
    "4G (W)",
    '5G (W)'
  ))

  data$scenario_capacity = factor(data$scenario_capacity,
                                  levels=c("~2 Mbps Per User",
                                           "~5 Mbps Per User",
                                           "~10 Mbps Per User"#,
                                           # "~20 Mbps Per User"
                                  ))

  data = data[complete.cases(data), ]

  data$scenario_adopt = factor(data$scenario_adopt,
                               levels=c("Low (2% Adoption Growth)",
                                        "Baseline (4% Adoption Growth)",
                                        "High (6% Adoption Growth)"))

  data <- data[(data$scenario_adopt == 'Baseline (4% Adoption Growth)'),]

  data <- select(data, scenario_adopt, scenario_capacity, strategy_short,
                 total_ran:total_market_cost)

  data = data %>%
    group_by(scenario_adopt, scenario_capacity, strategy_short) %>%
    mutate(
      perc_ran = total_ran / total_market_cost * 100,
      perc_backhaul = total_backhaul_fronthaul / total_market_cost * 100,
      perc_civils = total_civils / total_market_cost * 100,
      perc_core_network = total_core_network / total_market_cost * 100,
      perc_administration = total_administration / total_market_cost * 100,
      perc_spectrum_cost = total_spectrum_cost / total_market_cost * 100,
      perc_tax = total_tax / total_market_cost * 100,
      perc_profit_margin = total_profit_margin / total_market_cost * 100,
    ) %>%
    select(scenario_adopt, scenario_capacity, strategy_short, perc_ran,
           perc_backhaul, perc_civils,
           perc_core_network, perc_administration, perc_spectrum_cost,
           perc_tax, perc_profit_margin)

  data <- gather(data, metric, value, perc_ran:perc_profit_margin)

  data$metric = factor(data$metric, levels=c(
    'perc_profit_margin',
    'perc_tax',
    'perc_spectrum_cost',
    'perc_administration',
    'perc_core_network',
    'perc_civils',
    'perc_backhaul',
    'perc_ran'
  ),
  labels=c(
    "Profit",
    "Tax",
    "Spectrum",
    "Administration",
    'Core',
    "Civils",
    "Backhaul",
    "RAN"
  ))

  ggplot(data, aes(x=strategy_short, y=value, group=metric, fill=metric)) +
    geom_bar(stat = "identity") +
    coord_flip() +
    scale_fill_brewer(palette="Spectral", name = NULL, direction=1) +
    theme(legend.position = "bottom", axis.text.x = element_text(angle = 45, hjust = 1)) +
    labs(title = "Private Cost Composition by Technology", colour=NULL,
         subtitle = "Baseline Infrastructure Sharing, Spectrum Pricing and Taxation",
         x = NULL, y = "Percentage of Total Private Cost (%)") +
    scale_y_continuous(expand = c(0, 0)) +
    theme(panel.spacing = unit(0.6, "lines")) +
    guides(fill=guide_legend(ncol=8, reverse = TRUE)) +
    facet_wrap(scenario_capacity~scenario_adopt, scales = "free", ncol=3)

  path = file.path(folder, 'figures', iso3, 'private_cost_composition.png')
  ggsave(path, plot = last_plot(), units="in", width=8, height=4, dpi=300)
  path = file.path(folder, '..', 'reports', 'images', iso3, 'private_cost_composition.png')
  ggsave(path, plot = last_plot(), units="in", width=8, height=4, dpi=300)

  }

