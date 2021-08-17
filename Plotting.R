# Análise dos resultados de performance das plataformas


rm(list=ls())

library(tidyverse)
library(ggplot2)
library(readr)
library(stringr)
library(dplyr)
library(ggpubr)

setwd('D:\\Projects\\Mestrado\\performance_watt\\edge\\newperformance')


values <- read.csv('mean_values.csv')
names(values)
View(values)

# Converting the time values to seconds
values$meanNetworkDelay <- values$meanNetworkDelay/1000
values$meanResponseTime <- values$meanResponseTime/1000


## ----------------------------- Plotting the Results-----------------------

#################################################
##     Memory Usage VS worklaod VS Algorithm   ##
##                                            ##   
################################################

# Criando um canvas 2x2 graficos
par(mfrow=c(1,2))
par(mfrow=c(1,1))

opts <- c(4, 2, 1)
workloads <- c(0, 0.01, 0.1, 0.25, 0.5, 0.75, 1.0)
algos <- c('CNN', 'KNN', 'RF')
sizes <- c(8, 32)
cores <- c('black','red','blue')

# Plotando a base do gráfico, apenas com o primeiro dataframe

memory128 <- ggplot(data=filter(values, Size==128), aes(x=Workload, y=MeanMemoryUsage)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='Memory Analysis (128x128)', 
       x='Workload', y='Mean Memory Usage(%)') +
  coord_cartesian(ylim=c(12, 55)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) + 
  scale_y_continuous(breaks=seq(15, 55, 5)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))

memory64 <- ggplot(data=filter(values, Size==64), aes(x=Workload, y=MeanMemoryUsage)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='Memory Analysis (64x64)', 
       x='Workload', y='Mean Memory Usage(%)') +
  coord_cartesian(ylim=c(12, 55)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) + 
  scale_y_continuous(breaks=seq(15, 55, 5)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))



memory32 <- ggplot(data=filter(values, Size==32), aes(x=Workload, y=MeanMemoryUsage)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='Memory Analysis (32x32)', 
       x='Workload', y='Mean Memory Usage(%)') +
  coord_cartesian(ylim=c(12, 55)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) + 
  scale_y_continuous(breaks=seq(15, 55, 5)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))
  


memory8 <- ggplot(data=filter(values, Size==8), aes(x=Workload, y=MeanMemoryUsage)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='Memory Analysis (8x8)', x='Workload', y='Mean Memory Usage(%)') +
  coord_cartesian(ylim=c(12, 55)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) + 
  scale_y_continuous(breaks=seq(15, 55, 5)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))



cpu128 <- ggplot(data=filter(values, Size==128), aes(x=Workload, y=MeanCPUUsage)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='CPU Analysis (128x128)', x='Workload', y='Mean CPU Usage(%)') +
  coord_cartesian(ylim=c(25, 65)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) + 
  scale_y_continuous(breaks=seq(25, 65, 5)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))


cpu64 <- ggplot(data=filter(values, Size==64), aes(x=Workload, y=MeanCPUUsage)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='CPU Analysis (64x64)', x='Workload', y='Mean CPU Usage(%)') +
  coord_cartesian(ylim=c(25, 65)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) + 
  scale_y_continuous(breaks=seq(25, 65, 5)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))


cpu32 <- ggplot(data=filter(values, Size==32), aes(x=Workload, y=MeanCPUUsage)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='CPU Analysis (32x32)', x='Workload', y='Mean CPU Usage(%)') +
  coord_cartesian(ylim=c(25, 65)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) + 
  scale_y_continuous(breaks=seq(25, 65, 5)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))


cpu8 <- ggplot(data=filter(values, Size==8), aes(x=Workload, y=MeanCPUUsage)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='CPU Analysis (8x8)', x='Workload', y='Mean CPU Usage(%)') +
  coord_cartesian(ylim=c(25, 65)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) + 
  scale_y_continuous(breaks=seq(25, 65, 5)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))



