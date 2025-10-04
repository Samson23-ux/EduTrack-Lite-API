import hashlib
from pathlib import Path

path = Path('app')

def write_logs(data):
    (path/'data/logs.txt').write_text(data)

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def partition(data, start, end):
    if end is None:
        end = len(data) - 1

    l, r = start, end-1

    while l < r:
        if data[l].name <= data[end].name:
            l += 1
        elif data[r].name > data[end].name:
            r -= 1
        else:
            data[l], data[r] = data[r], data[l]

    if data[l].name > data[end].name:
        data[l], data[end] = data[end], data[l]
        return l
    else:
        return end

def quick_sort(data, start=0, end=None):
    if end is None:
        end = len(data) - 1

    if start < end:
        pivot = partition(data, start, end)
        quick_sort(data, start, pivot-1)
        quick_sort(data, pivot+1, end)

    return data
