library(tidyverse)

###################################################################
folder <- dirname(rstudioapi::getSourceEditorContext()$path)

#load data
filename = 'national_market_cost_results_technology_options.csv'
data1 <- read.csv(file.path(folder, '..',  '..', 'results', 
                           'model_results', 'SEN', filename))
data2 <- read.csv(file.path(folder, '..',  '..', 'results', 
                           'model_results', 'GMB', filename))

data = rbind(data1, data2)

rm(data1, data2)

data <- data[grep("10_10_10", data$scenario), ]
data <- data[!(data$total_market_cost == "NA"),]
data <- data[(data$confidence == 50),]
names(data)[names(data) == 'societal_cost'] <- 'social_cost'
data = select(data, GID_0, scenario, strategy, private_cost, 
              government_cost, social_cost)

data$strategy = factor(data$strategy, levels=c(
  "3G_umts_fiber_baseline_baseline_baseline_baseline",
  "4G_epc_fiber_baseline_baseline_baseline_baseline",
  "5G_nsa_fiber_baseline_baseline_baseline_baseline",
  "3G_umts_wireless_baseline_baseline_baseline_baseline",
  "4G_epc_wireless_baseline_baseline_baseline_baseline",
  "5G_nsa_wireless_baseline_baseline_baseline_baseline"
  ),
  labels=c("3G (FB)", "4G (FB)", "5G (FB)", 
           "3G (W)","4G (W)", "5G (W)"))

names(data)[names(data) == 'GID_0'] <- 'country'

data <- select(data, country, scenario, strategy, private_cost, 
               government_cost, social_cost)

data = data[complete.cases(data),]

data$scenario = factor(data$scenario, levels=c("low_10_10_10",
                                               "baseline_10_10_10",
                                               "high_10_10_10"),
                       labels=c("Low",
                                "Baseline",
                                "High"))

# data = data[data$country == 'GMB' | data$country == 'SEN' | data$country == 'UGA',] 

data$country = factor(data$country, levels=c("GMB",
                                             "SEN"),
                      labels=c("The Gambia",
                               "Senegal"
                      ))

min_value = round(min(data$social_cost)/1e9,0)
max_value = round(max(data$social_cost)/1e9,0)

totals <- data %>%
  group_by(country, scenario, strategy) %>%
  summarize(social_cost = round(
    (social_cost)/1e9, 2))

colnames(data)[colnames(data) == 'private_cost'] <- 'Private Cost ($USD)'
colnames(data)[colnames(data) == 'government_cost'] <- 'Government Cost ($USD)'
colnames(data)[colnames(data) == 'societal_cost'] <- 'Social Cost ($USD)'

data <- data %>% gather(key="Cost_Type", value = "value",
                        'Private Cost ($USD)', 
                        'Government Cost ($USD)', 
)

data$value = round(data$value/1e9, 2)

ggplot(data, aes(y=value, x=strategy, fill=Cost_Type)) + 
  geom_bar(position="stack", stat="identity") +
  geom_text(aes(strategy, social_cost, label = social_cost, fill = NULL),
            size = 2, data = totals, hjust=-.2) +
  coord_flip() +
  scale_fill_manual(values=c("#E1BE6A", "#40B0A6"), name=NULL) +
  theme(legend.position = "bottom") +
  labs(
    title="Cross-Country Cost Comparison of Universal Broadband by Technology",
    colour=NULL,
    subtitle = "Reported for all scenarios targetting a mean 10 Mbps Per User",
    x = NULL, y = "Social Cost (Billions $USD)") +
  scale_y_continuous(expand = c(0, 0), limits = c(0, max_value+5)) +
  theme(panel.spacing = unit(0.6, "lines")) +
  guides(fill=guide_legend(ncol=3, reverse = TRUE)) +
  facet_grid(country~scenario)


# combined <- ggarrange(sinr, spectral_efficiency, 
#                       ncol = 1, nrow = 2,
#                       common.legend = TRUE, 
#                       legend='bottom' 
#                       # heights=c(3.5, 5)
# )

path = file.path(folder, 'figures', 'cross_country_costs.png')
ggsave(path, units="in", width=8, height=5, dpi=300)
dev.off()





