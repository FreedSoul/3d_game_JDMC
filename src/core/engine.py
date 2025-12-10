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
        # Force 2 Summon Crests, 1 Movement, 1 Attack - JUST FOR TESTING
        results = {
            DieFace.SUMMON: 2,
            DieFace.MOVEMENT: 10,
            DieFace.ATTACK: 1
        }
        self.add_crests(self.current_player_id, results)
        return results

    def summon_monster(self, player_id: int, monster_id: str, x: int, y: int):
        """
        Spawns a monster at x,y. For MVP testing.
        """
        cell = self.grid.get_cell(x, y)
        if cell:
            cell.monster_id = monster_id
            cell.monster_owner_id = player_id

    def execute_move(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        player = self.get_current_player()
        
        move_power = player.crests.get(DieFace.MOVEMENT, 0)
        valid_moves = self.grid.get_valid_moves(from_x, from_y, move_power, player.player_id)
        
        if (to_x, to_y) not in valid_moves:
            return False
            
        # Re-calculate simple cost (Manhattan)
        dist = abs(from_x - to_x) + abs(from_y - to_y)
        
        if move_power < dist:
            return False
            
        player.crests[DieFace.MOVEMENT] -= dist
        
        self.grid.move_monster(from_x, from_y, to_x, to_y)
        return True

    def execute_attack(self, attacker_x: int, attacker_y: int, target_x: int, target_y: int) -> tuple[bool, str]:
        attacker_cell = self.grid.get_cell(attacker_x, attacker_y)
        target_cell = self.grid.get_cell(target_x, target_y)
        
        if not attacker_cell or not target_cell:
            return False, "Invalid cell"
            
        if not attacker_cell.monster_id or not target_cell.monster_id:
            return False, "No monster found"

        # Range Check (Adjacent only for MVP)
        dist = abs(attacker_x - target_x) + abs(attacker_y - target_y)
        if dist != 1:
            return False, "Target out of range"

        # Cost Check
        player = self.players.get(attacker_cell.monster_owner_id)
        if player.crests.get(DieFace.ATTACK, 0) < 1:
            return False, "Not enough Attack Crests"
            
        # Deduct Crest
        player.crests[DieFace.ATTACK] -= 1
        
        # Calculate Damage (MVP: Fixed 10)
        damage = 10 
        
        # Log Logic
        attacker_name = f"{attacker_cell.monster_id} (P{attacker_cell.monster_owner_id})"
        target_name = f"{target_cell.monster_id} (P{target_cell.monster_owner_id})"
        
        # Action Effect
        target_cell.monster_id = None
        target_cell.monster_owner_id = None
        
        msg = f"{attacker_name} attacked {target_name} for {damage} dmg! Target destroyed!"
        print(msg)
        return True, msg
