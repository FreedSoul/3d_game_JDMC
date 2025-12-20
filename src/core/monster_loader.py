import json
import os
from src.core.dataclasses import Monster, Pattern
from src.core.patterns_registry import PATTERNS

class MonsterLoader:
    @staticmethod
    def load_monsters(directory_path):
        """Loads all .json monster files from the given directory."""
        monsters = []
        
        # Ensure directory exists
        if not os.path.exists(directory_path):
            print(f"Warning: Monster directory {directory_path} does not exist.")
            return monsters

        for filename in os.listdir(directory_path):
            if filename.endswith(".json"):
                file_path = os.path.join(directory_path, filename)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        monster = MonsterLoader.parse_monster(data, directory_path)
                        if monster:
                            monsters.append(monster)
                except Exception as e:
                    print(f"Error loading monster from {filename}: {e}")
        
        return monsters

    @staticmethod
    def parse_monster(data, base_path=""):
        """Parses a dictionary into a Monster object."""
        pattern_name = data.get("pattern", "RECT_2X3")
        pattern = PATTERNS.get(pattern_name)
        if not pattern:
            pattern = Pattern(shape=[(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)])
            
        texture_path = data.get("texture_path")
        if not texture_path and "texture" in data:
             texture_path = f"assets/cards/{data['texture']}"

        miniature_path = data.get("miniature_path")
        
        return Monster(
            name=data.get("name", "Unknown"),
            level=data.get("level", 1),
            hp=data.get("hp", 10),
            atk=data.get("atk", 10),
            defense=data.get("defense", 0),
            type=data.get("type", "Normal"),
            description=data.get("description", ""),
            texture_path=texture_path,
            miniature_path=miniature_path,
            pattern=pattern,
            effects=data.get("effects", [])
        )
