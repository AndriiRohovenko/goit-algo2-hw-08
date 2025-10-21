import random
from functools import lru_cache
import time


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [
        (random.randint(0, n // 2), random.randint(n // 2, n - 1))
        for _ in range(hot_pool)
    ]
    queries = []
    for _ in range(q):
        if random.random() < p_update:  # ~3% запитів — Update
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:  # ~97% — Range
            if random.random() < p_hot:  # 95% — «гарячі» діапазони
                left, right = random.choice(hot)
            else:  # 5% — випадкові діапазони
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries


# --- No caching implementation
def range_sum_no_cache(array, left, right):
    return sum(array[left : right + 1])


def update_no_cache(array, index, value):
    array[index] = value
    return array


# --- Caching implementation
array_global = []


@lru_cache(maxsize=1000)
def range_sum_with_cache(left, right):
    return sum(array_global[left : right + 1])


def update_with_cache(index, value):
    array_global[index] = value
    range_sum_with_cache.cache_clear()


def test_performance(n=100_000, q=50_000):
    global array_global

    data = [random.randint(1, 100) for _ in range(n)]
    queries = make_queries(n, q)

    # Без кешу
    arr_no_cache = data.copy()
    start = time.time()
    for query in queries:
        if query[0] == "Update":
            update_no_cache(arr_no_cache, query[1], query[2])
        else:
            range_sum_no_cache(arr_no_cache, query[1], query[2])
    t1 = time.time() - start

    # З кешем
    array_global = data.copy()
    start = time.time()
    for query in queries:
        if query[0] == "Update":
            update_with_cache(query[1], query[2])
        else:
            range_sum_with_cache(query[1], query[2])
    t2 = time.time() - start

    print(f"Без кешу : {t1:.2f} c")
    print(f"LRU-кеш  : {t2:.2f} c  (прискорення ×{t1/t2:.2f})")


if __name__ == "__main__":
    test_performance()
