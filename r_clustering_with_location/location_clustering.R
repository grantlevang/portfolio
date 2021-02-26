#Reading in

df = data.table::fread("location.csv")
head(df)

#Isolating the co-ordinate data from the rest of the data frame
co_ords = df[,3:4]

#Quick exploratory plot to see what we're working with
plot(co_ords)

#Find optimal number of clusters
center_nos = data.frame(NULL)
names(center_nos) = c("Centers", "Sum of Squares Within Clusters")
for (centers in c(1:10)){
  clusters = kmeans(co_ords, centers=centers, iter.max=100, algorithm = "Hartigan-Wong")
  WSS = clusters$tot.withinss
  center_nos = rbind(center_nos, data.frame(Centers=centers, TotalWSS=WSS))
}

center_nos

#Use elbow plot to find optimal number of clusters
plot(center_nos[,1], center_nos[,2], type="b", main="Elbow Plot", ylab="Within Cluster SS",xlab="Number of clusters")

#Optimal may be 4, 5 or 6

#Assign a cluster to each observation using 4 and 5 clusters
clusters4 = kmeans(co_ords, centers=4, iter.max=100, algorithm = "Hartigan-Wong")
clusters5 = kmeans(co_ords, centers=5, iter.max=100, algorithm = "Hartigan-Wong")
clusters6 = kmeans(co_ords, centers=6, iter.max=100, algorithm = "Hartigan-Wong")

df[,"cluster_w_4centers"] = factor(clusters4$cluster)
df[,"cluster_w_5centers"] = factor(clusters5$cluster)
df[,"cluster_w_6centers"] = factor(clusters6$cluster)

centers_4 = cbind(as.data.frame(clusters4$centers), centers = factor(c(1,2,3,4)))
centers_5 = cbind(as.data.frame(clusters5$centers), centers = factor(c(1,2,3,4,5)))
centers_6 = cbind(as.data.frame(clusters6$centers), centers = factor(c(1,2,3,4,5,6)))

#Visualization
install.packages("ggplot2")
library(ggplot2)
#4 centers plot
gg4 = ggplot(df, aes(x=latitude, y=longitude, color=cluster_w_4centers)) + geom_point() +
  geom_point(data=centers_4, aes(x=latitude, y=longitude, color=centers)) +
  geom_point(data=centers_4, aes(x=latitude, y=longitude, color=centers), size=60, alpha=0.1, show.legend=FALSE) + 
  stat_ellipse() + theme_bw()
gg4

#5 centers plot
gg5 = ggplot(df, aes(x=latitude, y=longitude, color=cluster_w_5centers)) + geom_point() +
  geom_point(data=centers_5, aes(x=latitude, y=longitude, color=centers)) +
  geom_point(data=centers_5, aes(x=latitude, y=longitude, color=centers), size=60, alpha=0.1, show.legend=FALSE) + 
  stat_ellipse() + theme_bw()
gg5

#6 centers plot
gg6 = ggplot(df, aes(x=latitude, y=longitude, color=cluster_w_6centers)) + geom_point() +
  geom_point(data=centers_6, aes(x=latitude, y=longitude, color=centers)) +
  geom_point(data=centers_6, aes(x=latitude, y=longitude, color=centers), size=60, alpha=0.1, show.legend=FALSE) + 
  stat_ellipse() + theme_bw()
gg6

#Model with 5 centers separates a distinct cluster


#DBSCAN approach - just out of interest
# install.packages("fpc")
# install.packages("dbscan")
# 
# db = fpc::dbscan(co_ords, eps = 1.3, MinPts = 5)
# 
# plot(db, co_ords, main="DBSCAN", frame=F)
# 
# 
# install.packages("factoextra")
# factoextra::fviz_cluster(db, co_ords, stand=F, frame=F, geom="point")

