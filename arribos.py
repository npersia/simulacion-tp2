from random import expovariate

def arr_t1_t2(media,tiempo_total):
    l = 1/media
    arr = []
    t_total = 0

    while True:
        t = expovariate(l)
        t_total += t
        if t_total > tiempo_total:
            t_total -= t
            return arr, t_total
        arr.append(t)

def tiempos_de_arribo(arr):
    arr2 = []
    arr2.append(arr[0])
    for i in range(1,len(arr)):
        arr2.append(arr[i]+arr2[i-1])
    return arr2


a,b = arr_t1_t2(4,120)
print(a)
print(b)
print(tiempos_de_arribo(a))
