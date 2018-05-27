from functions import *
from matplotlib import animation
from matplotlib.pyplot import *
from sklearn.decomposition import PCA
from elbowMethod import elbow_method

dataset = load_data('data.txt')  # загрузка данных
rows = len(dataset)  # кол-во строк в данных

mas = min_max(dataset, rows)  # нахождение min и max данных
min = mas[0]
max = mas[1]

data_norm = normalization(dataset, min, max, rows)  # нормализация данных
f = open('data_norm.txt', 'w')  # открытие файла для записи данных
for i in range(len(data_norm)):  # пробег по всем строкам данных
    f.write(str(data_norm[i]))  # сохранение нормальных данных
f.close()  # закрытие файла

centroids_history = []  # массив истории центройдов
lables_history = []  # массив истории меток

elbow_method(6, data_norm, centroids_history, lables_history)  # выполнение метода локтей

last_lable = KMeans(3, data_norm, centroids_history, lables_history)  # выполнение алгоритма К-средних

#print(centroids_history)
print(last_lable)
#print(lables_history)
#print(centroids_history)


"""
Метод главных компонент (PCA) для понижения размерности данных.
Уменьшение до 2D пространства.
"""
model_points = PCA(n_components=2)
model_points.fit(data_norm)
data_2D = model_points.transform(data_norm)  # массив координат 2D пространства

x_points_2D = []  # массив координат Х всех точек
y_points_2D = []  # массив координат Y всех точек
slicing_points(data_2D, x_points_2D, y_points_2D)  # разделение координат

fig = figure()  #создание окна для графика


def animate(i):
    clf()  # очищение графика
    #j=i*2
    ylabel('name')  # название оси Y
    xlabel('name')  # название оси X

    """
    #x_centers=[]
    #y_centers=[]
   # m = 0
   # for l in range(len(centroids_history[0])):
    #    x_centers.append(x_centroid_2D[j+m])
     #   y_centers.append(y_centroid_2D[j+m])
      #  m+=1

    #axes = gca()
    #axes.set_xlim([-0.0001, 0.005])
    """

    scatter(x_points_2D, y_points_2D, c=lables_history[i],s=1, cmap='rainbow',alpha=0.8)  # построение графика точек
    #scatter(x_centers, y_centers,s=80, marker='*', c='black')


anim = animation.FuncAnimation(fig,animate,frames=len(lables_history), interval=1000, repeat=False)  # анимация графика
show()  # показ графика