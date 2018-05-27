from math import sqrt
from random import randint
import linkedList


def load_data(file_name):
    """
    Загрузка данных из txt файла.
    :param file_name: имя файла
    :return: матрица данных
    """
    f = open(file_name, 'r')  # открытие файла
    data = []  # массив для данных
    for i in f:  # пробег по строкам файла
        data.append(list(map(int, i.split())))  # добавление каждой точки в массив данных
    f.close()  # закрытие файла
    return data


def min_max(data, rows):
    """
    Вычисление минимального и максимального значений в данных.
    :param data: матрица данных
    :param rows: кол-во строк в данных
    :return:  минимальное и максимальное значения
    """
    max = 0
    min = data[0][0]
    for i in range(rows):  # пробег по всем строкам данных
        for k in range(34):  # пробег по всем колонкам данных
            if data[i][k] > max:  # поиск максимального
                max = data[i][k]
            if data[i][k] < min:  # поиск минимального
                min = data[i][k]

    return [min, max]


def fillZero(rows, columns):
    """
    Заполнение матрицы нулями
    :param rows: кол-во строк матрицы
    :param columns: кол-во столбцов матрицы
    :return: матрица,заполненный нулями
    """
    null_matrix = []  # нулевая матрица
    for i in range(rows):  # пробег по всем строкам
        null_matrix.append([])  # добавление строки в матрицу
        for j in range(columns):  # пробег по всем колонкам
            null_matrix[i].append(0)  # добавление нулевого элемента
    return null_matrix


def normalization(data, min, max, rows):
    """
    Нормализация данных.
    :param data: матрица данных
    :param min: минимальное значение в данных
    :param max: максимальное значение в данных
    :param rows: кол-во колонок
    :return: нормализованная матрица данных
    """

    data_norm = fillZero(rows, 34)  # заполнение матрицы нулями
    for i in range(rows):  # пробег по всем строкам
        for k in range(34):  # пробег по всем колонкам
            x = ((data[i][k] - min) / (max - min))  # нормализация
            data_norm[i][k] = float(x)  # приведение к вещественному типу
    return data_norm


def distance(first, second):
    """
    Нахождение расстояния между двумя точками
    :param first: координаты первой точки
    :param second: координаты второй точки
    :return: расстояние между точками
    """
    return sqrt((first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2)


def randCenter(k, data_norm):
    """
    Генерация случайных центройдов для каждого кластера
    :param k: кол-во кластеров
    :param data_norm: матрица данных
    :return: координаты случайных цетройдов
    """
    coordinates = []  # массив координат случайных центройдов
    rang = len(data_norm)  # кол-во строк в матрице данных
    use = set()  # создание множества использованных чисел
    rand = randint(0, rang - 1)  # генерация рандомного числа
    for i in range(k):  # пробег цикла от 1 до кол-ва кластеров
        use.add(rand)   # добавление использованного числа в множество
        coordinates.append(data_norm[rand])  # добавление координат центройда в список
        rand = randint(0, rang - 1)
        while rand in use:  # проверка числа на нахождение во множестве использованных
            rand = randint(0, rang - 1)
    return coordinates


def findLables(centroids, data_norm):
    """
    Определение меток точек (принадлежность точек к кластерам)
    :param centroids: массив центройдов каждого кластера
    :param data_norm: матрица данных
    :return: массив меток

    distance_mas - массив расстяний от каждой точки к ближайшему ей центройду
    """
    distance_mas = fillZero(len(data_norm), 2)  # заполнение массива расстояний нулями
    for i in range(len(data_norm)):  # пробег по всем точкам
        distance_mas[i] = [distance(centroids[0], data_norm[i]), 0]  # расстояние от точки до первого центройда
        for j in range(len(centroids)):  # пробег по каждому центройду
            dist = [distance(centroids[j], data_norm[i]), j]  # расстояние от каждого центройда до точки
            if distance_mas[i][0] > dist[0]:  # нахождение наиболее близкого центройда к точке
                distance_mas[i] = dist
    lables_mas = []
    for i in distance_mas:  # пробег по массиву расстояний
        lables_mas.append(i[1])  # заполнение массива меток индексами ближайших центройдов
    return lables_mas


def findCenter(lables, k, data_norm):
    """
    Вычисление новых центройдов
    :param lables: массив принадлежности точек к кластерам
    :param k: кол-во кластеров
    :param data_norm: матрица данных
    :return: массив координат новых центройдов
    """
    coordinates = []  # массив координат новых центройдов
    for i in range(k):  # пробег по всем кластерам
        sumx = 0
        sumy = 0
        ch = 0
        for j in range(len(data_norm)):  # пробег по всем точкам данных
            if lables[j] == i:  # условие принадлежности точки к кластеру
                ch += 1  # счетчик кол-ва точек в кластере
                sumx += data_norm[j][0]  # сумма координат Х точек кластера
                sumy += data_norm[j][1]  # сумма координат Y точек кластера
        coordinates.append([sumx / ch, sumy / ch])  # среднее всех точек каждого кластера
    return coordinates


def KMeans(k, data_norm, centroids_history, lables_history):
    """
    Выполнение алгоритма K-средних
    :param k: кол-во кластеров
    :param data_norm: матрица данных
    :param centroids_history: массив истории координат центройдов
    :param lables_history: массив истории меток точек
    :return: итоговый массив меток (принадлежности точек к кластерам)
    """
    centroids = randCenter(k, data_norm)  # нахождение случайных центройдов
    centroids_history.append(centroids)  # добавление случайных центройдов в историю
    actual_lable = findLables(centroids, data_norm)  # вычисление актуального массива меток
    lables_history.append(actual_lable)  # добавление массива актуальных меток в историю
    while not (findCenter(actual_lable, k, data_norm) == centroids):  # пока новые центройды не совпадают с предыдущими
        centroids = findCenter(actual_lable, k, data_norm)  # нахождение новых центройдов
        centroids_history.append(centroids)  # добавление новых центройдов в историю
        actual_lable = findLables(centroids, data_norm)  # вычисление актуального массива меток
        lables_history.append(actual_lable)  # добавление актуальных меток в историю

    return actual_lable


def slicing_points(data_norm, x_points, y_points):
    """
    Разделение координат Х и Y всех точек по разным массивам
    :param data_norm: матрица данных
    :param x_points: пустой массив координат Х
    :param y_points: пустой массив координат Y
    """
    for point in data_norm:
            x_points.append(point[0])  # добавление координаты X
            y_points.append(point[1])  # добавление координаты Y


def slicing_centroids(centroids_history, x_centroid, y_centroid):
    """
    Разделение координат Х и У всех центройдов по разным массивам
    :param centroids_history: матрица истории координат центройдов
    :param x_centroid: пустой массив координат Х
    :param y_centroid: пустой массив координат Y
    :return:
    """
    for c in centroids_history:  # пробег по всем центройдам в истории
        for i in range(len(c)):  # пробег по каждой координате центройда
            x_centroid.append(c[i][0])  # добавление координаты X
            y_centroid.append(c[i][1])  # добавление координаты Y
