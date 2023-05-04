import math
import random
import numpy as np
from prettytable import PrettyTable

random.seed("karimovareg1234")
# VARIABLES
tt = 0.0
Tp = 0.0
Na = 0
C1 = 0
C2 = 0
n = 0
i1 = 0
i2 = 0
lambd = 2
Amount = 0
Work = 0.0

# LISTS
A = []
W = []
D = []
TimeEvent = []
N = []
Event = []
ClientOfEvent = []
ClientOfEvent2 = []
V = []


# FUNCTIONS
def lambdaFunc(t):
    if 2 <= t < 8:
        return 1 + 2 / (t - 3)
    elif 8 <= t < 12:
        return 1 + 8 / t
    elif t >= 16:
        return 1 + 16 / t
    else:
        return abs(math.sin(t))


def poisson(t, lambd):
    while (1):
        u1 = random.random()
        t -= math.log(u1) / lambd
        u2 = random.random()
        if (u2 <= lambdaFunc(t) / lambd):
            return t


def exponentional(lambd):
    return -math.log(random.random()) / lambd


def add():
    global tt, Ta, Na, n, i1, i2, T1, T2, Amount
    tt = Ta
    Na += 1
    Ta = poisson(tt, lambd)
    A.insert(Na,tt)

    if (n == 0):
        n = 1
        i1 = Na
        i2 = 0
        Vi = exponentional(lambd)
        T1 = tt + Vi
        V.append(Vi)
        hand1='на 1 обработчик'
    elif (n == 1) and (i2 == 0):
        n = 2
        i2 = Na
        Vi = exponentional(lambd)
        T2 = tt + Vi
        V.append(Vi)
        hand1 = 'на 2 обработчик'
    elif n == 1 and i1 == 0:
        n = 2
        i1 = Na
        Vi = exponentional(lambd)
        T1 = tt + Vi
        V.append(Vi)
        hand1 = 'на 1 обработчик'
    elif (n > 1):
        n = n + 1
        hand1='в очередь'
    Amount += 1
    N.append(n)
    TimeEvent.append(tt)
    Event.append('Клиент '+ hand1 +' прибыл:' + str(Na))


def leaving_1():
    global T1, C1, n,tt, i1, m ,i2
    tt = T1
    C1 += 1
    handler = i1
    D.insert(i1-1,tt)
    if (n == 1):
        n = 0
        T1 = 1e6
    if (n == 2):
        n = 1
        i1 = 0
        T1 = 1e6
    if (n > 2):
        m = max(i1, i2)
        n = n-1
        i1 = m + 1
        Vi = exponentional(lambd)
        T1 = tt + Vi
        V.append(Vi)
    N.append(n)
    TimeEvent.append(tt)
    Event.append('Уход клиента с 1:' + str(handler))

def leaving_2():
    global T2, C2, n, n, tt, i1,i2, m
    tt = T2
    C2 += 1
    handler = i2
    D.insert(i2-1,tt)
    if (n == 1):
        n = 0
        T2 = 1e6
    if (n == 2):
        n = 1
        i2 = 0
        T2 = 1e6
    if (n > 2):
        m = max(i1, i2)
        n = n - 1
        i2 = m + 1
        Vi = exponentional(lambd)
        T2 = tt + Vi
        V.append(Vi)
    N.append(n)
    TimeEvent.append(tt)
    Event.append('Уход клиента со 2:' + str(handler))


