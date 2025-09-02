def suggest_best_algorithm(processes, time_quantum=None):
    if not processes:
        return ("none", "No processes available to analyze.")

    # Check if all processes have a valid 'priority' > 0
    all_have_valid_priority = all(
        'priority' in p and isinstance(p['priority'], (int, float)) and p['priority'] > 0
        for p in processes
    )

    burst_times = [p.get('burst_time', 0) for p in processes]
    burst_variance = max(burst_times) - min(burst_times) if len(burst_times) > 1 else 0

    if all_have_valid_priority:
        return ("priority", "Priority Scheduling — All processes have valid priorities greater than 0.")

    elif burst_variance > 2:
        return ("sjf", "SJF (Shortest Job First) — Processes have varying burst times.")

    elif time_quantum and time_quantum > 0:
        return ("rr", f"Round Robin — Suitable for time-shared systems with time quantum = {time_quantum}.")

    else:
        return ("fcfs", "FCFS (First-Come First-Serve) — Simple non-preemptive scheduling.")
