from fileWork import *
from matplotlib import animation
from matplotlib.pyplot import *
from sklearn.decomposition import PCA

dataset = load_data('data.txt')  # загрузка данных
rows = len(dataset)  # кол-во строк в данных

mas = min_max(dataset, rows)  # нахождение min и max данных
min = mas[0]
max = mas[1]

data_norm = normalization(dataset, min, max, rows, mas)  # нормализация данных
f = open('data_norm.txt', 'w')
for i in range(len(data_norm)):
    f.write(str(data_norm[i]))  # сохранение нормальных данных
f.close()

centroids_history=[]
lables_history=[]

#elbow_method(6, data_norm, centroids_history, lables_history, mas)

last_lable=KMeans(3, data_norm, centroids_history, lables_history, mas)

#print(centroids_history)
print(last_lable)
#print(lables_history)
#print(centroids_history)

model_points = PCA(n_components=2)
model_points.fit(data_norm)
data_2D= model_points.transform(data_norm)
x_points_2D=[]
y_points_2D=[]
slicing_points(data_2D, x_points_2D , y_points_2D )


#model_centroids = PCA(n_components=2)
#model_centroids.fit(centroids_history)
#centroids_2D=model_centroids.transform(centroids_history)
#x_centroid_2D=[]
#y_centroid_2D=[]
#slicing_centroids(centroids_history, x_centroid_2D, y_centroid_2D)


fig=figure()
def animate(i):
    clf()
    j=i*2
    ylabel('average of fans')
    xlabel('average of goals')

    #x_centers=[]
    #y_centers=[]
   # m = 0
   # for l in range(len(centroids_history[0])):
    #    x_centers.append(x_centroid_2D[j+m])
     #   y_centers.append(y_centroid_2D[j+m])
      #  m+=1

    #axes = gca()
    #axes.set_xlim([-0.0001, 0.005])
    scatter(x_points_2D, y_points_2D, c=lables_history[i],s=1, cmap='rainbow',alpha=0.8)
    #scatter(x_centers, y_centers,s=80, marker='*', c='black')


anim = animation.FuncAnimation(fig,animate,frames=len(lables_history), interval=1000, repeat=False)
show()