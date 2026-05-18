import random
import time

def solve():
    # 1. Read N and M manually
    n, m = map(int, input("Enter N and M (space-separated): ").split())
    
    # 2. Read skill ratings
    skills_input = input(f"Enter {n} skill ratings (space-separated): ")
    skills = [0] + list(map(int, skills_input.split()))
    
    # 3. Build adjacency list for conflict pairs
    adj = {i: [] for i in range(1, n + 1)}
    
    if m > 0:
        print(f"Enter {m} conflict pairs (one pair per line):")
        for _ in range(m):
            u, v = map(int, input().split())
            adj[u].append(v)
            adj[v].append(u)
            
    class Coder:
        def __init__(self, id, skill, degree):
            self.id = id
            self.skill = skill
            self.degree = degree
            self.score = 0.0

    coders = [Coder(i, skills[i], len(adj[i])) for i in range(1, n + 1)]
    
    best_total_score = -1
    best_team = []
    
    start_time = time.time()
    time_limit = 295  # 4m 55s
    
    print("\nCalculating best team... (Press Ctrl+C to stop early and view current best)")
    
    try:
        # Continuously evaluate combinations
        while True:
            if time.time() - start_time > time_limit:
                break
                
            # Perturb the greedy choice metric
            for coder in coders:
                random_factor = random.uniform(0.8, 1.2)
                coder.score = (coder.skill / (coder.degree + 1.0)) * random_factor
                
            coders.sort(key=lambda x: x.score, reverse=True)
            
            in_team = [False] * (n + 1)
            excluded = [False] * (n + 1)
            
            current_total_score = 0
            current_team = []
            
            for coder in coders:
                id = coder.id
                if not excluded[id]:
                    in_team[id] = True
                    current_team.append(id)
                    current_total_score += coder.skill
                    
                    for neighbor in adj[id]:
                        excluded[neighbor] = True
                        
            if current_total_score > best_total_score:
                best_total_score = current_total_score
                best_team = current_team
                
    except KeyboardInterrupt:
        # Catch manual cancellation to print the best result found so far
        print("\nSearch stopped early by user.")

    best_team.sort()
    
    print("\n--- OUTPUT ---")
    print(best_total_score)
    print(" ".join(map(str, best_team)))

if __name__ == '__main__':
    solve()