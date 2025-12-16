"""
Algorithm Testing System - Measures performance of pathfinding algorithms
"""
import time
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from map import GameMap
from algorithms import (
    astar, dijkstra, bfs, dfs, 
    greedy_best_first, bidirectional_search, 
    ida_star, theta_star
)

class AlgorithmTester:
    """Class for testing and measuring algorithm performance"""
    
    def __init__(self, map_path):
        self.game_map = GameMap(map_path)
        self.algorithms = {
            'A*': astar,
            'Dijkstra': dijkstra,
            'BFS': bfs,
            'DFS': dfs,
            'Greedy Best-First': greedy_best_first,
            'Bidirectional': bidirectional_search,
            'IDA*': ida_star,
            'Theta*': theta_star
        }
    
    def test_algorithm(self, algorithm_name, start, goal, num_runs=10, timeout=5.0):
        """
        Test a specific algorithm
        
        Args:
            algorithm_name: Name of the algorithm
            start: Start point (x, y)
            goal: Goal point (x, y)
            num_runs: Number of runs for measurement
            timeout: Maximum time per run in seconds
        
        Returns:
            dict: Test results
        """
        if algorithm_name not in self.algorithms:
            return None
        
        algorithm = self.algorithms[algorithm_name]
        times = []
        path_lengths = []
        success_count = 0
        timeout_count = 0
        
        for _ in range(num_runs):
            start_time = time.time()
            try:
                path = algorithm(self.game_map, start, goal)
                elapsed_time = time.time() - start_time
                
                # Check for timeout
                if elapsed_time > timeout:
                    timeout_count += 1
                    path_lengths.append(float('inf'))
                    times.append(timeout)
                    continue
                
                times.append(elapsed_time)
                if path:
                    path_lengths.append(len(path))
                    success_count += 1
                else:
                    path_lengths.append(float('inf'))
            except (KeyboardInterrupt, RecursionError, MemoryError):
                timeout_count += 1
                path_lengths.append(float('inf'))
                times.append(timeout)
        
        avg_time = sum(times) / len(times) if times else 0
        avg_length = sum([l for l in path_lengths if l != float('inf')]) / success_count if success_count > 0 else float('inf')
        success_rate = success_count / num_runs * 100
        
        return {
            'name': algorithm_name,
            'avg_time': avg_time,
            'avg_path_length': avg_length,
            'success_rate': success_rate,
            'times': times,
            'path_lengths': path_lengths,
            'timeout_count': timeout_count
        }
    
    def test_all_algorithms(self, start, goal, num_runs=10, timeout=5.0):
        """
        Test all algorithms
        
        Args:
            start: Start point (x, y)
            goal: Goal point (x, y)
            num_runs: Number of runs
            timeout: Maximum time per run in seconds
        
        Returns:
            list: List of results for all algorithms
        """
        results = []
        for alg_name in self.algorithms.keys():
            print(f"Testing {alg_name}...", end=" ", flush=True)
            try:
                result = self.test_algorithm(alg_name, start, goal, num_runs, timeout)
                if result:
                    results.append(result)
                    if result['timeout_count'] > 0:
                        print(f"Done (with {result['timeout_count']} timeouts)")
                    else:
                        print("Done")
                else:
                    print("Failed")
            except Exception as e:
                print(f"Error: {e}")
        return results
    
    def find_best_algorithm(self, start, goal, num_runs=10):
        """
        Find the best algorithm based on accuracy and speed
        
        Scoring formula:
        score = (success_rate * 0.5) + (1 / avg_path_length) * 0.3 + (1 / avg_time) * 0.2
        
        Args:
            start: Start point (x, y)
            goal: Goal point (x, y)
            num_runs: Number of runs
        
        Returns:
            dict: Best algorithm and its results
        """
        results = self.test_all_algorithms(start, goal, num_runs)
        
        if not results:
            return None
        
        # Calculate score for each algorithm
        scored_results = []
        for result in results:
            if result['success_rate'] == 0:
                score = 0
            else:
                # Normalize path length score (shorter is better)
                length_score = (1 / result['avg_path_length']) * 0.3 if result['avg_path_length'] != float('inf') else 0
                # Normalize time score (faster is better)
                time_score = (1 / (result['avg_time'] + 0.001)) * 0.2  # Avoid division by zero
                # Success rate score (higher is better)
                success_score = result['success_rate'] / 100 * 0.5
                score = success_score + length_score + time_score
            
            scored_results.append({
                **result,
                'score': score
            })
        
        # Sort by score (highest first)
        scored_results.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_results[0] if scored_results else None

if __name__ == "__main__":
    # Quick test
    map_path = Path(__file__).parent.parent / "maps" / "map1.txt"
    tester = AlgorithmTester(map_path)
    
    # Use positions from map
    start = tester.game_map.start
    goal = tester.game_map.ghost_positions[0] if tester.game_map.ghost_positions else (5, 5)
    
    print("=" * 60)
    print("Testing All Algorithms")
    print("=" * 60)
    
    best = tester.find_best_algorithm(start, goal, num_runs=5)
    
    if best:
        print(f"\nBest Algorithm: {best['name']}")
        print(f"Success Rate: {best['success_rate']:.2f}%")
        print(f"Average Path Length: {best['avg_path_length']:.2f}")
        print(f"Average Time: {best['avg_time']*1000:.4f} ms")
        print(f"Score: {best['score']:.4f}")
    else:
        print("No results found!")
