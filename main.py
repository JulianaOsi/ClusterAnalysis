"""
Модуль исполняет функции других модулей.
"""
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

centroids_history = []  # массив истории центроидов
lables_history = []  # массив истории меток

elbow_method(6, data_norm, centroids_history, lables_history)  # выполнение локтевого метода

last_lable = KMeans(3, data_norm, centroids_history, lables_history)  # выполнение алгоритма К-средних


print(last_lable)  # печать меток


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
    scatter(x_points_2D, y_points_2D, c=lables_history[i],s=1, cmap='rainbow',alpha=0.8)  # построение графика точек


anim = animation.FuncAnimation(fig,animate,frames=len(lables_history), interval=1000, repeat=False)  # анимация графика
show()  # показ графика

