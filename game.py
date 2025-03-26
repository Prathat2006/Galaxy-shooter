import os
import random
import time
import keyboard
import asset
from asset import return_boss_ship ,return_spaceship,enemys
from formation import generate_random_enemy_formation
import math
from colorama import init
from colorama import Fore, Back, Style
import json  # Import JSON module for high score handling

def get_terminal_size():
    size = os.get_terminal_size()
    return size.columns, size.lines

BOSS_SHIP = return_boss_ship()
SPACESHIP = asset.return_spaceship()
ENEMY = asset.enemys()

BULLETE= asset.BULLETS
BULLET = asset.BULLET
ENEMY_BULLET = asset.ENEMY_BULLET
MAX_HEALTH = asset.MAX_HEALTH
MAX_BULLET_POWER = asset.MAX_BULLET_POWER
HEART_POWERUP = asset.HEART_POWERUP
BULLET_POWERUP = asset.BULLET_POWERUP
OVER=asset.game_over

# Adjustable formation dimensions
FORMATION_HEIGHT = asset.FORMATION_HEIGHT  # Default number of enemy rows
FORMATION_WIDTH = asset.FORMATION_WIDTH  # Default number of enemy columns
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

HIGH_SCORE_FILE = "highscore.json"

def load_high_score():
    """Load the high score from the JSON file."""
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            data = json.load(f)
            return data.get("high_score", 0)
    return 0

def save_high_score(high_score):
    """Save the high score to the JSON file."""
    with open(HIGH_SCORE_FILE, "w") as f:
        json.dump({"high_score": high_score}, f)

def draw_game(width, height, spaceship_x, bullets, enemies, enemy_bullets, falling_enemies, power_ups, score, health, bullet_power, boss_state, boss_x, boss_y, boss_health, seeking_enemies, round_number):
    screen = [[" " for _ in range(width)] for _ in range(height)]
    
    # Get the current selected base spaceship
    base_ship = None
    if hasattr(asset, 'selected_spaceship'):
        for key, value in asset.base_spaceships.items():
            if value == asset.selected_spaceship:
                base_ship = key
                break
    
    # Determine spaceship design based on bullet power
    if base_ship:
        # Map bullet power to upgrade level (1->base, 2->1, 3->2, 4->3, 5->4)
        upgrade_key = f"{base_ship}{min(max(0, bullet_power - 1), 4)}"
        spaceship_design = asset.upgrade_spaceship.get(upgrade_key, asset.selected_spaceship)
    else:
        spaceship_design = asset.selected_spaceship
    
    # Draw spaceship
    ship_y = height - len(spaceship_design) - 1
    for i, line in enumerate(spaceship_design):
        for j, char in enumerate(line):
            if 0 <= spaceship_x + j - 2 < width:
                screen[ship_y + i][spaceship_x + j - 2] = char
    
    # Draw bullets
    for by, bx in bullets:
        if 0 <= by < height and 0 <= bx < width:  # Ensure bullet is within bounds
            screen[by][bx] = BULLET
    
    # Draw enemies
    for ey, ex in enemies:
        for i, line in enumerate(ENEMY):
            for j, char in enumerate(line):
                if 0 <= int(ey) + i < height and 0 <= int(ex) + j < width:  # Adjusted offset
                    screen[int(ey) + i][int(ex) + j] = char
    
    # Draw enemy bullets
    for by, bx, bullet_type in enemy_bullets:
        if 0 <= int(by) < height and 0 <= int(bx) < width:  # Ensure enemy bullet is within bounds
            screen[int(by)][int(bx)] = bullet_type  # Use the specific bullet type
    
    # Draw falling enemies
    for ey, ex in falling_enemies:
        for i, line in enumerate(ENEMY):
            for j, char in enumerate(line):
                if 0 <= int(ey) + i < height and 0 <= int(ex) + j < width:  # Adjusted offset
                    screen[int(ey) + i][int(ex) + j] = char
    
    # Draw seeking enemies
    for ey, ex in seeking_enemies:
        for i, line in enumerate(ENEMY):
            for j, char in enumerate(line):
                if 0 <= int(ey) + i < height and 0 <= int(ex) + j < width:  # Adjusted offset
                    screen[int(ey) + i][int(ex) + j] = char
    
    # Draw power-ups
    for py, px, power_type in power_ups:
        if 0 <= py < height and 0 <= px < width:
            screen[int(py)][int(px)] = HEART_POWERUP if power_type == "heart" else BULLET_POWERUP
    
    # Draw boss if active
    if boss_state == "appearing":
        for i, line in enumerate(BOSS_SHIP):
            for j, char in enumerate(line):
                if 0 <= int(boss_y) + i < height and 0 <= int(boss_x) + j < width:
                    screen[int(boss_y) + i][int(boss_x) + j] = char
    elif boss_state == "active":
        for i, line in enumerate(BOSS_SHIP):
            for j, char in enumerate(line):
                if 0 <= int(boss_y) + i < height and 0 <= int(boss_x) + j < width:
                    screen[int(boss_y) + i][int(boss_x) + j] = char
    
    # Build the status line
    status = f"Round: {round_number} | Score: {score} | Health: {'❤️' * health} | Bullet Power: {'⚡' * bullet_power} | HIGH SCORE: {load_high_score()}"
    if boss_state in ["appearing", "active"]:
        bar_length = 30
        health_percentage = boss_health / 4000
        filled_length = int(bar_length * health_percentage)
        health_bar = "█" * filled_length + "░" * (bar_length - filled_length)
        status += f" | Boss Health: [{health_bar}] {boss_health}"
    
    # Combine the screen into a single string
    output = "\n".join("".join(row) for row in screen)
    output = f"{status}\n{output}"
    
    # Print the entire frame at once
    clear_screen()
    print(output)

