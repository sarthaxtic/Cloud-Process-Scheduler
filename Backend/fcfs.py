def fcfs(processes):
    # Sort processes by arrival time
    processes.sort(key=lambda x: int(x['arrivalTime']))
    time = 0
    chart = []
    turnaround = waiting = 0

    for p in processes:
        arrival = int(p['arrivalTime'])
        burst = int(p['burstTime'])
        pid = int(p['processId'])

        start = max(time, arrival)
        end = start + burst
        time = end

        chart.append({"processId": pid, "start": start, "end": end})
        turnaround += end - arrival
        waiting += end - arrival - burst

    n = len(processes)
    return {
        "chart": chart,
        "averageTurnaround": round(turnaround / n, 2),
        "averageWaiting": round(waiting / n, 2)
    }
