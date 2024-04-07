from collections import defaultdict
from itertools import chain
import statistics
import heapq

# Define the task relationships, processing times, and tools for each task
graph = defaultdict(list, {
    1: [3], 3: [6], 6: [10, 11], 10: [14], 14: [18], 18: [22, 23], 22: [26],
    11: [14, 15], 23: [26, 27], 26: [27, 29], 2: [4, 9], 4: [7, 8], 7: [11, 12],
    15: [18, 19, 16], 19: [23, 20], 29: [30], 12: [15, 13], 24: [27, 28], 27: [29],
    5: [8], 8: [13], 16: [20], 20: [24, 25], 13: [16, 17], 25: [28], 28: [29], 9: [17],
    17: [21], 21: [25], 30: []
})

processing_times = {
    1: 13, 2: 6, 3: 7, 4: 6, 5: 11, 6: 11, 7: 6, 8: 11, 9: 14, 10: 8, 11: 11, 12: 15,
    13: 14, 14: 5, 15: 12, 16: 6, 17: 7, 18: 15, 19: 6, 20: 10, 21: 11, 22: 7, 23: 10,
    24: 9, 25: 7, 26: 15, 27: 12, 28: 12, 29: 7, 30: 5
}

task_tools = {
    2: 'M1', 3: 'M1', 4: 'M2', 5: 'M1', 8: 'M1', 9: 'M3', 10: 'M3', 11: 'M1', 14: 'M3',
    15: 'M2', 17: 'M2', 18: 'M1', 19: 'M1', 20: 'M1', 21: 'M1', 22: 'M1', 23: 'M3',
    25: 'M3', 27: 'M2', 29: 'M2', 30: 'M3'
}

# Identify starting tasks
starting_tasks = set(graph.keys()) - set(chain.from_iterable(graph.values()))

# Function to find all paths from a starting task to task 30
def find_all_paths(start, end=30, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    paths = []
    for next_task in graph[start]:
        new_paths = find_all_paths(next_task, end, path)
        for new_path in new_paths:
            paths.append(new_path)
    return paths

# Calculate the total processing time, tool variety, and standard deviation for each path
def calculate_path_metrics(path):
    times = [processing_times[task] for task in path]
    tools = {task_tools.get(task, None) for task in path}
    tools.discard(None)  # Remove None values
    std_dev = statistics.stdev(times) if len(times) > 1 else 0
    return sum(times), len(tools), std_dev

# Find all paths from each starting task and store them in 'all_paths'
all_paths = {start: find_all_paths(start) for start in starting_tasks}

# Iterate over 'all_paths' to get all the paths and their details
for start_task, paths in all_paths.items():
    print(f"\nAll paths from starting task {start_task}:")
    for path in paths:
        total_time, tool_variety, std_dev = calculate_path_metrics(path)
        print(f"Path: {path}, Total Time: {total_time}, Tool Variety: {tool_variety}, Std Dev: {std_dev:.2f}")

print('\n')

# Identifying the most optimal path for each starting task
optimal_paths = {}
for start in starting_tasks:
    best_score = float('inf')
    for path in find_all_paths(start):
        total_time, tool_variety, std_dev = calculate_path_metrics(path)
        score = total_time + std_dev - tool_variety # Set up based on requirements (can change)
        if score < best_score:
            best_score = score
            optimal_paths[start] = path

# Calculate all paths and their metrics from every starting task
all_paths_metrics = []
for start_task in starting_tasks:
    for path in find_all_paths(start_task):
        total_time, tool_variety, std_dev = calculate_path_metrics(path)
        # Adjust depending on assignment requirement(s)
        score = total_time - tool_variety * 10 + std_dev  # Example scoring formula
        all_paths_metrics.append((path, score, total_time, tool_variety, std_dev))

# Sort paths by the score, ascending so that a lower score is better
all_paths_metrics.sort(key=lambda x: x[1])

# Identify starting tasks as those with no predecessors
starting_tasks = set(graph.keys()) - set(chain.from_iterable(graph.values()))

# Function to find all paths from a given starting task to the end task
def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for next_task in graph[start]:
        new_paths = find_all_paths(graph, next_task, end, path)
        for new_path in new_paths:
            paths.append(new_path)
    return paths

# Function to calculate path metrics
def calculate_path_metrics(path):
    total_time = sum(processing_times[task] for task in path)
    tools_used = {task_tools.get(task, None) for task in path}
    tools_used.discard(None)  # Remove None values representing no tool used
    std_dev = statistics.stdev([processing_times[task] for task in path]) if len(path) > 1 else 0
    return total_time, len(tools_used), std_dev

# Find all paths for each starting task and calculate their metrics
all_paths_metrics = []
for start_task in starting_tasks:
    for path in find_all_paths(graph, start_task, 30):
        total_time, tool_variety, std_dev = calculate_path_metrics(path)
        score = total_time + std_dev - tool_variety  # scoring formula
        all_paths_metrics.append((path, total_time, tool_variety, std_dev, score))

# Sort all paths by their score to identify the top 10 paths
top_10_paths = heapq.nsmallest(10, all_paths_metrics, key=lambda x: x[-1])

# Print out the top 10 paths
print("Top 10 Paths from Any Starting Point:")
for path, total_time, tool_variety, std_dev, score in top_10_paths:
    print(f"Path: {path}, Total Time: {total_time}, Tool Variety: {tool_variety}, Std Dev: {std_dev:.2f}, Score: {score:.2f}")

# Function to assign tasks to workstations based on a given path
def assign_tasks_to_workstations(path, processing_times, number_of_workstations=10):
    workstations = [{'id': f'WS{i+1}', 'tasks': [], 'total_time': 0} for i in range(number_of_workstations)]
    for task in path:
        workstation = min(workstations, key=lambda ws: ws['total_time'])
        workstation['tasks'].append(task)
        workstation['total_time'] += processing_times[task]
    return workstations

# Output the workstation assignments for the top 10 paths
print("\nWorkstation Assignments for Top 10 Paths:")
for index, (path, total_time, tool_variety, std_dev, score) in enumerate(top_10_paths):
    ws_assignment = assign_tasks_to_workstations(path, processing_times)
    print(f"\nTop {index+1} Path: {path}, Score: {score:.2f}")
    for ws in ws_assignment:
        print(f"  {ws['id']} assigned tasks: {ws['tasks']} with total processing time: {ws['total_time']}")

# Find the single most optimal path out of all starting tasks
most_optimal_path = min(all_paths_metrics, key=lambda x: x[-1])[0]

# Assign tasks to workstations based on the most optimal path
workstations = [{'id': f'WS{i+1}', 'tasks': [], 'total_time': 0} for i in range(10)]
for task in most_optimal_path:
    workstation = min(workstations, key=lambda ws: ws['total_time'])
    workstation['tasks'].append(task)
    workstation['total_time'] += processing_times[task]

# Output the assignments
print("\nWorkstation Assignments Based on Most Optimal Path:")
for ws in workstations:
    print(f"{ws['id']} assigned tasks: {ws['tasks']} with total processing time: {ws['total_time']}")

# Output the most optimal path and its metrics
optimal_total_time, optimal_tool_variety, optimal_std_dev = calculate_path_metrics(most_optimal_path)
print(f"\nMost Optimal Path: {most_optimal_path}")
print(f"Total Time: {optimal_total_time}, Tool Variety: {optimal_tool_variety}, Std Dev: {optimal_std_dev:.2f}")
