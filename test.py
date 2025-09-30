from multiprocessing import Pool
import time

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(None) as p:
        print(p.map(f, [1, 2, 3]))
        time.sleep(10)