"""
def last_1():
    global T1, C1, n, tt, i1, m, i2
    handler = i1
    D.insert(i1 - 1, T)
    V.append(0)
    N.append(n)
    TimeEvent.append(T)
    Event.append('Уход клиента: ' + str(handler) + 'с 1')

def last_2():
    global T1, C1, n, tt, i1, m, i2
    handler = i2
    D.insert(i1 - 1, T)
    V.append(0)
    N.append(n)
    TimeEvent.append(T)
    Event.append('Уход клиента: ' + str(handler) + 'с 2')


def end():
    global n, Tp, tt, T
    Tp = max(tt - T, 0)
    N.append(n)

"""
# MAIN
#t_start = int(input('Введите начало рабочего дня: '))
#t_finish = int(input('Введите конец рабочего дня: '))
#print('lambd(λ) = 2 чел/час')
t_start = 10
t_finish = 18
tt = t_start
T = t_finish
Ta = poisson(tt, lambd)
T1 = 1e6
T2 = 1e6
C1 = 0
C2 = 0
while (1):
    if (Ta == min(Ta,T1,T2)):
        add()
    if (T1 == min(Ta,T1,T2)):
        leaving_1()
    elif (T2 == min(Ta,T1,T2)):
        leaving_2()
    if (min(Ta, T1, T2) > T) and (n == 0):
        break

table3 = PrettyTable(
    ['Номер клиента', 'Время прибытия', 'Время обслуживания'])
for i in range(len(A)):
    table3.add_row([i + 1, round(A[i], 3), round(V[i], 3)])

print(table3)

table1 = PrettyTable(['Событие', 'Время события'])
for i in range(len(TimeEvent)):
    table1.add_row([Event[i], round(TimeEvent[i], 3)])
    if Event[i][0] == 'У' :
        index = int((Event[i].split(':'))[1]) -1
        W.insert(index,TimeEvent[i] - (A[index] + V[index]))




Work = 0
for i in range(len(A)):
    if i == 0:
        Work = A[0] - t_start
    elif W[i] == 0:
        Work += A[i] - D[i - 1]

print(table1)

table2 = PrettyTable(
    ['№', 'Время прихода', 'Время нач. обсл.', 'Время ухода', 'Время обсл.', 'Время в очер.', 'Время в системе'])
for i in range(len(D)):
    table2.add_row(
        [i + 1, round(A[i], 3), round(A[i] + W[i], 3), round(D[i], 3), round(D[i] - A[i] - W[i], 3), round(W[i], 3), round(D[i] - A[i], 3)])
print(table2)

print('Количество клиентов за смену: ', Amount)
mean_go = 0
for i in range(len(A) - 1):
    mean_go += A[i + 1] - A[i]
mean_go /= (len(A) - 2)
print('Среднее время между поступлениями: ', mean_go)

print('Время задержки закрытия: ', Tp)
mean_client = 0
for i in range(1, len(TimeEvent)):
    mean_client += N[i - 1] * (TimeEvent[i] - TimeEvent[i - 1])
mean_client /= 10
print('Оценка ожидаемого среднего числа клиентов в очереди: ', mean_client)
print('Среднее время клиентов в очереди: ', np.mean(W))
print('Среднее время клиента в системе: ', np.mean(np.array(D) - np.array(A)))
print('Коэффициент занятости устройства: ', 1 - (Work / (t_finish - t_start)))
print('Средняя длина очереди: ', np.mean(N))

print('\n\nВарификация на 6 клиентов (для проверки вручную):')
print('Среднее время клиента в системе: ', round(np.mean(np.array(D[:6]) - np.array(A[:6])), 3))
print('Среднее время клиентов в очереди: ', round(np.mean(W[:6]), 3))
mean_D = 0
for i in range(10):
    if i != 9:
        mean_D += N[i] * (TimeEvent[i + 1] - TimeEvent[i])
    else:
        mean_D += N[i] * (11 - TimeEvent[i])
mean_D /= 3
print('Число клиентов в системе в период [0, T](оценка ожидаемого среднего числа клиентов в очереди): ',
      round(mean_D, 3))

mean_T = 0
for i in range(6):
    if i == 0:
        mean_T = A[0] - t_start
    elif W[i] == 0:
        mean_T += A[i] - D[i - 1]
print('Коэффициент занятости устройства: ', 1 - (mean_T / 4))