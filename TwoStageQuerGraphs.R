library(ggplot2)

legend = rep(c("Random", "Maximize", "Two-Stage"), 10)
legend

################################ Variable Number of Incidents ###############################################################
x_axis = c()
x_levels = c()
for (i in seq(10, 100, by=10)) {
expr = paste(c("Inc = ", i), collapse = " ")
x_levels = c(x_levels, expr)
repititions = rep(expr, 3 )
x_axis = c(x_axis, repititions)  
}
x_axis
x_levels
dat = data.frame(
                Query_type = factor(legend, levels = c("Random", "Maximize", "Two-Stage")),
                Neighbors_Cnt = c(19, 17, 24, 48, 42, 50, 56, 45, 62, 81, 56, 82, 93, 95, 160, 121, 87, 129, 134, 118, 160, 153, 124, 190, 177, 153, 178, 205, 147, 247),
                Incident_Cnt = factor(x_axis, levels = x_levels)
                
)

dat
ggplot(data=dat, aes(x=Incident_Cnt, y=Neighbors_Cnt, fill=Query_type)) +
  geom_bar(stat="identity", position=position_dodge())

################################ Variable Crowd #########################################################
x_axis = c()
x_levels = c()
for (i in seq(10, 100, by=10)) {
  expr = paste(c("Crowd = ", i), collapse = " ")
  x_levels = c(x_levels, expr)
  repititions = rep(expr, 3 )
  x_axis = c(x_axis, repititions)  
}
x_axis
x_levels
dat = data.frame(
  Query_type = factor(legend, levels = c("Random", "Maximize", "Two-Stage")),
  Neighbors_Cnt = c(500, 500, 400, 261, 182, 218, 167, 131, 185, 126, 87, 140, 88, 86, 110, 84, 63, 104, 76, 56, 71, 67, 51, 76, 44, 48, 51, 50, 41, 70),
  Crowd_Cnt = factor(x_axis, levels = x_levels)
  
)

dat
ggplot(data=dat, aes(x=Crowd_Cnt, y=Neighbors_Cnt, fill=Query_type)) +
  geom_bar(stat="identity", position=position_dodge())
################################ Variable Number of People to query #########################################################
x_axis = c()
x_levels = c()
for (i in seq(10, 100, by=10)) {
  expr = paste(c("Quer = ", i), collapse = " ")
  x_levels = c(x_levels, expr)
  repititions = rep(expr, 3 )
  x_axis = c(x_axis, repititions)  
}
x_axis
x_levels
dat = data.frame(
  Query_type = factor(legend, levels = c("Random", "Maximize", "Two-Stage")),
  Neighbors_Cnt = c(27, 21, 21, 39, 41, 52, 76, 79, 115, 96, 111, 150, 130, 116, 175, 138, 142, 190, 171, 177, 210, 197, 196, 215, 223, 226, 235, 250, 250, 230),
  Quer_Cnt = factor(x_axis, levels = x_levels)
  
)

dat
ggplot(data=dat, aes(x=Quer_Cnt, y=Neighbors_Cnt, fill=Query_type)) +
  geom_bar(stat="identity", position=position_dodge())
################################ Variable First Stage Percentage x*t #########################################################
x_axis = c()
x_levels = c()
for (i in seq(10, 100, by=10)) {
  expr = paste(c("Quer = ", i), collapse = " ")
  x_levels = c(x_levels, expr)
  repititions = rep(expr, 3 )
  x_axis = c(x_axis, repititions)  
}
x_axis
x_levels
dat = data.frame(
  Query_type = factor(legend, levels = c("Random", "Maximize", "Two-Stage")),
  Neighbors_Cnt = c(27, 21, 21, 39, 41, 52, 76, 79, 115, 96, 111, 150, 130, 116, 175, 138, 142, 190, 171, 177, 210, 197, 196, 215, 223, 226, 235, 250, 250, 230),
  Quer_Cnt = factor(x_axis, levels = x_levels)
  
)

dat
ggplot(data=dat, aes(x=Quer_Cnt, y=Neighbors_Cnt, fill=Query_type)) +
  geom_bar(stat="identity", position=position_dodge())

