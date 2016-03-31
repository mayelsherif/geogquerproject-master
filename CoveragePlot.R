library(ggplot2)

clust_cnt = c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)


firstStage_0.2 = c(61.84, 77.05, 78.21, 77.65, 72.16, 70.9, 65.78, 67, 66.94, 65.98)
firstStage_0.2_rounded = c(62, 77, 78, 78, 72, 71, 66, 67, 67, 66)

firstStage_0.4 = c(77.27, 82.53, 89.98, 89.15, 88.97, 85.54, 84.41, 84.58, 82.55, 82.17)
firstStage_0.4_rounded = c(77, 83, 90, 89, 89, 86, 84, 85, 83, 82)

firstStage_0.6 = c(83.55, 87.26, 88.37, 90.94, 92.6, 90.73, 89.56, 86.78, 87.18, 86.85)
firstStage_0.6_rounded = c(84, 87, 88, 91, 93, 91, 90, 87, 87, 87)

firstStage_0.8 = c(86.29, 86.95, 88.37, 89.42, 91.37, 91.15, 89.21, 88.35, 89.75, 89.29)
firstStage_0.8_rounded = c(86, 87, 88, 89, 91, 91, 89, 88, 90, 89)


df1 <- data.frame(Clust_Cnt = factor(c(rep(clust_cnt, 4))),
                  Incident_Coverage = c(firstStage_0.2_rounded, firstStage_0.4_rounded, firstStage_0.6_rounded, firstStage_0.8_rounded), 
                  Query_type = factor(rep(c("FSP = 20%","FSP = 40%","FSP = 60%","FSP = 80%"), each=10)))
df1


# Map sex to color
ggplot(data=df1, aes(x=Clust_Cnt, y=Incident_Coverage, group=Query_type, colour=Query_type)) +
  geom_line(size=1.5) +
  geom_point(size=3)+
  labs(x = "Number of clusters", y = "Incident Coverage", linetype='Query Type:')+
  theme(axis.title.y = element_text(size = 16, face = 'bold'), axis.title.x = element_text(size = 16, face = 'bold'), axis.text.x = element_text(size = 14, face = 'bold'))+
  scale_fill_discrete(name = "Query Type:") + theme(legend.text=element_text(size=16, face = 'bold'), legend.title = element_text(size=16, face = 'bold')) + theme(legend.position="top")







### reshape this to give a column indicating group
#df2 <- with(df1,
 #           as.data.frame(cbind( c(clust_cnt_0.2, clust_cnt_0.4, clust_cnt_0.6, clust_cnt_0.8),
#                                 c(firstStage_0.2, firstStage_0.4, firstStage_0.6, firstStage_0.8),
 #                                rep(c("firstStage0.2","firstStage0.4","firstStage0.6","firstStage0.8"), each=10) )
  #          ))
#colnames(df2) <- c("Cluster_Count","Spatial_Coverage","Querying_Technique_Variations")
#df2$Querying_Technique_Variations <- as.factor(df2$Querying_Technique_Variations)
#ggplot(df2, aes(Cluster_Count)) + geom_line(aes(y= Spatial_Coverage))


#df1 = data.frame(firstStage_0.2, firstStage_0.4, firstStage_0.6, firstStage_0.8)

#ggplot(df1, aes(clust_cnt)) + 
#  geom_line(aes(y = firstStage_0.2)) + 
#  geom_line(aes(y = firstStage_0.4)) +
#  geom_line(aes(y = firstStage_0.6)) + 
#  geom_line(aes(y = firstStage_0.8)) 
