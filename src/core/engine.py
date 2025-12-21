from typing import Dict
import random
from src.core.grid import Grid
from src.core.dataclasses import PlayerState, DieFace
from src.core.constants import Phase

class GameEngine:
    def __init__(self):
        self.grid = Grid()
        self.players: Dict[int, PlayerState] = {
            1: PlayerState(player_id=1),
            2: PlayerState(player_id=2)
        }
        
        # Load and Distribute Monsters
        from src.core.monster_loader import MonsterLoader
        all_monsters = MonsterLoader.load_monsters("data/monsters")
        
        # Simple split: Evens to P1, Odds to P2 (or split half/half)
        # We need to make copies if we want independent instances, 
        # but for now shared reference (read-only stats) is fine, 
        # BUT 'hand' is a list on PlayerState, so that is distinct.
        # Wait - if we modify the Monster object (e.g. current HP), we need deep copies.
        # Currently Monster is a Pydantic model. 
        # Let's just distribute references for now, assuming base stats don't execute logic on the card instance itself 
        # (logic should be on the board instance).
        
        # Split logic:
        mid_idx = len(all_monsters) // 2
        # P1 gets first half, P2 gets second half
        # To ensure fair distribution of types, maybe alternating?
        
        for i, monster in enumerate(all_monsters):
            if i % 2 == 0:
                self.players[1].hand.append(monster)
            else:
                self.players[2].hand.append(monster)
        
        self.current_player_id = 1
        self.turn_count = 1
        self.current_phase = Phase.ROLL
        
        # Initialize Dungeon Masters (simplified for now)
        # Player 1 DM at (6, 0) - Bottom center
        self.grid.set_owner(6, 0, 1)
        self.grid.get_cell(6, 0).is_dungeon_master = True
        
        # Player 2 DM at (6, 18) - Top center
        self.grid.set_owner(6, 18, 2)
        self.grid.get_cell(6, 18).is_dungeon_master = True

    def next_phase(self):
        """Cycles through phases: ROLL -> MAIN -> ATTACK -> ADJUST -> END"""
        if self.current_phase == Phase.ROLL:
            self.current_phase = Phase.MAIN
        elif self.current_phase == Phase.MAIN:
            self.current_phase = Phase.ATTACK
        elif self.current_phase == Phase.ATTACK:
            self.current_phase = Phase.ADJUST
        elif self.current_phase == Phase.ADJUST:
             # Typically next is END, enabling 'End Turn' button
             # Or we can auto-end? User says "until the last phase, the button end turn will be activated"
             # So 'next phase' from ADJUST leads to a state where End Turn is active.
             # Let's say the phase *is* END, and in END phase, End Turn button works.
             self.current_phase = Phase.END

        print(f"Phase Changed to: {self.current_phase.value}")
        return self.current_phase

    def end_turn(self):
        """Ends the turn and passes to next player, resetting phase."""
        self.current_player_id = 2 if self.current_player_id == 1 else 1
        self.current_phase = Phase.ROLL # Reset to Roll
        if self.current_player_id == 1:
            self.turn_count += 1
        print(f"Turn Ended. Now Player {self.current_player_id} - {self.current_phase.value}")

    def add_crests(self, player_id: int, crests: Dict[DieFace, int]):
        player = self.players.get(player_id)
        if player:
            for face, amount in crests.items():
                player.crests[face] += amount

    def remove_crests(self, player_id: int, crests: Dict[DieFace, int]) -> bool:
        player = self.players.get(player_id)
        if not player:
            return False
            
        # 1. Check if affordable
        for face, cost in crests.items():
            if player.crests.get(face, 0) < cost:
                return False
                
        # 2. Deduct
        for face, cost in crests.items():
            player.crests[face] -= cost
            
        return True

    def get_current_player(self) -> PlayerState:
        return self.players[self.current_player_id]

    def roll_dice(self) -> Dict[DieFace, int]:
        """
        Simulate rolling 3 dice with real random logic.
        Each die has 6 faces (Uniform distribution).
        """
        results = {}
        
        # All possible faces
        faces = list(DieFace)
        
        # Roll 3 dice
        rolls = random.choices(faces, k=3)
        
        for roll in rolls:
            results[roll] = results.get(roll, 0) + 1
            
        self.add_crests(self.current_player_id, results)
        return results
    
    def deduct_summon_cost(self, cost=2):
        """Deduct summon crests from current player (default cost: 2)"""
        # Use centralized optional deduction
        if self.remove_crests(self.current_player_id, {DieFace.SUMMON: cost}):
            player = self.get_current_player()
            print(f"Deducted {cost} SUMMON crests. Remaining: {player.crests[DieFace.SUMMON]}")
            return True
            
        print(f"Not enough SUMMON crests.")
        return False


    def summon_monster(self, player_id: int, monster_id: str, x: int, y: int, monster_obj=None):
        """
        Spawns a monster at x,y. For MVP testing.
        """
        cell = self.grid.get_cell(x, y)
        if cell:
            cell.monster_id = monster_id
            cell.monster_owner_id = player_id
            cell.monster_ref = monster_obj

    def execute_move(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        player = self.get_current_player()
        
        move_power = player.crests.get(DieFace.MOVEMENT, 0)
        valid_moves = self.grid.get_valid_moves(from_x, from_y, move_power, player.player_id)
        
        if (to_x, to_y) not in valid_moves:
            return False
            
        # Re-calculate simple cost (Manhattan)
        dist = abs(from_x - to_x) + abs(from_y - to_y)
        
        if not self.remove_crests(player.player_id, {DieFace.MOVEMENT: dist}):
            return False
        
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
        attacker_player = self.players.get(attacker_cell.monster_owner_id)
        if not self.remove_crests(attacker_player.player_id, {DieFace.ATTACK: 1}):
            return False, "Not enough Attack Crests"

        # Stats
        attacker = attacker_cell.monster_ref
        target = target_cell.monster_ref
        
        atk_power = attacker.atk
        def_power = target.defense
        hp_power = target.hp
        
        # Defense Policy: Auto-Spend if available
        defender_player = self.players.get(target_cell.monster_owner_id)
        defense_bonus = 0
        spent_defense = False
        
        if defender_player and defender_player.crests.get(DieFace.DEFENSE, 0) > 0:
            self.remove_crests(defender_player.player_id, {DieFace.DEFENSE: 1})
            defense_bonus = def_power
            spent_defense = True
            
        # Calculation
        resistance = hp_power + defense_bonus
        impact = atk_power - resistance
        
        attacker_name = f"{attacker.name} (P{attacker_cell.monster_owner_id})"
        target_name = f"{target.name} (P{target_cell.monster_owner_id})"
        
        print(f"BATTLE: {attacker_name} [ATK {atk_power}] vs {target_name} [HP {hp_power} + DEF {defense_bonus if spent_defense else 0}]")
        print(f"Impact: {atk_power} - {resistance} = {impact}")

        if impact >= 0:
            # Destroy Target
            msg = f"{attacker_name} destroyed {target_name}! (Impact: {impact})"
            target_cell.monster_id = None
            target_cell.monster_owner_id = None
            target_cell.monster_ref = None
            
            # Remove from defender hand if it was mostly tracking via grid, 
            # but PlayerState.hand only tracked *unsummoned* cards mostly.
            # If we tracked summoned monsters in a list, we'd remove it there too.
            print(msg)
            return True, msg
        else:
            # Attack Failed
            msg = f"{attacker_name} failed to damage {target_name}. (Impact: {impact})"
            print(msg)
            return True, msg
