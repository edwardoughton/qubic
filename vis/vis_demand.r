###VISUALISE MODEL OUTPUTS###
library(tidyverse)
library(ggpubr)


my_list = list(
  # c("AFG", 0, -.3, 0, -.4, 1, -.3),
  # c("AGO", 0, -.5, 0, -1.2, 1, -.6),
  # c("BGD", 0, -.2, 0, -.5, 1, -.42),
  # c("BTN", 1, -.3, 1, -.4, 2, -.3),
  # c("CMR", 0, -.2, 0, -.5, 1, -.42),
  c("COL", 1, -.3, 1, -.4, 2, -.3)#,
  # c("CRI", 1, -.3, 1, -.4, 2, -.3),
  # c("EGY", 0, -.2, 0, -.7, 1, -.42),
  # c("SLV", 1, -.3, 1, -.7, 1, -.4),
  # c("GMB", 2, -.2, 2, -.5, 2, -.42),
  # c("HND", 1, -.4, 1, -1.1, 2, -.7),
  # c("IND", 0, -.2, 0, -2.2, 0, -2),
  # c("KEN", 0, -.2, 0, -.6, 1, -.42),
  # c("LKA", 0, -.3, 0, -.6, 1, -.3),
  # c("MAR", 0, -.2, 0, -.7, 2, -.42),
  # c("MDG", 0, -.2, 0, -.3, 1, -.42),
  # c("MDV", 1, -1, 1, -1.3, 3, -.7),
  # c("MOZ", 0, -.2, 0, -.5, 1, -.42),
  # c("MWI", 0, -.2, 0, -1, 1, -.42),
  # c("NPL", 0, -.2, 0, -.5, 1, -.42),
  # c("NGA", 0, -.2, 0, -.5, 0, -.42),
  # c("PAK", 0, -.2, 0, -1.2, 0, -1.4),
  # c("SEN", 0, -.2, 0, -1, 1, -.3)
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
  
  folder <- dirname(rstudioapi::getSourceEditorContext()$path)
  filename = paste(iso3,'.csv', sep="")
  path = file.path(folder, 'subscriptions', 'data_inputs', filename)
  
  data <- read.csv(path)
  
  data$scenario = factor(data$scenario, levels=c("low",
                                                 'baseline',
                                                 "high"
  ),
  labels=c("Low",
           "Baseline",
           "High"
  ))
  
  data = data[complete.cases(data),]
  
  subscriptions = 
    ggplot(data, aes(x=year, y=penetration, group=scenario)) +
    geom_point(aes(shape=scenario, color=scenario), size=1) +
    geom_line(aes(color=scenario)) +
    scale_shape_manual(values=c(0, 1, 2, 3, 4, 5)) +
    scale_size_manual(values=c(0.1, 0.1, 0.1, 0.1, 0.1)) +
    scale_color_manual(values=c( 
                                # "#F0E442",
                                #"#E69F00",
                                "#56B4E9",
                                "#009E73",
                                "#D55E00"#, 
                                # "#0072B2"
                                )) +
    geom_vline(xintercept=2020, linetype="dashed", color = "grey", size=.5) +
    scale_x_continuous(expand = c(0, 0.5), limits = c(2010,2030),
                       breaks = seq(2010,2030,2)) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          legend.position = "bottom", legend.title=element_blank()) +
    labs(title = "(A) Mobile Subscription Forecast by Scenario",
         x = NULL, y = "Subscribers (%)") +
    guides(shape=guide_legend(ncol=6), colour=guide_legend(ncol=6)) 
  
  #get folder directory
  folder <- dirname(rstudioapi::getSourceEditorContext()$path)
  filename = paste(iso3,'.csv', sep="")
  path = file.path(folder, 'smartphones', 'data_inputs', filename)
  
  data <- read.csv(path)
  
  data$scenario = factor(data$scenario, levels=c("low",
                                                 'baseline',
                                                 "high"
  ),
  labels=c("Low",
           "Baseline",
           "High"
  ))
  
  data$settlement_type = factor(data$settlement_type,
                                levels=c("urban",
                                         "rural"),
                                labels=c("Urban",
                                         "Rural"))
  
  data = data[complete.cases(data),]
  data$country = NULL
  
  smartphones = 
    ggplot(data, aes(x=year, y=penetration, group=scenario)) +
    geom_point(aes(shape=scenario, color=scenario), size=1) +
    geom_line(aes(color=scenario)) +
    scale_shape_manual(values=c(0, 1, 2, 3, 4, 5)) +
    scale_color_manual(values=c("#009E73", "#F0E442","#E69F00"#,
                                #"#56B4E9","#D55E00", "#0072B2"
                                )) +
    scale_x_continuous(expand = c(0, 0.25), limits = c(2020,2030),
                       breaks = seq(2020,2030,2)) +
    scale_y_continuous(expand = c(0, 0), limits = c(0,100)) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          legend.position = "bottom", legend.title=element_blank()) +
    labs(title = "(B) Smartphone Penetration Forecast by Scenario",
         x = NULL, y = "Smartphones (%)") +
    guides(shape=guide_legend(ncol=6), colour=guide_legend(ncol=6)) +
    facet_grid(~settlement_type)
  
  combined <- ggarrange(subscriptions, smartphones,
                        ncol = 1, nrow = 2,
                        common.legend = TRUE,
                        legend='bottom', heights=c(5, 5))
  
  path = file.path(folder, 'figures', iso3, 'demand_graphic.png')
  ggsave(path, units="in", width=6, height=5.5, dpi=300)
  print(combined)
  dev.off()
  
  dir.create(file.path(folder, '..', 'reports', 'images', iso3), showWarnings = FALSE)
  path = file.path(folder, '..', 'reports', 'images', iso3, 'demand_graphic.png')
  ggsave(path, plot = last_plot(), units="in", width=8, height=7, dpi=300)
  
  
  remove(subscriptions, smartphones, combined, data)
}