def print_centered_message(message, width, height, score):
    """Helper function to print a multi-line message centered on the screen."""
    clear_screen()
    vertical_padding = (height - len(message)) // 2
    print("\n" * vertical_padding, end="")  # Add vertical padding
    for line in message:
        horizontal_padding = (width - len(line)) // 2
        print(" " * horizontal_padding + line)
    
    # Load the high score
    high_score = load_high_score()
    
    # Check if the current score is greater than the high score
    if score > high_score:
        high_score = score
        save_high_score(high_score)
        print("\n" + " " * horizontal_padding, " " * (horizontal_padding//2)," "*8,Fore.GREEN + "NEW HIGH SCORE!" + Style.RESET_ALL)
    
    # Display the score and high score
    print("\n" + " " * horizontal_padding, Fore.CYAN + f"YOUR SCORE: {score}" + Style.RESET_ALL, " " * horizontal_padding,Fore.YELLOW + f"HIGH SCORE: {high_score}" + Style.RESET_ALL)
    print(" " * horizontal_padding, )
    print(" " * horizontal_padding, )
    print(" " * horizontal_padding, )
    print(" " * horizontal_padding, )
    
    time.sleep(3)  # Pause for 3 seconds before exiting

def game_loop():
    width, height = get_terminal_size()
    width = max(40, width - 2)  # Ensure a minimum width
    height = max(20, height - 5)  # Ensure a minimum height

    round_number = 1
    spaceship_x = width // 2
    bullets = []
    
    # Start with a random enemy formation
    enemies = generate_random_enemy_formation(width, height, rows=FORMATION_HEIGHT, columns=FORMATION_WIDTH)
    
    enemy_bullets = []
    
    falling_enemies = []
    seeking_enemies = []  # List of (y, x) tuples for seeking enemies
    power_ups = []  # List of (y, x, type) tuples
    score = 0
    health = 3
    bullet_power = 1  # Number of bullets fired at once
    last_shot_time = 0
    shot_delay = 0.2
    last_enemy_shot_time = 0
    enemy_shot_delay = 1.5
    last_falling_enemy_time = 0
    falling_enemy_delay = 3.0
    last_seeking_enemy_time = 0
    seeking_enemy_delay = 2.0  # Spawn seeking enemy every 2 seconds
    
    # Boss variables
    boss_state = "inactive"  # inactive, appearing, active
    missiles = []
    boss_x = width // 2 - len(BOSS_SHIP[0]) // 2
    boss_y = -len(BOSS_SHIP)
    boss_health = 4000
    boss_direction = 1  # 1 for right, -1 for left
    boss_speed = 0.5
    last_boss_shot_time = 0
    boss_shot_delay = 1.0
    player_frozen = False
    last_boss_player_bullet_time = 0  # Track time for boss firing player-type bullets
    boss_player_bullet_delay = 0.2  # Delay between each boss player-type bullet
    last_boss_pipe_bullet_time = 0  # Track time for boss firing '|' bullets
    boss_pipe_bullet_delay = 0.2  # Delay between each boss '|' bullet

    # Initialize boss attributes
    boss_attributes = {
        "is_stationary": False,
        "stationary_start_time": 0
    }

    while True:
        width, height = get_terminal_size()
        width = max(40, width - 2)
        height = max(20, height - 5)

        current_time = time.time()
        
        # Move bullets
        bullets = [(by - 1, bx) for by, bx in bullets if by > 0]
        enemy_bullets = [(by + 0.5, bx, bullet_type) for by, bx, bullet_type in enemy_bullets if by < height - 1]
        # enemy_s_bullets = [(by + 0.5, bx) for by, bx in enemy_s_bullets if by < height - 1]
        
        # Move falling enemies towards player
        falling_enemies = [(ey + 0.3, ex + (1 if ex < spaceship_x else -1)) 
                          for ey, ex in falling_enemies if ey < height - 1]
        
        # Move seeking enemies towards player
        seeking_enemies = [(ey + 0.2, ex + (1 if ex < spaceship_x else -1)) 
                          for ey, ex in seeking_enemies if ey < height - 1]
        
        # Move power-ups down
        power_ups = [(py + 0.5, px, power_type) for py, px, power_type in power_ups if py < height - 1]
        
        # Boss logic
        if boss_state == "inactive" and not enemies and not falling_enemies:
            boss_state = "appearing"
            boss_y = -len(BOSS_SHIP)
            player_frozen = True
        
        elif boss_state == "appearing":
            boss_y += 0.5
            if boss_y >= 0:
                boss_state = "active"
                player_frozen = False
        
        elif boss_state == "active":
            # Handle boss movement and stationary behavior
            if boss_attributes["is_stationary"]:
                # Boss is stationary
                if current_time - boss_attributes["stationary_start_time"] >= 9:  # Stay stationary for 9 seconds
                    boss_attributes["is_stationary"] = False
                    boss_direction = random.choice([-1, 1])  # Randomly choose left (-1) or right (1)
                else:
                    # Boss firing 'i' bullets from all 'Y' positions while stationary
                    if current_time - last_boss_pipe_bullet_time >= boss_pipe_bullet_delay:
                        y_offsets = []
                        for i, row in enumerate(BOSS_SHIP):
                            for j, char in enumerate(row):
                                if char == 'Y':
                                    y_offsets.append((i, j))
                        
                        for y_offset in y_offsets:
                            boss_fire_x = boss_x + y_offset[1]
                            boss_fire_y = boss_y + y_offset[0]
                            
                            # Fire 'i' bullets continuously from all 'Y' positions
                            enemy_bullets.append((boss_fire_y + 1, boss_fire_x, BULLETE))  # Use "i" as bullet type
                        
                        last_boss_pipe_bullet_time = current_time

                    if current_time - last_boss_player_bullet_time >= boss_player_bullet_delay:
                        y_offset = None
                        for i, row in enumerate(BOSS_SHIP):
                            for j, char in enumerate(row):
                                if char == 'Y':
                                    y_offset = (i, j)
                                    break
                            if y_offset:
                                break
                            
                        if y_offset:
                            boss_fire_x = boss_x + y_offset[1]
                            boss_fire_y = boss_y + y_offset[0]
                            
                            # Fire player-type bullets continuously
                            enemy_bullets.append((boss_fire_y + 1, boss_fire_x, BULLETE))  # Use ENEMY_BULLET type
                        
                        last_boss_player_bullet_time = current_time                        
                    
                    # Double the bullets fired from 'V' when stationary
                    if current_time - last_boss_shot_time >= boss_shot_delay:
                        v_offset = None
                        for i, row in enumerate(BOSS_SHIP):
                            for j, char in enumerate(row):
                                if char == 'V':
                                    v_offset = (i, j)
                                    break
                            if v_offset:
                                break
                        
                        if v_offset:
                            boss_fire_x = boss_x + v_offset[1]
                            boss_fire_y = boss_y + v_offset[0]
                            
                            # 10 falling bullets spread out from 'V' (doubled)
                            for i in range(10):
                                spread = (i - 4.5) * 3  # Spread bullets horizontally
                                enemy_bullets.append((boss_fire_y + 1, boss_fire_x + spread, ENEMY_BULLET))
                            
                            # 6 seeking bullets from 'V' (doubled)
                            for i in range(6):
                                spread = (i - 2.5) * 3  # Spread bullets horizontally
                                enemy_bullets.append((boss_fire_y + 1, boss_fire_x + spread, ENEMY_BULLET))
                        
                        last_boss_shot_time = current_time
            else:
                # Boss is moving
                boss_x += boss_direction * boss_speed
                if boss_x <= 0 or boss_x + len(BOSS_SHIP[0]) >= width:
                    boss_direction *= -1  # Reverse direction if hitting screen edge
                
                # Randomly decide to stop moving
                if random.random() < 0.01:  # 1% chance per frame to stop
                    boss_attributes["is_stationary"] = True
                    boss_attributes["stationary_start_time"] = current_time

            # Boss shooting (centered on 'V')
            if current_time - last_boss_shot_time >= boss_shot_delay:
                # Find the 'V' character's position in the boss design
                v_offset = None
                for i, row in enumerate(BOSS_SHIP):
                    for j, char in enumerate(row):
                        if char == 'V':
                            v_offset = (i, j)
                            break
                    if v_offset:
                        break
                
                if v_offset:
                    boss_fire_x = boss_x + v_offset[1]
                    boss_fire_y = boss_y + v_offset[0]
                    
                    # 5 falling bullets spread out from 'V'
                    for i in range(5):
                        spread = (i - 2) * 2  # Spread bullets horizontally
                        enemy_bullets.append((boss_fire_y + 1, boss_fire_x + spread, ENEMY_BULLET))  # Use ENEMY_BULLET type
                    
                    # 3 seeking bullets from 'V'
                    for i in range(3):
                        spread = (i - 1) * 3  # Spread bullets horizontally
                        enemy_bullets.append((boss_fire_y + 1, boss_fire_x + spread, ENEMY_BULLET))  # Use ENEMY_BULLET type
                
                last_boss_shot_time = current_time
            
            # Spawn seeking enemies
            if current_time - last_seeking_enemy_time >= seeking_enemy_delay:
                # Spawn at random x position at the top
                spawn_x = random.randint(5, width - 5)
                seeking_enemies.append((0, spawn_x))
                last_seeking_enemy_time = current_time
            
            # Boss firing player-type bullets from 'Y'


        # Check bullet collisions with enemies
        bullets_copy = bullets[:]
        for bullet in bullets_copy:
            for enemy in enemies[:]:
                ey, ex = enemy
                if int(ey) <= bullet[0] <= int(ey) + 2 and int(ex) - 2 <= bullet[1] <= int(ex) + 2:
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                    # Random chance to drop power-up
                    if random.random() < 0.3:  # 30% chance
                        power_type = "heart" if random.random() < 0.5 else "bullet"
                        power_ups.append((int(ey) + 2, int(ex), power_type))
                    break
        
        # Check bullet collisions with falling enemies
        bullets_copy = bullets[:]
        for bullet in bullets_copy:
            for falling_enemy in falling_enemies[:]:
                ey, ex = falling_enemy
                if int(ey) <= bullet[0] <= int(ey) + 2 and int(ex) - 2 <= bullet[1] <= int(ex) + 2:
                    falling_enemies.remove(falling_enemy)
                    bullets.remove(bullet)
                    score += 2
                    # Random chance to drop power-up
                    if random.random() < 0.1:  # 10% chance
                        power_type = "heart" if random.random() < 0.5 else "bullet"
                        power_ups.append((int(ey) + 2, int(ex), power_type))
                    break
        
        # Check bullet collisions with seeking enemies
        bullets_copy = bullets[:]
        for bullet in bullets_copy:
            for seeking_enemy in seeking_enemies[:]:
                ey, ex = seeking_enemy
                if int(ey) <= bullet[0] <= int(ey) + 2 and int(ex) - 2 <= bullet[1] <= int(ex) + 2:
                    seeking_enemies.remove(seeking_enemy)
                    bullets.remove(bullet)
                    score += 3  # More points for seeking enemies
                    # Random chance to drop power-up
                    if random.random() < 0.1:  # 10% chance
                        power_type = "heart" if random.random() < 0.5 else "bullet"
                        power_ups.append((int(ey) + 2, int(ex), power_type))
                    break
        
        # Check bullet collisions with boss
        if boss_state == "active":
            bullets_copy = bullets[:]
            for bullet in bullets_copy:
                if (int(boss_y) <= bullet[0] <= int(boss_y) + len(BOSS_SHIP) and 
                    int(boss_x) <= bullet[1] <= int(boss_x) + len(BOSS_SHIP[0])):
                    bullets.remove(bullet)
                    boss_health -= bullet_power
                    if boss_health <= 0:
                        print(f"Congratulations! You defeated the boss in Round {round_number}! Score: {score}")
                        round_number += 1
                        # Reset game state for next round
                        enemies = generate_random_enemy_formation(width, height, rows=FORMATION_HEIGHT, columns=FORMATION_WIDTH)
                        enemy_shot_delay *= 0.8  # Increase enemy shooting speed
                        falling_enemy_delay *= 0.8  # Increase falling enemy spawn rate
                        seeking_enemy_delay *= 0.8  # Increase seeking enemy spawn rate
                        boss_health = 4000 + (round_number - 1) * 1000  # Increase boss health
                        boss_speed += 0.2  # Increase boss speed
                        boss_state = "inactive"
                        player_frozen = False
                        break
        
        # Check bullet collisions with enemy bullets
        bullets_copy = bullets[:]
        for bullet in bullets_copy:
            for enemy_bullet in enemy_bullets[:]:
                if abs(bullet[0] - enemy_bullet[0]) <= 1 and abs(bullet[1] - enemy_bullet[1]) <= 1:
                    bullets.remove(bullet)
                    enemy_bullets.remove(enemy_bullet)
                    break
        
        # Check player collision with enemy bullets
        for bullet in enemy_bullets[:]:
            if height - 4 <= bullet[0] < height and spaceship_x - 2 <= bullet[1] <= spaceship_x + 2:
                health -= 1
                # Lose one bullet power when taking damage
                if bullet_power > 1:
                    bullet_power -= 1
                enemy_bullets.remove(bullet)
                if health <= 0:
                    print_centered_message(OVER, width, height, score)
                    return
        
        # Check player collision with falling enemies
        for falling_enemy in falling_enemies[:]:
            ey, ex = falling_enemy
            if height - 4 <= int(ey) < height and spaceship_x - 2 <= int(ex) <= spaceship_x + 2:
                health -= 2  # Falling enemies do more damage
                # Lose two bullet power when hit by falling enemy
                if bullet_power > 1:
                    bullet_power = max(1, bullet_power - 2)
                falling_enemies.remove(falling_enemy)
                if health <= 0:
                    print_centered_message(OVER, width, height, score)
                    return
        
        # Check player collision with seeking enemies
        for seeking_enemy in seeking_enemies[:]:
            ey, ex = seeking_enemy
            if height - 4 <= int(ey) < height and spaceship_x - 2 <= int(ex) <= spaceship_x + 2:
                health -= 3  # Seeking enemies do more damage
                # Lose three bullet power when hit by seeking enemy
                if bullet_power > 1:
                    bullet_power = max(1, bullet_power - 3)
                seeking_enemies.remove(seeking_enemy)
                if health <= 0:
                    print_centered_message(OVER, width, height, score)
                    return
        
        # Check player collision with power-ups
        for power_up in power_ups[:]:
            py, px, power_type = power_up
            if height - 4 <= int(py) < height and spaceship_x - 2 <= int(px) <= spaceship_x + 2:
                if power_type == "heart" and health < MAX_HEALTH:  # Max health is 5
                    health += 1
                    score += 10
                elif power_type == "bullet" and bullet_power < MAX_BULLET_POWER:  # Max bullet power is 5
                    bullet_power += 1
                    score += 10
                else:
                    score += 50  # Extra points for collecting power-ups
                power_ups.remove(power_up)
        
        # Enemy shooting with increasing randomness
        if current_time - last_enemy_shot_time >= enemy_shot_delay and enemies:
            # More random number of shooters with higher rounds
            max_shooters = min(5, 2 + round_number)
            shooters = random.sample(enemies, min(max_shooters, len(enemies)))
            for enemy in shooters:
                # Add some randomness to shooting
                if random.random() < 0.7 + (round_number * 0.05):  # Increase shooting probability
                    enemy_bullets.append((int(enemy[0]) + 3, int(enemy[1]), ENEMY_BULLET))
            last_enemy_shot_time = current_time
        
        # Spawn falling enemies from existing enemies
        if current_time - last_falling_enemy_time >= falling_enemy_delay and enemies:
            # Choose a random enemy to fall
            falling_enemy = random.choice(enemies)
            enemies.remove(falling_enemy)  # Remove from original position
            falling_enemies.append(falling_enemy)  # Add to falling enemies
            last_falling_enemy_time = current_time
        
        # Handle input (only if player is not frozen)
        if not player_frozen:
            if keyboard.is_pressed('left') and spaceship_x > 2:
                spaceship_x -= 1
            if keyboard.is_pressed('right') and spaceship_x < width - 3:
                spaceship_x += 1
            if keyboard.is_pressed('space') and current_time - last_shot_time >= shot_delay:
                # Dynamically determine the spaceship design based on bullet power
                base_ship = None
                if hasattr(asset, 'selected_spaceship'):
                    for key, value in asset.base_spaceships.items():
                        if value == asset.selected_spaceship:
                            base_ship = key
                            break
                
                if base_ship:
                    upgrade_key = f"{base_ship}{min(max(0, bullet_power - 1), 4)}"
                    spaceship_design = asset.upgrade_spaceship.get(upgrade_key, asset.selected_spaceship)
                else:
                    spaceship_design = asset.selected_spaceship

                # Find the 'A' character's position in the current spaceship design
                a_offset = None
                for i, row in enumerate(spaceship_design):
                    for j, char in enumerate(row):
                        if char == 'A':
                            a_offset = (i, j)
                            break
                    if a_offset:
                        break
                
                # Calculate firing point based on 'A' position
                if a_offset:
                    fire_x = spaceship_x + a_offset[1] - 2
                    fire_y = height - len(spaceship_design) + a_offset[0]
                    
                    # Fire bullets based on bullet power
                    if bullet_power % 2 == 1:
                        # Odd number of bullets: center bullet at 'A'
                        bullets.append((fire_y - 1, fire_x))
                        
                        # Additional bullets on sides
                        for i in range(1, (bullet_power + 1) // 2):
                            bullets.append((fire_y - 1, fire_x - i * 2))  # Left side
                            bullets.append((fire_y - 1, fire_x + i * 2))  # Right side
                    else:
                        # Even number of bullets: split evenly on both sides of 'A'
                        for i in range(1, bullet_power // 2 + 1):
                            bullets.append((fire_y - 1, fire_x - (2 * i - 1)))  # Left side
                            bullets.append((fire_y - 1, fire_x + (2 * i - 1)))  # Right side
                
                last_shot_time = current_time
        if keyboard.is_pressed('q'):
            break
        
        draw_game(width, height, spaceship_x, bullets, enemies, enemy_bullets, falling_enemies, power_ups, score, health, bullet_power, boss_state, boss_x, boss_y, boss_health, seeking_enemies, round_number)
        time.sleep(1/20)  # Cap at 30 frames per second (best is 10 frames per second)

if __name__ == "__main__":
    game_loop()