import time
from functools import lru_cache


# С помощью декоратора @lru_cache закешируйте функцию которая рекурсивно считает сумму положительных чисел списка.

@lru_cache
def get_cache(data: tuple)-> int:
    if not data:
        return 0
    time.sleep(0.1)
    if data[0] % 2 == 0:
        return data[0] + get_cache(data[1:])
    return get_cache(data[1:])


print(get_cache(tuple([3,6,7,8,0,8,9,2])))
print(get_cache(tuple([3,6,7,8,0,8,9,2])))
print(get_cache(tuple([2,4,6,4,3,3,3,1])))




