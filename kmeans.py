import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import *


def load_data(file_name):
    """Метод для загрузки данных из txt файла.
    Принимает имя файла. Возвращает массив данных.

    """
    f = open(file_name, 'r')
    mas = []
    for i in f:
        mas.append(list(map(int, i.split())))
    f.close()
    return mas


dataset = load_data('data.txt')  # загрузка данных
rows = len(dataset)  # кол-во строк в данных


def min_max(data):
    """Вычисление минимального и максимального значений в данных.
    Принимает массив данных. Возвращает список из минимального
    и максимального значений

    """
    max = 0
    min = data[0][0]
    for i in range(rows):
        for k in range(2):
            if data[i][k] > max:
                max = data[i][k]
            if data[i][k] < min:
                min = data[i][k]

    return [min, max]


mas = min_max(dataset)  # нахождение min и max данных
min = mas[0]
max = mas[1]


def fillZero(x, y):
    mas = []
    for i in range(x):
        mas.append([])
        for j in range(y):
            mas[i].append(0)
    return mas


def normalization(data, min, max):
    """Нормализация данных. Принимает массив данных, минимальное
    и максимальное значения в данных. Возвращает нормализованный
    массив данных

    """
    data_norm = fillZero(rows, 2)  # заполнение массива нулями
    for i in range(rows):
        for k in range(2):
            x = ((data[i][k] - min) / (max - min))

            data_norm[i][k] = float(x)
    return data_norm


data_norm = normalization(dataset, min, max)  # нормализация данных
f = open('data_norm.txt', 'w')
for i in range(len(data_norm)):
    f.write(str(data_norm[i]))  # сохранение нормальных данных
f.close()


def distance(first, second):
    return sqrt((first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2)


def randcenter(k):

    mas = []
    rang = len(data_norm)
    use = set()
    rand = random.randint(0, rang - 1)
    for i in range(k):
        use.add(rand)
        mas.append(data_norm[rand])
        rand = random.randint(0, rang - 1)
        while rand in use:
            rand = random.randint(0, rang - 1)
    return mas


def findlables(rand_c):
    distancemas = fillZero(len(data_norm), 2)
    for i in range(len(data_norm)):
        distancemas[i] = [distance(rand_c[0], data_norm[i]), 0] #?
        for j in range(len(rand_c)):
            dist = [distance(rand_c[j], data_norm[i]), j]
            if distancemas[i][0] > dist[0]:
                distancemas[i] = dist
    a = []
    for i in distancemas:
        a.append(i[1])
    return a


def findcenter(lables, k):
    mas = []
    for i in range(k):
        sumx = 0
        sumy = 0
        ch = 0
        for j in range(len(data_norm)):
            if lables[j] == i:

                ch += 1
                sumx += data_norm[j][0]
                sumy += data_norm[j][1]
        mas.append([sumx / ch, sumy / ch])
    return mas


centroids_history=[]
lables_history=[]


def KMeans(k):
    centroids = randcenter(k)
    centroids_history.append(centroids)
    actual_lable = findlables(centroids)
    lables_history.append(actual_lable)
    while not (findcenter(actual_lable, k) == centroids):
        centroids = findcenter(actual_lable, k)
        centroids_history.append(centroids)
        actual_lable = findlables(centroids)
        lables_history.append(actual_lable)

    return actual_lable


def inertia_(lable,last_centroids):
    value =0
    i=0
    for elem in lable:
        dist = distance(data_norm[i],last_centroids[elem])
        value+=dist
        i+=1

    return value


def elbow_method(max_k):
    inertia=[]
    for i in range(1,max_k):
        last_lable=KMeans(i)
        value=inertia_(last_lable,centroids_history[len(centroids_history)-1])
        inertia.append(value)
        centroids_history.clear()
        lables_history.clear()

    plt.plot(range(1,max_k),inertia,marker='s')
    plt.show()

elbow_method(5)

last_lable=KMeans(2)

#print(centroids_history)
print(last_lable)
#print(lables_history)

x_points = []
y_points = []
def slicing_points():

    for point in data_norm:
            x_points.append(point[0])
            y_points.append(point[1])

slicing_points()


x_centroid=[]
y_centroid=[]
def slicing_centroids():
    for c in centroids_history:
        for i in range(len(c)):
            x_centroid.append(c[i][0])
            y_centroid.append(c[i][1])

slicing_centroids()

fig=plt.figure()
def animate(i):
    plt.clf()
    j=i*2
    plt.ylabel('average of fans')
    plt.xlabel('average of goals')

    x_centers=[]
    y_centers=[]
    m = 0
    for l in range(len(centroids_history[0])):
        x_centers.append(x_centroid[j+m])
        y_centers.append(y_centroid[j+m])
        m+=1

    axes = plt.gca()
    axes.set_xlim([-0.0001, 0.005])
    plt.scatter(x_points, y_points, c=lables_history[i], cmap='rainbow',alpha=0.8)
    plt.scatter(x_centers, y_centers,s=80, marker='*', c='black')


anim = animation.FuncAnimation(fig,animate,frames=len(lables_history), interval=1000, repeat=False)
plt.show()