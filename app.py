import time
import sys
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def binary_search_iterative(arr, target):
    low = 0
    high = len(arr) - 1
    steps = 0
    
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, steps

def binary_search_recursive(arr, target, low, high, steps=0):
    steps += 1
    if low > high:
        return -1, steps
    
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid, steps
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high, steps)
    else:
        return binary_search_recursive(arr, target, low, high - 1, steps)

# --- DATA DUMMY (KATALOG LAGU) ---
# Menggunakan integer ID agar mudah disorting dan dicari
def get_dataset(size):
    return list(range(0, size * 2, 2)) # Data genap terurut: 0, 2, 4...

# --- ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    target = int(request.form.get('target'))
    algo_type = request.form.get('algo')
    data_size = 10000 # Default sampel
    data = get_dataset(data_size)
    
    start_time = time.perf_counter()
    
    if algo_type == 'iterative':
        index, steps = binary_search_iterative(data, target)
    else:
        index, steps = binary_search_recursive(data, target, 0, len(data)-1)
        
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000 # ke milidetik

    return jsonify({
        'index': index,
        'steps': steps,
        'time': f"{execution_time:.6f} ms",
        'algo': algo_type
    })

# [cite_start]--- FITUR BENCHMARK
@app.route('/benchmark')
def benchmark():
    # Ukuran input variatif: 10, 100, ..., 1.000.000
    sizes = [10, 100, 1000, 5000, 10000, 50000, 100000]
    results_iter = []
    results_recur = []
    
    for size in sizes:
        data = get_dataset(size)
        target = data[-1] # Worst case: cari elemen terakhir
        
        # Test Iterative
        start = time.perf_counter()
        binary_search_iterative(data, target)
        end = time.perf_counter()
        results_iter.append((end - start) * 1000) # ms
        
        # Test Recursive
        # Menambah limit recursion untuk data besar
        sys.setrecursionlimit(max(2000, size + 100))
        start = time.perf_counter()
        binary_search_recursive(data, target, 0, len(data)-1)
        end = time.perf_counter()
        results_recur.append((end - start) * 1000) # ms

    return jsonify({
        'sizes': sizes,
        'iterative': results_iter,
        'recursive': results_recur
    })

if __name__ == '__main__':

    app.run(debug=True)
