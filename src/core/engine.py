from typing import Dict
from src.core.grid import Grid
from src.core.dataclasses import PlayerState, DieFace

class GameEngine:
    def __init__(self):
        self.grid = Grid()
        self.players: Dict[int, PlayerState] = {
            1: PlayerState(player_id=1),
            2: PlayerState(player_id=2)
        }
        self.current_player_id = 1
        self.turn_count = 1
        
        # Initialize Dungeon Masters (simplified for now)
        # Player 1 DM at (6, 0) - Bottom center
        self.grid.set_owner(6, 0, 1)
        self.grid.get_cell(6, 0).is_dungeon_master = True
        
        # Player 2 DM at (6, 18) - Top center
        self.grid.set_owner(6, 18, 2)
        self.grid.get_cell(6, 18).is_dungeon_master = True

    def next_turn(self):
        self.current_player_id = 2 if self.current_player_id == 1 else 1
        if self.current_player_id == 1:
            self.turn_count += 1

    def add_crests(self, player_id: int, crests: Dict[DieFace, int]):
        player = self.players.get(player_id)
        if player:
            for face, amount in crests.items():
                player.crests[face] += amount

    def get_current_player(self) -> PlayerState:
        return self.players[self.current_player_id]

    def roll_dice(self) -> Dict[DieFace, int]:
        """
        Simulate rolling 3 dice.
        For MVP Phase 3, we force a specific result to test Dimensioning.
        """
        # TODO: Implement real random logic later
        # Force 2 Summon Crests (Level 1) + 1 Movement - JUST FOR TESTING
        results = {
            DieFace.SUMMON: 2,
            DieFace.MOVEMENT: 1
        }
        self.add_crests(self.current_player_id, results)
        return results
