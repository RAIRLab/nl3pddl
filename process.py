from concurrent.futures import ProcessPoolExecutor

def f(x):
    return x * x

if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=100) as p:
        results = list(p.map(f, [1, 2, 3]))
        print(results)  # [1, 4, 9]
