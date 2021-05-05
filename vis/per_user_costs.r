###VISUALISE MODEL OUTPUTS###
library(tidyverse)
library(ggpubr)

###############################################################################
folder <- dirname(rstudioapi::getSourceEditorContext()$path)

filename = 'regional_market_results_technology_options.csv'
data <- read.csv(file.path(folder, '..', 'results', 'model_results', filename))

names(data)[names(data) == 'GID_0'] <- 'country'

data$scenario_adopt = ''
data$scenario_adopt[grep("low", data$scenario)] = 'Low (2% Adoption Growth)'
data$scenario_adopt[grep("baseline", data$scenario)] = 'Baseline (3% Adoption Growth)'
data$scenario_adopt[grep("high", data$scenario)] = 'High (4% Adoption Growth)'

data$scenario_capacity = ''
data$scenario_capacity[grep("5_5_5", data$scenario)] = '5 Mbps Per User'
data$scenario_capacity[grep("10_10_10", data$scenario)] = '10 Mbps Per User'
data$scenario_capacity[grep("20_20_20", data$scenario)] = '20 Mbps Per User'

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

data = data %>% filter(data$strategy_short == '4G (W)')

data$scenario_capacity = factor(data$scenario_capacity, 
                                levels=c("20 Mbps Per User",
                                         "10 Mbps Per User",
                                         "5 Mbps Per User"))

data$scenario_adopt = factor(data$scenario_adopt, 
                             levels=c("Low (2% Adoption Growth)",
                                      "Baseline (3% Adoption Growth)",
                                      "High (4% Adoption Growth)"))

data <- data[(data$confidence == 50),]

data <- select(data, decile, scenario_adopt, scenario_capacity, strategy_short, 
               private_cost_per_network_user, government_cost_per_network_user)

data <- gather(data, metric, value, private_cost_per_network_user:
                 government_cost_per_network_user)
               
data$metric = factor(data$metric, 
                      levels=c("private_cost_per_network_user",
                               "government_cost_per_network_user"),
                     labels=c("Private Cost",
                              "Government Cost"))

min_value = min(round(data$value))
max_value = max(round(data$value))

data_summary <- function(data, varname, groupnames){
  require(plyr)
  summary_func <- function(x, col){
    c(mean = mean(x[[col]], na.rm=TRUE),
      sd = sd(x[[col]], na.rm=TRUE))
  }
  data_sum<-ddply(data, groupnames, .fun=summary_func,
                  varname)
  data_sum <- rename(data_sum, c("mean" = varname))
  return(data_sum)
}

df2 <- data_summary(data, varname="value", 
                    groupnames=c('decile', 'metric', 'scenario_adopt', 
                                 'scenario_capacity', 'strategy_short'))

ggplot(df2, aes(x=decile, y=value, fill=metric)) + 
  geom_bar(stat="identity", color="black", position=position_dodge()) +
  geom_errorbar(aes(ymin=value, ymax=value+sd), width=.2,
                position=position_dodge(9)) +
  scale_fill_manual(values=c("#E1BE6A", "#40B0A6"), name=NULL) +
  theme(legend.position = "bottom",
        axis.text.x = element_text(angle = 45, hjust=1)
        ) +
  labs(title = "Per User Social Cost of Universal Broadband by Technology for The Gambia",
       colour=NULL,
       subtitle = "Reported for 4G (W) using error bars representing one standard deviation",
       x = NULL, y = "Cost Per User ($USD)") +
  scale_x_continuous(expand = c(0, 0), breaks = seq(0,100, 10)) +
  scale_y_continuous(expand = c(0, 0), limits=c(min_value+100, max_value-100)) +
  theme(panel.spacing = unit(0.6, "lines")) +
  guides(fill=guide_legend(ncol=3, reverse = TRUE)) +
  facet_grid(scenario_capacity~scenario_adopt)

path = file.path(folder, 'figures', 'social_cost_per_user_by_strategy.png')
ggsave(path, units="in", width=8, height=8, dpi=300)
dev.off()



