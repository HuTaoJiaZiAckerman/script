library(data.table)
setwd("/home/caominghao/01.Data/04.HJB.Poppulation.Again/23.GWAS/05.emmax_361/")
p<-fread("bh.q4.cov.ps",data.table=F)
map<-read.table("361.qc.ld.bim")
pvalue<- cbind(map[,c(2,1,4)],p[,4])
colnames(pvalue)<-c("SNP","Chr","Pos","Pvalue")
library(CMplot)
CMplot(pvalue,plot.type="q",conf.int.col=NULL,box=TRUE,file="jpg",memo="bh",
    ,dpi=300,file.output=TRUE,verbose=TRUE)#QQ图
CMplot(pvalue, plot.type="m", LOG10=TRUE, ylim=NULL, threshold=c(0.05,1)/1004599,threshold.lty=c(1,2),
threshold.lwd=c(1,1), threshold.col=c("black","grey"), amplify=TRUE,bin.size=1e6,
signal.col=c("red","green"),signal.cex=c(1,1),
signal.pch=c(19,19),file="jpg",memo="bh",dpi=300,file.output=TRUE,verbose=TRUE)
