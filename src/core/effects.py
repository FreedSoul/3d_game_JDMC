from typing import Callable, Any, Dict

class Effect:
    """Base class for all card/monster effects."""
    def __init__(self, effect_id: str, description: str):
        self.effect_id = effect_id
        self.description = description
    
    def apply(self, game_engine, **kwargs):
        """Override this method to implement effect logic."""
        pass

# --- Specific Effects Implementation ---

class EffectDoubleAttack(Effect):
    def apply(self, game_engine, **kwargs):
        attacker = kwargs.get('attacker')
        if attacker:
            print(f"Effect Triggered: {self.effect_id} - Doubling Attack for {attacker.name}!")
            # Logic would go here (e.g. temporary buff)

class EffectHealSelf(Effect):
    def apply(self, game_engine, **kwargs):
        monster = kwargs.get('monster')
        if monster:
            print(f"Effect Triggered: {self.effect_id} - Healing {monster.name}!")
            # Logic here

# --- Registry ---

EFFECTS_REGISTRY: Dict[str, Effect] = {
    "E001_DOUBLE_ATK": EffectDoubleAttack("E001_DOUBLE_ATK", "Double Attack Power for one turn."),
    "E002_HEAL_SELF": EffectHealSelf("E002_HEAL_SELF", "Heal 10 HP."),
}

def get_effect(effect_id: str) -> Effect:
    return EFFECTS_REGISTRY.get(effect_id)
