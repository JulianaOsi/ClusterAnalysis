from functions import distance, KMeans
from matplotlib.pyplot import plot, show


def inertia_(lable, last_centroids, data_norm):
    """
    Нахождение критерия суммарной квадратичности внутри кластеров
    :param lable: массив меток
    :param last_centroids: массив координат итоговых центройдов
    :param data_norm: матрица данных
    :return: значение инерции
    """
    value = 0
    i = 0
    for elem in lable:  # пробег по каждой метке
        dist = distance(data_norm[i], last_centroids[elem])  # вычисление расстояния от точки до ее центройда
        value += dist  # прибавление расстояния к значению инерции
        i += 1  # счетчик точек
    return value


def elbow_method(max_k, data_norm, centroids_history, lables_history):
    """
    Метод локтей для нахождения оптимального количества кластеров
    :param max_k: максимальное кол-во возможных кластеров
    :param data_norm: матрица данных
    :param centroids_history: история центройдов
    :param lables_history: история меток
    """
    inertia = []  # массив всех инерций
    for i in range(1, max_k):  # цикл по кол-ву кластеров
        last_lable = KMeans(i, data_norm, centroids_history, lables_history)  # метод К-средних для данного  k
        value = inertia_(last_lable, centroids_history[len(centroids_history)-1], data_norm)  # значение инерции
        inertia.append(value)  # добавление значения инерции в массив
        centroids_history.clear()  # очистка истории центройдов
        lables_history.clear()  # очистка истории меток

    plot(range(1, max_k), inertia, marker='s')  # построение графика метода локтей
    show()  # показ графика

