"""
Модуль состоит из функций, необходимых для реализации кластерного анализа.
Также содержится функция кластеризации методом k-средних.
"""
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
    Выбор случайных центроидов для каждого кластера
    :param k: кол-во кластеров
    :param data_norm: матрица данных
    :return: координаты случайных цетроидов
    """
    coordinates = []  # массив координат случайных центроидов
    rang = len(data_norm)  # кол-во строк в матрице данных
    use = set()  # создание множества использованных чисел
    rand = randint(0, rang - 1)  # генерация рандомного числа
    for i in range(k):  # пробег цикла от 1 до кол-ва кластеров
        use.add(rand)   # добавление использованного числа в множество
        coordinates.append(data_norm[rand])  # добавление координат центроида в список
        rand = randint(0, rang - 1)
        while rand in use:  # проверка числа на нахождение во множестве использованных
            rand = randint(0, rang - 1)
    return coordinates


def findLables(centroids, data_norm):
    """
    Определение меток точек (принадлежность точек к кластерам)
    :param centroids: массив центроидов каждого кластера
    :param data_norm: матрица данных
    :return: массив меток

    distance_mas - массив расстяний от каждой точки к ближайшему ей центроиду
    """
    distance_mas = fillZero(len(data_norm), 2)  # заполнение массива расстояний нулями
    for i in range(len(data_norm)):  # пробег по всем точкам
        distance_mas[i] = [distance(centroids[0], data_norm[i]), 0]  # расстояние от точки до первого центроида
        for j in range(len(centroids)):  # пробег по каждому центроиду
            dist = [distance(centroids[j], data_norm[i]), j]  # расстояние от каждого центроида до точки, индекс кластера
            if distance_mas[i][0] > dist[0]:  # нахождение наиболее близкого центроида к точке
                distance_mas[i] = dist
    lables_mas = []
    for i in distance_mas:  # пробег по массиву расстояний
        lables_mas.append(i[1])  # заполнение массива меток индексами ближайших центроидов
    return lables_mas


def findCenter(lables, k, data_norm):
    """
    Вычисление новых центроидов
    :param lables: массив принадлежности точек к кластерам
    :param k: кол-во кластеров
    :param data_norm: матрица данных
    :return: массив координат новых центроидов
    """
    coordinates = []  # массив координат новых центроидов
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
    :param centroids_history: массив истории координат центроидов
    :param lables_history: массив истории меток точек
    :return: итоговый массив меток (принадлежности точек к кластерам)
    """
    centroids = randCenter(k, data_norm)  # нахождение случайных центроидов
    centroids_history.append(centroids)  # добавление случайных центроидов в историю
    actual_lable = findLables(centroids, data_norm)  # вычисление актуального массива меток
    lables_history.append(actual_lable)  # добавление массива актуальных меток в историю
    while not (findCenter(actual_lable, k, data_norm) == centroids):  # пока новые центроиды не совпадают с предыдущими
        centroids = findCenter(actual_lable, k, data_norm)  # нахождение новых центроидов
        centroids_history.append(centroids)  # добавление новых центроидов в историю
        actual_lable = findLables(centroids, data_norm)  # вычисление актуального массива меток
        lables_history.append(actual_lable)  # добавление актуальных меток в историю

    return actual_lable


def slicing_points(data_norm, x_points, y_points):
    """
    Разделение координат Х и Y всех точек по разным массивам
    :param data_norm: матрица данных
    :param x_points: пустой массив для записи координат Х
    :param y_points: пустой массив для записи координат Y
    """
    for point in data_norm:
            x_points.append(point[0])  # добавление координаты X
            y_points.append(point[1])  # добавление координаты Y

