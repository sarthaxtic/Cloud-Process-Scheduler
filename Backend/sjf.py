def sjf(processes):
    for p in processes:
        p['arrivalTime'] = int(p['arrivalTime'])
        p['burstTime'] = int(p['burstTime'])
        p['processId'] = int(p['processId'])

    processes.sort(key=lambda x: x['arrivalTime'])
    completed = []
    time = 0
    chart = []
    turnaround_total = waiting_total = 0

    while len(completed) < len(processes):
        ready = [p for p in processes if p not in completed and p['arrivalTime'] <= time]
        if not ready:
            time += 1
            continue
        shortest = min(ready, key=lambda x: x['burstTime'])
        start = time
        end = start + shortest['burstTime']
        chart.append({ "processId": shortest['processId'], "start": start, "end": end })
        time = end
        turnaround_total += end - shortest['arrivalTime']
        waiting_total += end - shortest['arrivalTime'] - shortest['burstTime']
        completed.append(shortest)

    return {
        "chart": chart,
        "averageTurnaround": round(turnaround_total / len(processes), 2),
        "averageWaiting": round(waiting_total / len(processes), 2)
    }
