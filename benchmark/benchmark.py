import csv

import requests
import time
import random
import threading
from statistics import mean


api_endpoints = {'q1': 'http://localhost:3000/wahlkreis/q1',
                 'q2': 'http://localhost:3000/wahlkreis/q2',
                 'q3': 'http://localhost:3000/wahlkreis/q3',
                 'q4': 'http://localhost:3000/wahlkreis/q4',
                 'q5': 'http://localhost:3000/wahlkreis/q5',
                 'q6-winners': 'http://localhost:3000/wahlkreis/q6-winners',
                 'q6-losers': 'http://localhost:3000/wahlkreis/q6-losers'
                 }
workload_distribution = {'q1': 25, 'q2': 10, 'q3': 10, 'q4': 10, 'q5': 10, 'q6-winners': 5, 'q6-losers': 5}

# Benchmarking Parameters
n_terminals = 100  # Number of simulated clients
requests_per_terminal = 10  # Number of requests per terminal
average_wait = 1.0  # Average wait time in seconds

# Results Storage
results = {endpoint: {'durations': [], 'hits': 0} for endpoint in api_endpoints}


# Thread Worker Function
def simulate_terminal():
    for _ in range(requests_per_terminal):
        endpoint = random.choices(list(api_endpoints.keys()), weights=workload_distribution.values())[0]
        start_time = time.time()
        response = requests.get(api_endpoints[endpoint])
        duration = time.time() - start_time

        # Record duration and increment hit count
        results_lock.acquire()
        results[endpoint]['durations'].append(duration)
        results[endpoint]['hits'] += 1
        results_lock.release()

        time.sleep(random.uniform(0.8 * average_wait, 1.2 * average_wait))


# To ensure thread-safe operations on the results dictionary
results_lock = threading.Lock()

threads = []
for _ in range(n_terminals):
    t = threading.Thread(target=simulate_terminal)
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

# Write Results to CSV and Print
with open('benchmark_results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Endpoint', 'Mean Duration (seconds)', 'Hits'])

    for endpoint, data in results.items():
        mean_duration = mean(data['durations']) if data['durations'] else 0
        hits = data['hits']
        writer.writerow([endpoint, f"{mean_duration:.2f}", hits])
        print(f"{endpoint}: Mean duration = {mean_duration:.6f} seconds, Hits = {hits}")