###############################################################################
folder <- dirname(rstudioapi::getSourceEditorContext()$path)

filename = 'regional_market_results_technology_options.csv'
data <- read.csv(file.path(folder, '..', 'results', 'model_results', filename))

names(data)[names(data) == 'GID_0'] <- 'country'

data$scenario_adopt = ''
data$scenario_adopt[grep("low", data$scenario)] = 'Low (2% Adoption Growth)'
data$scenario_adopt[grep("baseline", data$scenario)] = 'Baseline (3% Adoption Growth)'
data$scenario_adopt[grep("high", data$scenario)] = 'High (4% Adoption Growth)'

data$scenario_capacity = ''
data$scenario_capacity[grep("5_5_5", data$scenario)] = '5 Mbps Per User'
data$scenario_capacity[grep("10_10_10", data$scenario)] = '10 Mbps Per User'
data$scenario_capacity[grep("20_20_20", data$scenario)] = '20 Mbps Per User'

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

data = data %>% filter(data$strategy_short == '4G (W)')

data$scenario_capacity = factor(data$scenario_capacity, 
                                levels=c("20 Mbps Per User",
                                         "10 Mbps Per User",
                                         "5 Mbps Per User"))

data$scenario_adopt = factor(data$scenario_adopt, 
                             levels=c("Low (2% Adoption Growth)",
                                      "Baseline (3% Adoption Growth)",
                                      "High (4% Adoption Growth)"))

data <- data[(data$confidence == 50),]

data <- select(data, decile, scenario_adopt, scenario_capacity, strategy_short, 
               private_cost_per_smartphone_user, 
               government_cost_per_smartphone_user)

data <- gather(data, metric, value, private_cost_per_smartphone_user:
                 government_cost_per_smartphone_user)

data$metric = factor(data$metric, 
                     levels=c("private_cost_per_smartphone_user",
                              "government_cost_per_smartphone_user"),
                     labels=c("Private Cost",
                              "Government Cost"))

min_value = min(round(data$value))
max_value = max(round(data$value))

data_summary <- function(data, varname, groupnames){
  require(plyr)
  summary_func <- function(x, col){
    c(mean = mean(x[[col]], na.rm=TRUE),
      sd = sd(x[[col]], na.rm=TRUE))
  }
  data_sum<-ddply(data, groupnames, .fun=summary_func,
                  varname)
  data_sum <- rename(data_sum, c("mean" = varname))
  return(data_sum)
}

df2 <- data_summary(data, varname="value", 
                    groupnames=c('decile', 'metric', 'scenario_adopt', 
                                 'scenario_capacity', 'strategy_short'))

ggplot(df2, aes(x=decile, y=value, fill=metric)) + 
  geom_bar(stat="identity", color="black", position=position_dodge()) +
  geom_errorbar(aes(ymin=value, ymax=value+sd), width=.2,
                position=position_dodge(9)) +
  scale_fill_manual(values=c("#E1BE6A", "#40B0A6"), name=NULL) +
  theme(legend.position = "bottom",
        axis.text.x = element_text(angle = 45, hjust=1)
  ) +
  labs(title = "Smartphone User Social Cost of Universal Broadband by Technology for The Gambia",
       colour=NULL,
       subtitle = "Reported for 4G (W) using error bars representing one standard deviation",
       x = NULL, y = "Cost Per Smartphone ($USD)") +
  scale_x_continuous(expand = c(0, 0), breaks = seq(0,100, 10)) +
  scale_y_continuous(expand = c(0, 0), limits=c(min_value+100, max_value)) +
  theme(panel.spacing = unit(0.6, "lines")) +
  guides(fill=guide_legend(ncol=3, reverse = TRUE)) +
  facet_grid(scenario_capacity~scenario_adopt)

path = file.path(folder, 'figures', 'social_cost_per_smartphone_user_by_strategy.png')
ggsave(path, units="in", width=8, height=8, dpi=300)
dev.off()


