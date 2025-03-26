from asset import return_boss_ship ,return_spaceship,enemys
import asset
import random

BOSS_SHIP = return_boss_ship()
SPACESHIP = asset.return_spaceship()
ENEMY = asset.enemys()

BULLET = asset.BULLET
ENEMY_BULLET = asset.ENEMY_BULLET
MAX_HEALTH = asset.MAX_HEALTH
MAX_BULLET_POWER = asset.MAX_BULLET_POWER
HEART_POWERUP = asset.HEART_POWERUP
BULLET_POWERUP = asset.BULLET_POWERUP

# Adjustable formation dimensions
FORMATION_HEIGHT = asset.FORMATION_HEIGHT  # Default number of enemy rows
FORMATION_WIDTH = asset.FORMATION_WIDTH  # Default number of enemy columns


def generate_enemy_formations(width, height, rows, columns):
    """
    Create multiple enemy formation patterns with enhanced characteristics.
    
    Args:
    - width: Total screen width
    - height: Total screen height
    - rows: Number of enemy rows
    - columns: Number of enemy columns
    
    Returns:
    - List of formation generation functions
    """
    def standard_grid(width, height, rows, columns):
        """Standard uniform grid formation"""
        enemies = []
        enemy_width = len(ENEMY[0])
        enemy_height = len(ENEMY)
        horizontal_spacing = enemy_width + 1
        
        start_x = max(1, (width - ((columns * enemy_width) + ((columns - 1) * horizontal_spacing))) // 2)
        start_y = 1
        
        for row in range(rows):
            for col in range(columns):
                x = start_x + (col * (enemy_width + horizontal_spacing))
                y = start_y + (row * enemy_height)
                enemies.append((y, x))
        
        return enemies

    def staggered_formation(width, height, rows, columns):
        """Staggered formation with 3-character side offset and non-overlapping"""
        enemies = []
        enemy_width = len(ENEMY[0])
        enemy_height = len(ENEMY)
        
        # Calculate spacing to ensure full enemy visibility
        horizontal_spacing = enemy_width + 1
        
        start_x = max(1, (width - ((columns * enemy_width) + ((columns - 1) * horizontal_spacing))) // 2)
        start_y = 1
        
        for row in range(rows):
            for col in range(columns):
                x = start_x + (col * (enemy_width + horizontal_spacing))
                
                # 3-character side offset for alternating rows
                # Ensure the offset doesn't cause overlap
                if row % 2 == 1:
                    # Move the entire row's x by 3 character widths
                    x += enemy_width *1
                
                y = start_y + (row * enemy_height)
                enemies.append((y, x))
        
        return enemies

    def triangular_formation(width, height, rows, columns):
        """Triangular formation with progressive inner reduction"""
        enemies = []
        enemy_width = len(ENEMY[0])
        enemy_height = len(ENEMY)
        horizontal_spacing = enemy_width + 1
        
        start_x = max(1, width // 2)
        start_y = 1
        
        for row in range(rows):
            # Progressive reduction of enemies in each row
            row_enemies = columns - row
            for col in range(row_enemies):
                # Center the row and progressively reduce from both sides
                x = start_x + (col * (enemy_width + horizontal_spacing)) - ((row_enemies * (enemy_width + horizontal_spacing)) // 2)
                y = start_y + (row * enemy_height)
                enemies.append((y, x))
        
        return enemies

    def wave_formation(width, height, rows, columns):
        """Identical to standard grid formation"""
        return standard_grid(width, height, rows, columns)

    def zigzag_formation(width, height, rows, columns):
        """Zigzag formation with 3-space movement"""
        enemies = []
        enemy_width = len(ENEMY[0])
        enemy_height = len(ENEMY)
        horizontal_spacing = enemy_width + 1
        
        start_x = max(1, (width - ((columns * enemy_width) + ((columns - 1) * horizontal_spacing))) // 2)
        start_y = 1
        
        # 3-space movement horizontally
        move_spaces = enemy_width * 1
        
        for row in range(rows):
            for col in range(columns):
                x = start_x + (col * (enemy_width + horizontal_spacing))
                # Alternate horizontal offset for each row with 3-space movement
                x += move_spaces if col % 2 == row % 2 else 0
                y = start_y + (row * enemy_height)
                enemies.append((y, x))
        
        return enemies

    # Return list of formation functions
    return [
        standard_grid,
        staggered_formation,
        triangular_formation,
        wave_formation,
        zigzag_formation  
    ]

def generate_random_enemy_formation(width, height, rows, columns):
    """
    Select and generate a random enemy formation.
    
    Args:
    - width: Total screen width
    - height: Total screen height
    - rows: Number of enemy rows
    - columns: Number of enemy columns
    
    Returns:
    - List of enemy positions
    """
    # Get all formation functions
    formations = generate_enemy_formations(width, height, rows, columns)
    
    # Randomly select and generate a formation
    chosen_formation = random.choice(formations)
    return chosen_formation(width, height, rows, columns)
