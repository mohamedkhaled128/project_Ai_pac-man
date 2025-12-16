"""
Script to run tests and find the best algorithm
"""
from pathlib import Path
from algorithm_tester import AlgorithmTester
from collections import deque
import json

def main():
    map_path = Path(__file__).parent.parent / "maps" / "map1.txt"
    tester = AlgorithmTester(map_path)
    
    # Use positions from map
    start = tester.game_map.start

    def find_reachable_goal():
        """
        Pick the first reachable target (ghost, pellet, power pellet).
        Falls back to any reachable empty cell, else start.
        """
        gmap = tester.game_map

        # BFS to find reachability
        visited = {start}
        queue = deque([start])
        while queue:
            cur = queue.popleft()
            for n in gmap.neighbors(cur):
                if n not in visited:
                    visited.add(n)
                    queue.append(n)

        # Ordered candidates: ghosts, power pellets, pellets
        candidates = list(gmap.ghost_positions) + list(gmap.power_pellets) + list(gmap.pellets)
        for c in candidates:
            if c in visited:
                return c

        # Any reachable cell
        for cell in visited:
            if cell != start:
                return cell

        return start

    goal = find_reachable_goal()
    
    print("=" * 70)
    print("Testing All Algorithms - Pac-Man Pathfinding")
    print("=" * 70)
    print(f"Start Point: {start}")
    print(f"Goal Point: {goal}")
    print("=" * 70)
    
    # Test all algorithms (with timeout for slow algorithms)
    results = tester.test_all_algorithms(start, goal, num_runs=10, timeout=2.0)
    
    print("\n" + "=" * 70)
    print("Results:")
    print("=" * 70)
    
    for result in results:
        print(f"\n{result['name']}:")
        print(f"  - Success Rate: {result['success_rate']:.2f}%")
        print(f"  - Average Path Length: {result['avg_path_length']:.2f}")
        print(f"  - Average Time: {result['avg_time']*1000:.4f} ms")
        if result.get('timeout_count', 0) > 0:
            print(f"  - Timeouts: {result['timeout_count']}")
    
    # Find best algorithm
    best = tester.find_best_algorithm(start, goal, num_runs=10)
    
    print("\n" + "=" * 70)
    print("Best Algorithm:")
    print("=" * 70)
    
    if best:
        print(f"Name: {best['name']}")
        print(f"Success Rate: {best['success_rate']:.2f}%")
        print(f"Average Path Length: {best['avg_path_length']:.2f}")
        print(f"Average Time: {best['avg_time']*1000:.4f} ms")
        print(f"Score: {best['score']:.4f}")
        
        # Save results
        results_file = Path(__file__).parent.parent / "best_algorithm.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                'best_algorithm': best['name'],
                'results': best
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to: {results_file}")
        print(f"\n{'=' * 70}")
        print("✓ TESTING COMPLETED SUCCESSFULLY!")
        print(f"{'=' * 70}")
        print(f"\nBest Algorithm: {best['name']}")
        print(f"The game will now use '{best['name']}' algorithm automatically!")
        print(f"\n{'=' * 70}")
        print("You can now run the game with: python main.py")
        print(f"{'=' * 70}\n")
    else:
        print("\n" + "=" * 70)
        print("✗ TESTING FAILED - No results found!")
        print("=" * 70)
        print("The game will use A* as default algorithm.\n")

if __name__ == "__main__":
    main()
