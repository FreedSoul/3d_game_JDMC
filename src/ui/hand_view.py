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
        # Create 5 Dummy Monsters for MVP
        dummy_pattern = Pattern(shape=[(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)]) # Rect
        
        description_golem = "a formidale construct of raw crystal, its body can deflect even the strongest attacks. it slowly regenerates in contact with earth. "
        
        monsters_data = [
            Monster(
                name="Crystal Golem", 
                level=2, 
                hp=8, 
                atk=30, 
                defense=80, 
                type="Rock",
                description=description_golem,
                texture_path="../../assets/cards/crystal_golem_2.png",
                pattern=dummy_pattern, 
                effects=["E002_HEAL_SELF"]
            ),
            Monster(name="Twin Swords", level=1, hp=10, atk=40, defense=10, type="Warrior", pattern=dummy_pattern, effects=["E001_DOUBLE_ATK"]),
            Monster(name="Blast Lizard", level=2, hp=20, atk=30, defense=10, type="Reptile", pattern=dummy_pattern),
            Monster(name="Dark Magician", level=3, hp=20, atk=50, defense=10, type="Spellcaster", pattern=dummy_pattern),
            Monster(name="Cyber Raider", level=1, hp=10, atk=20, defense=0, type="Machine", pattern=dummy_pattern),
        ]
        
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
