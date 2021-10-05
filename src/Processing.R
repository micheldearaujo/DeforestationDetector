# Processando os resultados dos experimentos

rm(list=ls())

library(tidyverse)
library(ggplot2)
library(readr)
library(stringr)
library(dplyr)

# Carregando os arquivos
setwd('/media/michel/dados/Projects/Mestrado/performance_watt/cloud/')

# ----------------- Explorando os novos dados do watts up


# -- Limpando os arquivos txt que vieram com mais colunas de dados do que de título
# Só deve ser executada uma vez.

# -- O que é necessário fazer para cada arquivo?
# -- É necessário combinar os dados dos arquivos txt (Watts) com os dados dos arquivos csv
# -- Que possuem os recursos da maquina.
# -- Dessa forma, são 12 arquivos, 6 de cada, que irão se combinar e gerar apenas 6 de volta.
# -- Here is the function

clean_txt <- function(file_name){
  dat <- readLines(file_name)
  times <- vector()
  wats <- vector()
  for (line in 1:length(dat)){
    times[line] <- strsplit(dat, split='\t')[[line]][1]
    wats[line] <- strsplit(dat, split='\t')[[line]][2]
    
  }
  watts.df <- data.frame(Tempo = times, Watt = wats)
  watts.df <- watts.df[-c(1,2),][1:34,]
  write.csv(watts.df, file_name, row.names=F)
}


load_transform <- function(resources_name, watts_name){
  # Loading the files
  resources.i <- read.csv(resources_name)
  watt.i <- read.delim2(watts_name, sep=',')
  
  # # Transformando o currenTime em diferenças de tempos entre o tempo j e o tempo inicial
  tempos <- vector()
  for (j in 1:nrow(resources.i)){
    tempos[j] <- (difftime(resources.i$currentTime[j], resources.i$currentTime[1], units=c('secs')))/60
  }
  resources.i$Time <- tempos
  
  # Criando uma coluna em cada dataframe para fazer a união
  watt.i$Id <- c(1:nrow(watt.i))
  #watt.i <- watt.i[1:34,]
  resources.i <- resources.i[1:34,]
  resources.i$Id <- c(1:34)
  
  # Unindo os dois dataframes em apenas um
  final.i <- merge(watt.i, resources.i, by='Id')
  final.i <- final.i[-c(2)]
  head(final.i)
  
  # Salvando o dataframe tratado
  write.csv(final.i, resources_name, row.names=FALSE)
  return (final.i)
}

res <- resources.files[1]
res <- read.csv(res)
View(res)

load_transform_without_watt <- function(resources_name){
  # Loading the files
  resources.i <- read.csv(resources_name)
  
  # # Transformando o currenTime em diferenças de tempos entre o tempo j e o tempo inicial
  tempos <- vector()
  for (j in 1:nrow(resources.i)){
    tempos[j] <- (difftime(resources.i$currentTime[j], resources.i$currentTime[1], units=c('secs')))/60
  }
  resources.i$Time <- tempos
  
  #resources.i <- resources.i[1:34,]
  
  # Salvando o dataframe tratado
  write.csv(resources.i, resources_name, row.names=FALSE)
  return (resources.i)
}

# Pegando os nomes dos arquivos na pasta

watts.files <- list.files('resources/', pattern='TXT', full.names=T)
resources.files <- list.files('resources/', pattern='csv', full.names=T)
times.files <- list.files('times/', pattern='csv', full.name=T)

watts.files
resources.files
times.files

# Aplicando a limpeza nos arquivos txt, retornando apenas o tempo e o watt, com apenas 34 observações
for (file_name in watts.files){
 clean_txt(file_name=file_name)
}

# Aplicando a transformação e salvando os novos csvs
for (file_number in 1:length(resources.files)){
 df <- load_transform(resources.files[file_number], watts.files[file_number])
}

# Aplicando a transformação e salvando os novos csvs (CLOUD)
for (file_number in 1:length(resources.files)){
  df <- load_transform_without_watt(resources.files[file_number])
}

View(df)

# OS DADOS FORAM TRATADOS!

## --- Adicionando todos os dataframes em apenas um

uniteData <- function(files){
  # Primeiro vamos carregar o primeiro, que servirá de base para adicionar os outros
  df0 <- read.csv(files[1])
  
  # Aqui criamos uma coluna com o nome do arquivo, que contém o nome do algoritmo, o workload e o tamanho da imagem
  df0$desc <- files[1]
  
  # Aqui vamos criar um loop para adicionar cada um dos arquivos a partir do list.files
  for (file_number in 2:length(files)){
    print(files[file_number])
    df1 <- read.csv(files[file_number])
    df1$desc <- files[file_number]
    df0 <- rbind(df0, df1)
  }
  
  # Separando a coluna com o nome do arquivo que foi criada anteriormente em diferentes
  # informações, como o algoritmo, o tamanho da imagem e workload.
  df0 <- separate(df0, col='desc',
                  into=c('info', 'Platform', 'Algorithm', 'Size', 'Workload'),
                  sep='_')
  
  # Limpando o workload
  df0$Workload <- parse_number(x=df0$Workload)
  df0$Platform <- str_extract(string=df0$Platform, pattern='edge|server|cloud')
  df0$Platform <- toupper(df0$Platform)
  df0$Algorithm <- toupper(df0$Algorithm)
  write.csv(df0, 'resources/resources.csv', row.names=F)
  return (df0)
  
}

