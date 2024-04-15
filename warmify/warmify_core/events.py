def get_events_count_by_hour(events):
    events_count = [0 for _ in range(24)]
    for e in events:
        events_count[e.timestamp.hour] += 1
    return events_count
