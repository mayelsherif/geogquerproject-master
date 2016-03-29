mat_size = 10;
average_over = 100;
cluster_cnt = 5;
incident_cnt = 100;

% Used for commenting multiple lines

for n = 1:average_over
    M = randi(2, mat_size); 
    M = M -1;
    M
    dlmwrite('matrices.txt', M, '-append')
end
    

% -----------------------Generate clustered data
% ---------------------------------

%{
Inputs:

slope - Base direction of the lines on which clusters are based. 
slopeStd - Standard deviation of the slope; used to obtain a random slope variation from the normal distribution, which is added to the base slope in order to obtain the final slope of each cluster. 
numClusts - Number of clusters (and therefore of lines) to generate. 
xClustAvgSep - Average separation of line centers along the X axis. 
yClustAvgSep - Average separation of line centers along the Y axis. 
lengthAvg - The base length of lines on which clusters are based. 
lengthStd - Standard deviation of line length; used to obtain a random length variation from the normal distribution, which is added to the base length in order to obtain the final length of each line. 
lateralStd - "Cluster fatness", i.e., the standard deviation of the distance from each point to the respective line, in both x and y directions; this distance is obtained from the normal distribution. 
totalPoints - Total points in generated data (will be randomly divided among clusters).


Outputs:

data - Matrix (totalPoints x 2) with the generated data 
clustPoints - Vector (numClusts x 1) containing number of points in each cluster 
idx - Vector (totalPoints x 1) containing the cluster indices of each point 
centers - Matrix (numClusts x 2) containing centers from where clusters were generated 
slopes - Vector (numClusts x 1) containing the effective slopes used to generate clusters 
lengths - Vector (numClusts x 1) containing the effective lengths used to generate clusters
%}


op_end = 10;
op_start = 0;
file = strcat('matrixClust',int2str(cluster_cnt), '.txt') 
for n = 1:average_over
%Third Varibale is the number of clusters
%Last item is the number of points
[data cp idx] = generateData(1, 0.5, cluster_cnt, 15, 15, 5, 1, 2, incident_cnt);
%Inputs: slope (1), slopeStd (2), numClusts (3), xClustAvgSep (4),
%yClustAvgSep (5), lengthAvg (6), lengthStd (7), totalPoints (8)
% ------------------------------
%This creates 5 clusters with a total of 200 points, with a base slope of 1 (std=0.5),
%separated in average by 15 units in both x and y directions, with average length of 5 units (std=1)
%and a "fatness" or spread of 2 units.
x = data(:,1);
x_start = min(x);
x_end = max(x);
x_new = op_start + ((op_end - op_start)/(x_end - x_start))* (x - x_start)

y = data(:,2);
y_start = min(y);
y_end = max(y);
y_new = op_start + ((op_end - op_start)/(y_end - y_start))* (y - y_start)


x_new
y_new
idx
subplot(2,1,1)
scatter(data(:,1), data(:,2), 8, idx);
subplot(2,1,2)
scatter(x_new, y_new, 8, idx);
max(x_new)
max(y_new)

M(:,1) = x_new
M(:,2) = y_new 
M
if n == 1
   dlmwrite(file, M);
else
  dlmwrite(file, M, '-append');  
end

end
