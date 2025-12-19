from ursina import *
from src.ui.monster_card import MonsterCard
from src.core.dataclasses import Monster, Pattern

class HandView(Entity):
    def __init__(self, engine=None, on_summon_click=None):
        super().__init__(parent=camera.ui)
        self.engine = engine
        self.cards = []
        self.on_summon_click = on_summon_click
        self.create_test_hand()
        
    def update(self):
        if self.engine:
            player = self.engine.get_current_player()
            # Safety check if player exists
            if player:
                summ_crests = player.crests.get('SUMMON', 0)
                can_summon = summ_crests >= 2
                for c in self.cards:
                    c.set_summonable(can_summon)

    def create_test_hand(self):
        from src.core.monster_loader import MonsterLoader
        # Load monsters from data directory
        monsters_data = MonsterLoader.load_monsters("data/monsters")
        
        # Sort by name for consistent order (optional but nice)
        monsters_data.sort(key=lambda m: m.name)
        
        start_x = -0.35
        spacing = 0.20
        
        for i, m in enumerate(monsters_data):
            c = MonsterCard(
                monster=m, 
                position=(start_x + (i * spacing), -0.38), # Bottom Row
                scale=(0.15, 0.22), # Slightly smaller for hand
                on_click=self.on_card_click,
                on_summon_request=self.on_summon_click
            )
            self.cards.append(c)
            
    def on_card_click(self, monster):
        print(f"Card Clicked: {monster.name}")
        from src.ui.card_detail_modal import CardDetailModal
        CardDetailModal(monster)

    def remove_card(self, monster):
        print(f"Removing card for: {monster.name}")
        card_to_remove = None
        for card in self.cards:
            if card.monster == monster:
                card_to_remove = card
                break
        
        if card_to_remove:
            self.cards.remove(card_to_remove)
            destroy(card_to_remove)
            self.rearrange_cards()

    def rearrange_cards(self):
        start_x = -0.35
        spacing = 0.20
        for i, card in enumerate(self.cards):
            card.animate_position((start_x + (i * spacing), -0.38), duration=0.5)
