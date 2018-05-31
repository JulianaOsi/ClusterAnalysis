#класс Node для определения элемента списка
class Node:
    def __init__(self, value = None, next = None):
        """
        Инициализация элемента списка
        :param value: значение в элементе списка
        :param next: указатель на следующий элемент
        """
        self.value = value      #значение
        self.next = next        #следующий элемент

#класс LinkedList для определения списка
class LinkedList:
    def __init__(self):
        """
        Инициализация списка
        """
        self.first = None       #первый элемент
        self.last = None        #последний элемент
        self.length = 0         #длина списка

    def __str__(self):
        """
        Вывод списка на печать
        :return: строка из элементов списка
        """
        if self.first != None:          #проверка на пустой список
            current = self.first        #выбор первого элемента
            out = 'LinkedList [\n' +str(current.value) +'\n'    #вывод на печать первого элемента
            while current.next != None: #перебор элементов списка
                current = current.next  #перестановка позиции на следующий элемент
                out += str(current.value) + '\n'    #добавление остальных элементов в переменную для вывода на печать
            return out + ']'            #вывод на печать содержимого списка
        return 'LinkedList []'

    def clear(self):
        """
        Удаление списка
        """
        self.__init__()

    def add(self, x):
        """
        добавление в конец списка
        :param x: значение, которое будет храниться в элементе
        """
        self.length+=1      #переменная-счетчик размера массива
        if self.first == None:  #если список пустой
            self.last = self.first = Node(x, None)  #первый элемент будет началом и концом списка
        else:
            self.last.next = self.last = Node(x, None) #добавленный элемент становится последним

    def InsertNth(self,i,x):
        """
        добавление в произвольное место
        :param i: позиция в списке
        :param x: значение, которое будет храниться в элементе
        """
        if self.first == None:  #если список пустой
            self.last = self.first = Node(x, None)  #первый элемент будет началом и концом списка
            return
        if i == 0:
          self.first = Node(x,self.first)   #добавление в начало списка
          return
        curr=self.first     #выбор первого элемента
        count = 0           #счетчик пройденных элементов
        while curr != None: #если не конец списка
            count+=1        #увеличение счетчика
            if count == i:  #если найдена нужная позиция
              curr.next = Node(x,curr.next)
              if curr.next.next == None:#если элемент добавляется в конец
                self.last = curr.next#присваивается указатель на конец
              break
            curr = curr.next#переход на следуюший элемент

    def getValueNth(self, i):
        """
        Возвращает значение элемента, стоящего на выбранной позиции
        :param i: позиция в списке
        :return: значение элемента
        """
        curr=self.first             #выбор первого элемента
        count = 0                   #счетчик пройденных элементов
        while curr != None:         #проверка на окончание списка
            count+=1                #увеличение счетчика
            if count == i:          #если нужная позиция найдена
                return curr.value   #возврат значения
            curr = curr.next        #выбор следующего элемента

    def Del(self,i):
        """
        Удаляет элемент списка из выбранной позиции
        :param i: позиция в списке
        """
        if (self.first == None):    #если список пустой
          return                    #возвращает пустой список
        curr = self.first           #выбор первого элемента
        count = 0                   #счетчик пройденных элементов
        if i == 0:                  #если удаляется первый элемент
          self.first = self.first.next  #первым становится следующий элемент
          return
        while curr != None:         #пока список не кончится
            if count == i:          #проверка на нужную позицию
              if curr.next == None: #если удаляется последний элемент
                self.last = curr    #последним становится предыдущий
              old.next = curr.next  #изменение указателя на следующий элемент
              break
            old = curr              #выбор предыдущего элемента
            curr = curr.next        #переход к следующему элементу
            count += 1              #увеличение счетчика
