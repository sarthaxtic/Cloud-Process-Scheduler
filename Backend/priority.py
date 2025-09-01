def priority(processes):
    for p in processes:
        p['arrivalTime'] = int(p['arrivalTime'])
        p['burstTime'] = int(p['burstTime'])
        p['priority'] = int(p['priority'])
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
        high = min(ready, key=lambda x: x['priority'])
        start = time
        end = start + high['burstTime']
        chart.append({ "processId": high['processId'], "start": start, "end": end })
        time = end
        turnaround_total += end - high['arrivalTime']
        waiting_total += end - high['arrivalTime'] - high['burstTime']
        completed.append(high)

    return {
        "chart": chart,
        "averageTurnaround": round(turnaround_total / len(processes), 2),
        "averageWaiting": round(waiting_total / len(processes), 2)
    }
