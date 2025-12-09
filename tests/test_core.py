import pytest
from src.core.grid import Grid
from src.core.dataclasses import Pattern

@pytest.fixture
def grid():
    return Grid()

def test_grid_initialization(grid):
    assert grid.width == 13
    assert grid.height == 19
    assert grid.get_cell(0, 0) is not None
    assert grid.get_cell(13, 19) is None # Out of bounds

def test_pattern_rotation(grid):
    # Shape: L-shape
    # (0,0), (0,1), (1,1)
    pattern = Pattern(shape=[(0,0), (0,1), (1,1)])
    
    # 0 rotations
    assert grid.rotate_pattern(pattern, 0) == [(0,0), (0,1), (1,1)]
    
    # 1 rotation (90 deg clockwise)
    # (x, y) -> (y, -x)
    # (0,0) -> (0,0)
    # (0,1) -> (1,0)
    # (1,1) -> (1,-1)
    rotated = grid.rotate_pattern(pattern, 1)
    assert (1,0) in rotated
    assert (1,-1) in rotated
    assert (0,0) in rotated

def test_validate_dimension_boundaries(grid):
    pattern = Pattern(shape=[(0,0)])
    # Place at valid spot
    # But we need adjacency first. Let's set a DM or owned cell.
    grid.set_owner(5, 5, 1)
    
    # Try to place adjacent
    assert grid.validate_dimension(1, pattern, 5, 6) == True
    
    # Try to place out of bounds
    assert grid.validate_dimension(1, pattern, -1, 0) == False

def test_validate_dimension_collision(grid):
    pattern = Pattern(shape=[(0,0)])
    grid.set_owner(5, 5, 1)
    
    # Try to place ON TOP of existing
    assert grid.validate_dimension(1, pattern, 5, 5) == False

def test_validate_dimension_adjacency(grid):
    pattern = Pattern(shape=[(0,0)])
    grid.set_owner(5, 5, 1)
    
    # Adjacent
    assert grid.validate_dimension(1, pattern, 5, 6) == True
    
    # Not adjacent
    assert grid.validate_dimension(1, pattern, 7, 7) == False
    
    # Adjacent to ENEMY (should fail)
    grid.set_owner(8, 8, 2)
    assert grid.validate_dimension(1, pattern, 8, 9) == False
