import time

CASH = {}
def search_cash(key, value):
    if key not in CASH:
        print('sleep...')
        time.sleep(5)
        CASH[key] = value
    return CASH[key]

print(search_cash(1,'one'))
print(search_cash(2,'two'))



