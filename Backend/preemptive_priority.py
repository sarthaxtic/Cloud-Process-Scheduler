def preemptive_priority(processes):
    for p in processes:
        p['arrivalTime'] = int(p['arrivalTime'])
        p['burstTime'] = int(p['burstTime'])
        p['priority'] = int(p['priority'])
        p['processId'] = int(p['processId'])

    time = 0
    chart = []
    remaining = {p['processId']: p['burstTime'] for p in processes}
    arrived = []
    completed = []
    turnaround_total = waiting_total = 0
    processes = sorted(processes, key=lambda x: x['arrivalTime'])
    current = None
    start_time = {}

    while len(completed) < len(processes):
        arrived += [p for p in processes if p['arrivalTime'] == time and p not in arrived]
        ready = [p for p in arrived if p['processId'] not in completed and remaining[p['processId']] > 0]
        if ready:
            high = min(ready, key=lambda x: x['priority'])
            pid = high['processId']
            if current != pid:
                if current is not None and current in start_time:
                    chart.append({ "processId": current, "start": start_time[current], "end": time })
                current = pid
                start_time[pid] = time
            remaining[pid] -= 1
            if remaining[pid] == 0:
                completed.append(pid)
                turnaround_total += time + 1 - high['arrivalTime']
                waiting_total += time + 1 - high['arrivalTime'] - high['burstTime']
        else:
            if current is not None:
                chart.append({ "processId": current, "start": start_time[current], "end": time })
                current = None
        time += 1

    if current is not None:
        chart.append({ "processId": current, "start": start_time[current], "end": time })

    return {
        "chart": chart,
        "averageTurnaround": round(turnaround_total / len(processes), 2),
        "averageWaiting": round(waiting_total / len(processes), 2)
    }