watt128 <- ggplot(data=filter(values, Size==128), aes(x=Workload, y=MeanConsumption)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='Watt Consumption Analysis \n(128x128)', x='Workload', y='Mean Watt Consumption (W)') +
  coord_cartesian(ylim=c(3, 5.6)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) + 
  scale_y_continuous(breaks=seq(3.2, 5.6, 0.4)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))


watt64 <- ggplot(data=filter(values, Size==64), aes(x=Workload, y=MeanConsumption)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='Watt Consumption Analysis \n(64x64)', x='Workload', y='Mean Watt Consumption (W)') +
  coord_cartesian(ylim=c(3.2, 5.6)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) + 
  scale_y_continuous(breaks=seq(3.2, 5.6, 0.4)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))



watt32 <- ggplot(data=filter(values, Size==32), aes(x=Workload, y=MeanConsumption)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='Watt Consumption Analysis \n(32x32)', x='Workload', y='Mean Watt Consumption (W)') +
  coord_cartesian(ylim=c(3.2, 5.6)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) + 
  scale_y_continuous(breaks=seq(3.2, 5.6, 0.4)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))



watt8 <- ggplot(data=filter(values, Size==8), aes(x=Workload, y=MeanConsumption)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='Watt Consumption Analysis \n(8x8)', x='Workload', y='Mean Watt Consumption (W)') +
  coord_cartesian(ylim=c(3.2, 5.6)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) + 
  scale_y_continuous(breaks=seq(3.2, 5.6, 0.4)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))


# ----- Plotting the Response times ----------------------------------------------------------

clasTime128 <- ggplot(data=filter(values, Size==128), aes(x=Workload, y=meanResponseTime)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='Response Time Analysis \n(128x128)', x='Workload', y='Mean Response Time (s)') +
  coord_cartesian(ylim=c(0, 0.35)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) +
  scale_y_continuous(breaks=seq(0, 0.35, 0.1)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))


clasTime64 <- ggplot(data=filter(values, Size==64), aes(x=Workload, y=meanResponseTime)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='Response Time Analysis \n(64x64)', x='Workload', y='Mean Response Time (s)') +
coord_cartesian(ylim=c(0, 0.35)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) +
  scale_y_continuous(breaks=seq(0, 0.35, 0.1)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))



clasTime32 <- ggplot(data=filter(values, Size==32), aes(x=Workload, y=meanResponseTime)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='Response Time Analysis \n(32x32)', x='Workload', y='Mean Response Time (s)') +
  coord_cartesian(ylim=c(0, 0.35)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) +
  scale_y_continuous(breaks=seq(0, 0.35, 0.1)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))
                     #values = c("#999999",hcl(c(15, 195), 100, 65)))



clasTime8 <- ggplot(data=filter(values, Size==8), aes(x=Workload, y=meanResponseTime)) +
  geom_line(aes(col=Algorithm)) + 
  labs(title='Response Time Analysis \n(8x8)', x='Workload', y='Mean Response Time (s)') +
  coord_cartesian(ylim=c(0, 0.35)) +
  scale_x_continuous(breaks=c(round(0.0, 1), 0.1, 0.25, 0.5, 0.75, 1.0)) +
  scale_y_continuous(breaks=seq(0, 0.35, 0.1)) +
  scale_color_manual(limits = c("CNN", "KNN", "RF"),
                     values = c('#00ccff','#ff3300', '#000000'))



ggarrange(
  memory128, memory64, memory32, memory8, #labels = c("32x32", "8x8"),
  common.legend = TRUE, legend = "right"
)

ggarrange(
  cpu128, cpu64, cpu32, cpu8, #labels = c("32x32", "8x8"),
  common.legend = TRUE, legend = "right"
)

ggarrange(
  watt128, watt64, watt32, watt8, #labels = c("32x32", "8x8"),
  common.legend = TRUE, legend = "right"
)

ggarrange(
  clasTime128, clasTime64, clasTime32, clasTime8, #labels = c("32x32", "8x8"),
  common.legend = TRUE, legend = "right"
)

# ggarrange(
#   delayTime128, delayTime64, delayTime32, delayTime8, #labels = c("32x32", "8x8"),
#   common.legend = TRUE, legend = "bottom"
# )

