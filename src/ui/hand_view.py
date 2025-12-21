from ursina import *
from src.ui.monster_card import MonsterCard
from src.core.dataclasses import Monster, Pattern

class HandView(Entity):
    def __init__(self, engine=None, on_summon_click=None):
        super().__init__(parent=camera.ui)
        self.engine = engine
        self.cards = []
        self.on_summon_click = on_summon_click
        
        # Initial Draw if engine ready
        if self.engine:
            self.refresh_hand(self.engine.get_current_player())
        
    def update(self):
        if self.engine:
            player = self.engine.get_current_player()
            # Safety check if player exists
            if player:
                summ_crests = player.crests.get('SUMMON', 0)
                can_summon = summ_crests >= 2
                for c in self.cards:
                    c.set_summonable(can_summon)

    def refresh_hand(self, player_state):
        # 1. Clear existing
        for c in self.cards:
            destroy(c)
        self.cards.clear()
        
        # 2. Re-create for current player
        # Sort by name for consistent order
        hand_list = sorted(player_state.hand, key=lambda m: m.name)
        
        start_x = -0.35
        spacing = 0.20
        
        print(f"Refeshing Hand for Player {player_state.player_id}. Count: {len(hand_list)}")
        
        for i, m in enumerate(hand_list):
            c = MonsterCard(
                monster=m, 
                position=(start_x + (i * spacing), -1.5), # Start off-screen
                scale=(0.15, 0.22), # Slightly smaller for hand
                on_click=self.on_card_click,
                on_summon_request=self.on_summon_click
            )
            c.animate_position((start_x + (i * spacing), -0.38), duration=0.5, delay=i*0.1)
            self.cards.append(c)

    def on_card_click(self, monster):
        print(f"Card Clicked: {monster.name}")
        from src.ui.card_detail_modal import CardDetailModal
        CardDetailModal(monster)

    def remove_card(self, monster):
        print(f"Removing card for: {monster.name}")
        
        # Also remove from Data Model
        if self.engine:
            player = self.engine.get_current_player()
            if monster in player.hand:
                player.hand.remove(monster)
        
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
