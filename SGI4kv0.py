# test.py
from ursina import *
import math
import time
from pathlib import Path
import sys # Import sys to get the script name

# --- Initialization ---
# Initialize the Ursina application
app = Ursina(title="Ultra Mario FX [C] Team Flames 20XX")

# --- Scene Setup ---
# Set background color
window.color = color.rgb(20, 10, 40)
# Hide the default exit button
window.exit_button.visible = False

# Create a Mode 7-style ground plane
ground = Entity(
    model='plane',
    scale=(50, 1, 50),
    texture='white_cube',
    texture_scale=(25, 25), # Tile the texture
    color=color.rgb(100, 100, 100) # Grey color
)

# Create a placeholder for Mario (a red cube)
mario = Entity(
    model='cube',
    scale=(0.5, 1, 0.5),
    position=(0, 0.5, 0), # Position slightly above the ground
    color=color.red
)
# Create a yellow ring around Mario
ring = Entity(
    model='circle',
    scale=2,
    position=(0, 0.5, 0),
    color=color.yellow,
    double_sided=True # Make visible from both sides
)
ring.alpha = 0.5 # Make it semi-transparent

# --- Lighting ---
# Add subtle ambient light
AmbientLight(color=color.rgba(0.3, 0, 0.5, 1))
# Add a directional light source
DirectionalLight(color=color.white, direction=(1, -1, -1)) # Shining from top-right towards bottom-left

# --- UI Elements ---
# Text for the initial boot menu prompt
menu_text = Text(
    text="> PRESS ENTER TO LOOK BEYOND THE CURSED MIRROR <",
    origin=(0, 0), # Center the text origin
    scale=1.2,
    y=0.4, # Position vertically
    z=-1, # Position slightly in front of the camera default
    color=color.white
)
# Text for the game logo
logo_text = Text(
    text="ULTRA MARIO FX",
    origin=(0, 0),
    scale=2,
    y=0.47,
    z=-1,
    color=color.yellow
)

# --- Camera Setup ---
camera.z = -10 # Initial camera distance from origin
camera.y = 5  # Initial camera height
tilt_angle = 0 # Variable for camera tilt animation
zoom_speed = 0.015 # Speed for camera zoom animation

# --- Game State Variables ---
spin_speed = 0      # Current speed of Mario's spin
spin_direction = 0  # Direction of spin (1 or -1)
pulse_time = 0      # Timer for the ring's pulsing effect
game_started = False # Flag indicating if the initial 'enter' has been pressed
engine_mode = None   # Current game mode ('simulation', 'memory_leak', or None)

# --- File Generation ---
# Generate main_menu.txt if it doesn't exist, containing the secondary menu options
prompt_file = Path("main_menu.txt")
if not prompt_file.exists():
    try:
        with open(prompt_file, "w") as f:
            f.write(
                "WELCOME TO ULTRA MARIO FX CORE\n"
                "-------------------------------\n"
                "You have crossed into the mirror space.\n\n"
                "[1] Start Simulation\n"
                "[2] Load Memory Leak\n"
                "[3] Exit to Title\n\n"
                "Press a key to continue... if you dare.\n"
            )
        print(f"Generated menu file: {prompt_file}")
    except Exception as e:
        print(f"Error creating {prompt_file}: {e}")
        # Optionally handle the error, e.g., by quitting or setting a default state
        # application.quit()


# --- Functions ---
def self_patch():
    """
    Self-patches this program by making a backup of the current source
    and writing the current source (plus a patch timestamp) back to the
    original script file.
    """
    try:
        # Get the path of the currently running script
        current_file = Path(__file__).resolve()
        # Create a backup filename based on the current script's name
        backup_file = current_file.with_name(f"{current_file.stem}_backup.py")

        # Read the current source code
        current_code = current_file.read_text()

        # Create a backup of the current source code.
        backup_file.write_text(current_code)
        print(f"Backup saved as {backup_file.name}")

        # Prepare the new code with a patch timestamp comment
        patch_comment = f"\n# Self patched on {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        new_code = current_code + patch_comment

        # Write the updated code back to the original script file
        with open(current_file, "w") as f:
            f.write(new_code)

        print(f"Self patch complete. Updated code written to {current_file.name}.")
        print("Please restart the application to apply changes.")
        # Optional: Automatically quit after patching
        # application.quit()

    except Exception as e:
        print(f"Error during self-patch: {e}")


