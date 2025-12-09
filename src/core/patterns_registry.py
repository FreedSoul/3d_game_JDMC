from src.core.dataclasses import Pattern

# Standard DDM Unfold Patterns (6 cells)
# Coordinates are relative to a center point (usually the monster location)

PATTERNS = {
    "CROSS": Pattern(shape=[(0,0), (0,1), (0,-1), (1,0), (-1,0), (0,2)]),
    "T_SHAPE": Pattern(shape=[(0,0), (0,1), (0,-1), (1,0), (-1,0), (0, -2)]),
    "L_SHAPE": Pattern(shape=[(0,0), (0,1), (0,2), (0,-1), (1,-1), (2,-1)]),
    "LINE": Pattern(shape=[(0,0), (0,1), (0,2), (0,-1), (0,-2), (0,3)]),
    "Z_SHAPE": Pattern(shape=[(0,0), (1,0), (1,1), (0,-1), (-1,-1), (-1,-2)]),
    "H_SHAPE": Pattern(shape=[(0,0), (0,1), (0,-1), (1,1), (1,-1), (-1,0)]),
    # Add more as needed, these are just examples of 6-connected shapes
}
