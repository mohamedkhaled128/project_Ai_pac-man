
from pathlib import Path
from gui.game_gui import GameGUI

def main():
    
    map_path = Path(__file__).parent / "maps" / "map1.txt"
    
    if not map_path.exists():
        print(f"خطأ: لم يتم العثور على الخريطة في {map_path}")
        return
    
    game = GameGUI(map_path)
    game.run()

if __name__ == "__main__":
    main()