def update():
    """
    Called every frame by Ursina. Handles game logic updates,
    animations, and camera movement.
    """
    global tilt_angle, spin_speed, spin_direction, pulse_time, zoom_speed, game_started, engine_mode

    # --- Camera Animation ---
    # Oscillate camera tilt
    tilt_angle += time.dt * 5 # Increment angle based on frame time
    camera.rotation_x = math.sin(tilt_angle * 0.05) * 8 # Apply sinusoidal tilt

    # Oscillate camera zoom
    camera.z += zoom_speed * time.dt * 60 # Adjust zoom based on speed and frame time (scaled for consistency)
    # Reverse zoom direction at boundaries
    if camera.z > -6 or camera.z < -12:
        zoom_speed *= -1

    # --- Game Logic (Only if a mode is selected) ---
    if game_started and engine_mode:
        # Hide title screen text once a mode is running
        if menu_text.enabled:
            menu_text.enabled = False
            logo_text.enabled = False

        # --- Mario Spin and Animation ---
        if spin_speed != 0:
            # Apply rotation based on speed and direction
            mario.rotation_y += spin_speed * spin_direction * time.dt * 360
            ring.rotation_y += spin_speed * spin_direction * time.dt * 180 # Ring spins slower

            # Bob Mario up and down slightly while spinning
            mario.y = 0.5 + math.sin(time.time() * 5) * 0.05

            # Change color and scale based on spin direction
            if spin_direction > 0: # Clockwise (space)
                mario.color = color.orange
                mario.scale = (0.6, 1.2, 0.6) # Slightly larger/taller
            else: # Counter-clockwise (c)
                mario.color = color.blue
                mario.scale = (0.4, 0.8, 0.4) # Slightly smaller/shorter
        else:
            # Reset Mario's appearance when not spinning
            mario.color = color.red
            mario.scale = (0.5, 1, 0.5)
            mario.y = 0.5 # Reset vertical position

        # --- Ring Pulse Animation ---
        pulse_time += time.dt # Increment pulse timer
        # Oscillate ring scale using sine wave
        ring.scale = 2 + math.sin(pulse_time * 3) * 0.1
        # Oscillate ring alpha (transparency) using sine wave
        ring.alpha = 0.5 + math.sin(pulse_time * 3) * 0.2


def input(key):
    """
    Called by Ursina when a key is pressed or released.
    Handles user input for game state changes and controls.
    """
    global spin_speed, spin_direction, game_started, engine_mode

    # --- Initial Start ---
    # On first 'enter' press, show the secondary menu from the file
    if key == 'enter' and not game_started:
        print("\n>> Initiating FX Core... Welcome to the other side.")
        try:
            with open("main_menu.txt", "r") as f:
                print(f.read())
            game_started = True # Mark that the initial prompt has passed
            menu_text.text = "SELECT MODE [1], [2], or [3]" # Update prompt text
            menu_text.y = 0.1 # Reposition prompt
            logo_text.enabled = False # Hide logo during mode select
        except FileNotFoundError:
            print(f"Error: main_menu.txt not found. Cannot proceed.")
            # Optionally disable further input or quit
            # application.quit()
        except Exception as e:
             print(f"Error reading main_menu.txt: {e}")
             # application.quit()


    # --- Mode Selection ---
    # Only allow mode selection if 'enter' was pressed but no mode is active yet
    if game_started and not engine_mode:
        if key == '1':
            engine_mode = "simulation"
            print(">> Booting into Simulation Mode...")
            # menu_text.enabled = False # Text disabled in update() now
        elif key == '2':
            engine_mode = "memory_leak"
            print(">> Warning: Memory Leak Mode Engaged...")
            # menu_text.enabled = False
        elif key == '3':
            print(">> Returning to Title...")
            application.quit() # Exit the application

    # --- In-Game Controls (Only if a mode is active) ---
    if engine_mode:
        # Start spinning clockwise on 'space' press
        if key == 'space':
            spin_speed = 1
            spin_direction = 1
        # Start spinning counter-clockwise on 'c' press
        elif key == 'c':
            spin_speed = 1
            spin_direction = -1
        # Stop spinning when 'space' or 'c' is released
        elif key in ['space up', 'c up']:
            spin_speed = 0

    # --- Self-Patch Command ---
    # Trigger self-patching mechanism on 'p' press
    if key == 'p':
        print("\n>> Initiating self-patch sequence...")
        self_patch()

# --- Run Application ---
# Start the Ursina game loop
app.run()