data <- uniteData(resources.files)
View(data)




# ------- PROCESSING THE TIMING FILES
# Transformando o currenTime em diferenças de tempos entre o tempo j e o tempo inicial
# groupby workload e média dos tempos

transform_times <- function(times.name){
  
  times.i <- read.csv(times.name)
  
  tempos1 <- vector()
  tempos2 <- vector()
  j<-1
  for (j in 1:nrow(times.i)){
    tempos1[j] <- (difftime(times.i$currentTime[j], times.i$currentTime[1], units=c('secs')))/60
    # Transformando o classificationTime em segundos
    #tempos2[j] <- as.numeric(unlist(strsplit(times.i$classificationTime[j], split='\\.'))[2])/1000000
  }
  times.i$Tempo <- tempos1
  #times.i$ClassificationTime <- tempos2
  
  times.i <- filter(times.i, Tempo <=34)
  
  times.i$desc <- times.name
  times.i <- separate(times.i, col='desc',
           into=c('Performance', 'Platform', 'Algorithm', 'Size', 'Workload'),
           sep='_')
  
  times.i$Workload <- parse_number(x=times.i$Workload)
  times.i$Platform <- str_extract(string=times.i$Platform, pattern='edge|server|cloud')
  times.i$Platform <- toupper(times.i$Platform)
  times.i$Algorithm <- toupper(times.i$Algorithm)
  write.csv(times.i, times.name, row.names=F)
  return (times.i)
}



start_time <- Sys.time()
for (file in times.files){
  time.df <- transform_times(file)
}
end_time <- Sys.time()

print(paste('O tempo de processamento foi de:', end_time - start_time, sep=' '))


# Criando uma função para unir todos os time.files
unite_TimeData <- function(files){
  time.1 <- read.csv(files[1])
  
  for (file_number in 2:length(files)){
    time.i <- read.csv(files[file_number])
    time.1 <- rbind(time.1, time.i)
  }
  time.1 <- time.1[,-7]
  write.csv(time.1, 'times/times.csv', row.names=F)
  
}

unite_TimeData(times.files)

# --------------------- UNITE AND SALVE ALL

times <- read.csv('times/times.csv')
View(times)
resources <- read.csv('resources/resources.csv')

View(times)
View(resources)

# Calculando as médias dos tempos de classificação
mean.times <- times %>%
  group_by(Platform, Algorithm, Size, Workload) %>%
  summarise(meanNetworkDelay = mean(meanNetworkDelay, na.rm=T),
            meanResponseTime = mean(meanResponseTime, na.rm=T)) %>%
  arrange(Workload, Size)

# Calculando as médias dos recursos
mean.resources <- resources %>%
  group_by(Workload, Size, Algorithm, Platform) %>%
  summarise(MeanMemoryUsage = mean(percentageMemory..., na.rm=T),
            MeanCPUUsage = mean(totalCpuUsage..., na.rm=T),
            MeanAbsMemoryUsage = mean(usedMemory, na.rm=T)
            )
View(mean.resources)
View(mean.times)

# Salvando cada um separadamente
write.csv(mean.times, 'times/mean_times.csv', row.names=F)
write.csv(mean.resources, 'resources/mean_resources.csv', row.names=F)


# -- Uniting the 2 dataframes
#mean.resources$meanNetworkDelay <- mean.times$meanNetworkDelay
#mean.resources$meanResponseTime <- mean.times$meanResponseTime

newcolumn <- mean.resources[1:11,1:4]
newcolumn$meanNetworkDelay <- 0
newcolumn$meanResponseTime <- 0
newcolumns <- rbind(newcolumn, mean.times[1:66,])
mean.resources$meanNetworkDelay <- newcolumns$meanNetworkDelay
mean.resources$meanResponseTime <- newcolumns$meanResponseTime
View(newcolumns)
View(mean.resources)
write.csv(mean.resources, 'mean_values.csv', row.names=F)

# ---------------- testing plot ------------------
re <- read.csv(resources.files[1])
plot(re$Id, re$percentageMemory..., type='o',
     main='Multiprocessamento',
     ylab='Total CPU Usage (%)',
     xlab='Time')

colors <- c('red', 'blue', 'yellow', 'purple', 'black')

for (i in 1:length(names)){
  re <- read.csv(resources.files[i])
  lines(re$Id, re$totalCpuUsage..., col=colors[i])
}

legend('topright', pch = 15, legend=names,
       col=colors)




plot(mean.times$Workload, mean.times$MeanClassificationTime, type='o',
     main='Classification Time vs Workload',
     xlab='Workload',
     ylab='Mean Classification Time')



plot(mean.times$Workload, mean.times$MeanClassificationTime, type='o',
     main='Classification Time vs Workload',
     xlab='Workload',
     ylab='Mean Classification Time')


# ---------------------- LOOKING AT THE NETWORK INFORMATION ------------------

times <- read.csv('times/times.csv')
View(times)
names(times)
mean.times <- times %>%
  group_by(Platform, Algorithm, Size, Workload) %>%
  summarise(meanNetworkDelay = mean(meanNetworkDelay),
            meanResponseTime = mean(meanResponseTime))

View(mean.times)
write.csv(mean.times, 'times/mean_times.csv')
