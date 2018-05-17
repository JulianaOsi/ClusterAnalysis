from math import sqrt
from random import randint
from matplotlib.pyplot import show, plot, figure, clf, xlabel, ylabel, gca, scatter

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

def min_max(data, rows):
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

def fillZero(x, y, mas):
    mas = []
    for i in range(x):
        mas.append([])
        for j in range(y):
            mas[i].append(0)
    return mas

def normalization(data, min, max, rows, mas):
    """Нормализация данных. Принимает массив данных, минимальное
    и максимальное значения в данных. Возвращает нормализованный
    массив данных

    """
    data_norm = fillZero(rows, 2, mas)  # заполнение массива нулями
    for i in range(rows):
        for k in range(2):
            x = ((data[i][k] - min) / (max - min))

            data_norm[i][k] = float(x)
    return data_norm

def distance(first, second):
    return sqrt((first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2)

def randcenter(k, data_norm):

    mas = []
    rang = len(data_norm)
    use = set()
    rand = randint(0, rang - 1)
    for i in range(k):
        use.add(rand)
        mas.append(data_norm[rand])
        rand = randint(0, rang - 1)
        while rand in use:
            rand = randint(0, rang - 1)
    return mas

def findlables(rand_c, data_norm, mas):
    distancemas = fillZero(len(data_norm), 2, mas)
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

def findcenter(lables, k, data_norm):
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

def KMeans(k, data_norm, centroids_history, lables_history, mas):
    centroids = randcenter(k, data_norm)
    centroids_history.append(centroids)
    actual_lable = findlables(centroids, data_norm, mas)
    lables_history.append(actual_lable)
    while not (findcenter(actual_lable, k, data_norm) == centroids):
        centroids = findcenter(actual_lable, k, data_norm)
        centroids_history.append(centroids)
        actual_lable = findlables(centroids, data_norm, mas)
        lables_history.append(actual_lable)

    return actual_lable

def inertia_(lable,last_centroids, data_norm):
    value =0
    i=0
    for elem in lable:
        dist = distance(data_norm[i],last_centroids[elem])
        value+=dist
        i+=1

    return value

def elbow_method(max_k, data_norm, centroids_history, lables_history, mas):
    inertia=[]
    for i in range(1,max_k):
        last_lable=KMeans(i, data_norm, centroids_history, lables_history, mas)
        value=inertia_(last_lable,centroids_history[len(centroids_history)-1], data_norm)
        inertia.append(value)
        centroids_history.clear()
        lables_history.clear()

    plot(range(1,max_k),inertia,marker='s')
    show()

def slicing_points(data_norm, x_points, y_points):

    for point in data_norm:
            x_points.append(point[0])
            y_points.append(point[1])

def slicing_centroids(centroids_history, x_centroid, y_centroid):
    for c in centroids_history:
        for i in range(len(c)):
            x_centroid.append(c[i][0])
            y_centroid.append(c[i][1])




