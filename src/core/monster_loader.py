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
        
        # 1. Pattern Logic
        # New format might lack 'pattern' or have it in metadata/mechanics. 
        # Fallback to RECT_2X3 if missing.
        pattern_name = data.get("pattern")
        if not pattern_name and "metadata" in data:
             pattern_name = data["metadata"].get("pattern")
        
        # Default to RECT_2X3
        if not pattern_name:
             pattern_name = "RECT_2X3"
             
        pattern = PATTERNS.get(pattern_name)
        if not pattern:
            pattern = Pattern(shape=[(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)])
            
        # 2. Stats (Handle New vs Old)
        hp = data.get("hp", 10)
        atk = data.get("atk", 10)
        defense = data.get("defense", 0)
        
        if "stats" in data:
            stats = data["stats"]
            hp = stats.get("hp", hp)
            atk = stats.get("atk", atk)
            defense = stats.get("def", defense) # Note: 'def' in json maps to 'defense'
            
        # 3. Assets (Handle New vs Old)
        texture_path = data.get("texture_path")
        miniature_path = data.get("miniature_path")
        
        if "assets" in data:
            assets = data["assets"]
            # Map 'card_full_art' -> texture_path logic
            # Start with raw path
            if "card_full_art" in assets:
                 # Usually assets are relative to game root or assets folder? 
                 # Current data seems to assume "../assets/..." relative to json?
                 # New json has "cards/art/..."
                 # Let's try to harmonize. 
                 # If it starts with 'cards/', prepend '../assets/' or similar?
                 # For now, let's trust the path in JSON or prepend a standard base if needed.
                 # Existing code: texture_path = f"assets/cards/{data['texture']}"
                 texture_path = f"../assets/{assets['card_full_art']}"
            
            if "token_sprite" in assets:
                 miniature_path = f"../assets/{assets['token_sprite']}" # Approx mapping
        
        # Fallback for texture if still missing
        if not texture_path and "texture" in data:
             texture_path = f"../assets/cards/{data['texture']}"

        # 4. Mechanics / Effects
        effects = data.get("effects", [])
        if "mechanics" in data and "effects" in data["mechanics"]:
            # New format effects might be objects, not strings.
            # Monster dataclass expects List[str] currently?
            # Let's check dataclass... Yes, List[str].
            # If new format has objects, we need to extract IDs or update Dataclass.
            # For now, extract "id" if it's a dict.
            raw_effects = data["mechanics"]["effects"]
            effects = []
            for eff in raw_effects:
                if isinstance(eff, dict):
                    effects.append(eff.get("id", "UNKNOWN"))
                else:
                    effects.append(eff)

        return Monster(
            name=data.get("name", "Unknown"),
            level=data.get("level", 1),
            hp=hp,
            atk=atk,
            defense=defense,
            type=data.get("type", "Normal"),
            description=data.get("description", "") or data.get("metadata", {}).get("description", ""),
            texture_path=texture_path,
            miniature_path=miniature_path,
            pattern=pattern,
            effects=effects
        )
