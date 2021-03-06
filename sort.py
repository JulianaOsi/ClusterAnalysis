"""
Модуль содержит алгоритмы сортировки массивов
"""


def shellSort(arr):
    """
    Сортировка методом Шелла
    :param arr: массив, который нужно отсортировать
    Результатом работы является отсортированный массив
    """
    n = len(arr)    #подсчёт размерности массива
    gap = n // 2     #устанавливается большой зазор, который затем уменьшается
    while gap > 0:  #сортировка идёт, пока зазор положителен
        for i in range(gap, n): #перебор элементов массива, начиная с некоторого
            temp = arr[i]   #вспомогательная переменная для сохранения значения элемента, выбранного для сравнения
            j = i       #вспомогательная переменная, для сохранения i неизменяемым
            # пока элемент больше выбранного для сравнения и выхода за пределы массива не предвидится
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]       #бОльший элемент перемещается на место сравниваемого элемента
                j = j - gap                    #устанавливается позиция элемента, который переместили
            arr[j] = temp                   #в выбранную позицию устанавливается элемент, выбранный для сравнения
        gap = gap // 2    #уменьение зазораш