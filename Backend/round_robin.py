def round_robin(processes, quantum):
    for p in processes:
        p['arrivalTime'] = int(p['arrivalTime'])
        p['burstTime'] = int(p['burstTime'])
        p['processId'] = int(p['processId'])

    time = 0
    queue = []
    chart = []
    remaining = {p['processId']: p['burstTime'] for p in processes}
    processes.sort(key=lambda x: x['arrivalTime'])
    idx = 0
    turnaround_total = 0
    waiting_total = 0
    finished = {}

    while idx < len(processes) or queue:
        while idx < len(processes) and processes[idx]['arrivalTime'] <= time:
            queue.append(processes[idx])
            idx += 1

        if not queue:
            time += 1
            continue

        current = queue.pop(0)
        pid = current['processId']
        burst_left = remaining[pid]
        run_time = min(burst_left, quantum)
        chart.append({ "processId": pid, "start": time, "end": time + run_time })
        time += run_time
        remaining[pid] -= run_time

        while idx < len(processes) and processes[idx]['arrivalTime'] <= time:
            queue.append(processes[idx])
            idx += 1

        if remaining[pid] > 0:
            queue.append(current)
        else:
            finished[pid] = time - current['arrivalTime']
            turnaround_total += finished[pid]
            waiting_total += finished[pid] - current['burstTime']

    return {
        "chart": chart,
        "averageTurnaround": round(turnaround_total / len(processes), 2),
        "averageWaiting": round(waiting_total / len(processes), 2)
    }
