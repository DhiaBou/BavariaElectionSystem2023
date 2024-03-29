import csv
import random
import threading
import time
from statistics import mean

import requests

api_endpoints = {'q1': 'http://localhost:8000/wahlkreis/q1',
                 'q2': 'http://localhost:8000/wahlkreis/q2',
                 'q3': 'http://localhost:8000/wahlkreis/q3',
                 'q4': 'http://localhost:8000/wahlkreis/q4',
                 'q5': 'http://localhost:8000/wahlkreis/q5',
                 'q6': 'http://localhost:8000/wahlkreis/q6'}

workload_distribution = {'q1': 0.25, 'q2': 0.10, 'q3': 0.25, 'q4': 0.10, 'q5': 0.10, 'q6': 0.20}

# List of different values of n
n_values = [20, 70]

# List of different average wait times
average_waits = [0.1, 0.2]

# Results Storage
all_results = {}

for n_terminals in n_values:
    for average_wait in average_waits:
        print('-----------------')
        print(n_terminals)
        print(average_wait)
        results = {endpoint: {'durations': [], 'hits': 0} for endpoint in api_endpoints}


        # Thread Worker Function
        def simulate_terminal():
            for i in range(requests_per_terminal):
                print(i)
                endpoint = random.choices(list(api_endpoints.keys()), weights=workload_distribution.values())[0]
                start_time = time.time()
                response = requests.get(api_endpoints[endpoint])
                url = response.url
                duration = time.time() - start_time
                print(duration)

                # Record duration and increment hit count
                results_lock.acquire()
                results[endpoint]['durations'].append(duration)
                results[endpoint]['hits'] += 1
                results_lock.release()

                time.sleep(random.uniform(0.8 * average_wait, 1.2 * average_wait))


        # To ensure thread-safe operations on the results dictionary
        results_lock = threading.Lock()

        threads = []
        requests_per_terminal = 20  # Number of requests per terminal

        for _ in range(n_terminals):
            t = threading.Thread(target=simulate_terminal)
            threads.append(t)
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        all_results[(n_terminals, average_wait)] = results

# Write Results to One CSV File
with open('benchmark_results_multi_threaded.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['N', 'Average Wait (seconds)', 'Endpoint', 'Mean Duration (seconds)', 'Min Duration (seconds)',
                     'Max Duration (seconds)', 'Hits'])

    for (n, wait), results in all_results.items():
        total_hits = sum([data['hits'] for data in results.values()])

        for endpoint, data in results.items():
            durations = data['durations']
            mean_duration = mean(durations) if durations else 0
            min_duration = min(durations) if durations else 0
            max_duration = max(durations) if durations else 0
            hits = data['hits']
            percentage_of_hits = (hits / total_hits) * 100 if total_hits > 0 else 0

            writer.writerow(
                [n, wait, endpoint, f"{mean_duration:.2f}", f"{min_duration:.6f}",
                 f"{max_duration:.6f}", hits])
