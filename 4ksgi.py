# test.py
from ursina import *
import math    # For math.sin
import time    # For time.time()

app = Ursina(title="Super Mario FX Core Booting...")

# Flat Mode 7-style ground plane with SNES checkerboard vibes
ground = Entity(
    model='plane',
    scale=(50, 1, 50),
    texture='white_cube',
    texture_scale=(25, 25),  # Tighter grid for retro feel
    color=color.rgb(100, 100, 100)  # Softer gray
)

# Low-poly Mario placeholder (cube with a bounce twist!)
mario = Entity(
    model='cube',
    scale=(0.5, 1, 0.5),
    position=(0, 0.5, 0),
    color=color.red
)

# Glowing ring with FX chip pulse
ring = Entity(
    model='circle',
    scale=2,
    position=(0, 0.5, 0),
    color=color.yellow,
    double_sided=True
)
ring.alpha = 0.5

# SGI-style lighting: purple ambient + white key light
AmbientLight(color=color.rgba(0.3, 0, 0.5, 1))
DirectionalLight(color=color.white, direction=(1, -1, -1))

# Camera setup for smoother fly-around
camera.z = -10
camera.y = 5
tilt_angle = 0
zoom_speed = 0.015  # Slower zoom for elegance

# Spin and bonus variables
spin_speed = 0
spin_direction = 0
pulse_time = 0  # For ring glow effect

def update():
    global tilt_angle, spin_speed, spin_direction, pulse_time, zoom_speed

    # Smoother camera fly-around
    tilt_angle += time.dt * 5   # Gentler tilt speed
    camera.rotation_x = math.sin(tilt_angle * 0.05) * 8  # Smoother tilt
    camera.z += zoom_speed
    if camera.z > -6 or camera.z < -12:  # Tighter zoom range
        zoom_speed *= -1

    # Mario spinning with a lil’ bounce
    if spin_speed != 0:
        mario.rotation_y += spin_speed * time.dt * 360
        ring.rotation_y += spin_speed * time.dt * 180
        mario.y = 0.5 + math.sin(time.time() * 5) * 0.05  # Tiny bounce

        # Bonus: Color and size shift
        if spin_direction > 0:  # Clockwise
            mario.color = color.orange
            mario.scale = (0.6, 1.2, 0.6)
        else:  # Counterclockwise
            mario.color = color.blue
            mario.scale = (0.4, 0.8, 0.4)
    else:
        mario.color = color.red
        mario.scale = (0.5, 1, 0.5)
        mario.y = 0.5  # Reset bounce

    # Pulsing ring effect
    pulse_time += time.dt
    ring.scale = 2 + math.sin(pulse_time * 3) * 0.1   # Subtle pulse
    ring.alpha = 0.5 + math.sin(pulse_time * 3) * 0.2 # Glow flicker

def input(key):
    global spin_speed, spin_direction
    if key == 'space':  # Clockwise spin
        spin_speed = 1
        spin_direction = 1
    elif key == 'c':    # Counterclockwise spin
        spin_speed = 1
        spin_direction = -1
    elif key == 'space up' or key == 'c up':  # Snap stop
        spin_speed = 0

app.run()
