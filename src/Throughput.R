library(readr)

#############################################################
#    CLOUD
#############################################################

#setwd("D:/Dropbox/Acadêmico/Minhas Pesquisas/Aging + Edge/Revista/Scripts/Private Cloud/Results - CloudStack")

perf1 <- read.csv(file = "monitoringCloudStackPerformance_0.1_Treated.csv", header = T, strip.white = T, na.strings = "", stringsAsFactors=FALSE, quote="" )
perf1<-perf1[perf1$currentTime<72, ]
perf1$hour <- as.factor(ceiling(perf1$currentTime))
perf1[1,5]<-1
#perf1[1,2]<-1
T1<- summary(perf1$hour)
T1<-T1[-1]
ET1<-rep.int(36000, length(T1))
#(Expected throughput – Real throughput) / Expected throughput
DR1<-(ET1-T1)/ET1
#Pegar as médias dos tempos de respostas.
T_M1 <- tapply(perf1$meanResponseTime, perf1$hour, mean)
T_M1<-T_M1[-1]
#Throughput/Response Time
power1<-T1/T_M1

perf2 <- read.csv(file = "monitoringCloudStackPerformance_0.5_Treated.csv", header = T, strip.white = T, na.strings = "", stringsAsFactors=FALSE, quote="" )
perf2<-perf2[perf2$currentTime<72, ]
perf2$hour <- as.factor(ceiling(perf2$currentTime))
perf2[1,5]<-1
#perf2[1,2]<-1
T2<- summary(perf2$hour)
T2<-T2[-1]
ET2<-rep.int(7200, length(T2))
#(Expected throughput – Real throughput) / Expected throughput
DR2<-(ET2-T2)/ET2
#Pegar as médias dos tempos de respostas.
T_M2 <- tapply(perf2$meanResponseTime, perf2$hour, mean)
T_M2<-T_M2[-1]
#Throughput/Response Time
power2<-T2/T_M2


perf3 <- read.csv(file = "monitoringCloudStackPerformance_1.0_Treated.csv", header = T, strip.white = T, na.strings = "", stringsAsFactors=FALSE, quote="" )
perf3<-perf3[perf3$currentTime<72, ]
perf3$hour <- as.factor(ceiling(perf3$currentTime))
perf3[1,5]<-1
#perf3[1,2]<-1
T3<- summary(perf3$hour)
T3<-T3[-1]
ET3<-rep.int(3600, length(T2))
#(Expected throughput – Real throughput) / Expected throughput
DR3<-(ET3-T3)/ET3
#Pegar as médias dos tempos de respostas.
T_M3 <- tapply(perf3$meanResponseTime, perf3$hour, mean)
T_M3<-T_M3[-1]
#Throughput/Response Time
power3<-T3/T_M3


###Plot
plot(names(T1),T1, type="o",pch=4, xlab="Time (hour)", ylab="Throughput (Trans/hour)",
     lwd = 1, cex.main=2, ylim = c(min(T1),36000))
lines(names(T1), rep.int(36000, length(T1)), type = "o", pch=1, col = "red")
legend("bottomright", pch = c(4,1),  legend = c("Real Throughput", "Expected Throughput"), col = c("black", "red", "blue"), 
       lty=1, lwd=1)

plot(names(T2),T2, type="o",pch=4, xlab="Time (hour)", ylab="Throughput (Trans/hour)",
     lwd = 1, cex.main=2,ylim = c(min(T2),7200))
lines(names(T2), rep.int(7200, length(T2)), type = "o", pch=1, col = "red")
legend("bottomleft", pch = c(4,1),  legend = c("Real Throughput", "Expected Throughput"), col = c("black", "red", "blue"), 
       lty=1, lwd=1)

plot(names(T3),T3, type="o",pch=4, xlab="Time (hour)", ylab="Throughput (Trans/hour)",
     lwd = 1, cex.main=2, ylim = c(min(T3),3600))
lines(names(T3), rep.int(3600, length(T3)), type = "o", pch=1, col = "red")
legend("bottomright", pch = c(4,1),  legend = c("Real Throughput", "Expected Throughput"), col = c("black", "red", "blue"), 
       lty=1, lwd=1)

#Power
plot(names(T1),power1, type="o",pch=4, xlab="Time (hour)", ylab="Power",
     lwd = 1, cex.main=2, main = "Power Analysis (Cloud)",ylim = c(8000,63000))
lines(names(T2), power2, type = "o", pch=1, col = "red")
lines(names(T3), power3, type = "o", pch=3, col = "blue")
legend(40, 30000, pch = c(4,1,3),  legend = c("workload 0.1", "workload 0.5","workload 1"), 
       col = c("black", "red", "blue"), lty=1, lwd=1)

#Request Dropping Analysis (Cloud)
plot(names(DR1),DR1, type="o",pch=4, xlab="Time (hour)", ylab="Request drop rate",
     lwd = 1, cex.main=2, main = "Request Dropping Analysis (Cloud)", ylim = c(0.0,0.8))
lines(names(DR2), DR2, type = "o", pch=1, col = "red")
lines(names(DR3), DR3, type = "o", pch=3, col = "blue")
legend(5, 0.4, pch = c(4,1,3),  legend = c("workload 0.1", "workload 0.5","workload 1"), 
       col = c("black", "red", "blue"), lty=1, lwd=1)

