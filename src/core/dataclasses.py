from enum import Enum
from typing import List, Tuple, Optional
from pydantic import BaseModel, Field

class DieFace(str, Enum):
    SUMMON = "SUMMON"
    MOVEMENT = "MOVEMENT"
    ATTACK = "ATTACK"
    DEFENSE = "DEFENSE"
    MAGIC = "MAGIC"
    TRAP = "TRAP"

class Pattern(BaseModel):
    """
    Represents the shape of the unfolded die.
    List of (x, y) relative coordinates.
    (0, 0) is typically the center or the position of the monster.
    """
    shape: List[Tuple[int, int]]

class Monster(BaseModel):
    name: str
    level: int
    hp: int
    atk: int
    defense: int = Field(alias="def") # 'def' is a reserved keyword
    pattern: Pattern
    effects: List[str] = [] # List of Effect IDs
    type: str = "Warrior" # Default type
    description: str = ""
    texture_path: Optional[str] = None
    miniature_path: Optional[str] = None
    
    class Config:
        populate_by_name = True

class PlayerState(BaseModel):
    player_id: int
    hp: int = 3 # Dungeon Master HP
    crests: dict[DieFace, int] = {
        DieFace.SUMMON: 0,
        DieFace.MOVEMENT: 0,
        DieFace.ATTACK: 0,
        DieFace.DEFENSE: 0,
        DieFace.MAGIC: 0,
        DieFace.TRAP: 0
    }
    # List of owned monster IDs or references could go here
