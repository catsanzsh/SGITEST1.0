from ursina import *

# Check if Ursina initializes
try:
    app = Ursina()
    print("Ursina started successfully, darling~!")
except Exception as e:
    print(f"Oopsie! Ursina failed to start: {e}")
    exit()

# Set a dark background for contrast
window.color = color.rgb(20, 10, 40)  # Deep purple-black
window.title = "Spinning Red Rectangle"
window.borderless = False
window.exit_button.visible = False
print("Background color set, darling~!")

# Create a red 3D rectangle (cuboid)
try:
    red_rectangle = Entity(
        model='cube',  # Base shape
        scale=(2, 0.5, 0.2),  # Flat and wide like a rectangle
        position=(0, 0, -5),  # In front of the camera
        color=color.red,      # Bright red
    )
    print("Red spinning rectangle created, darling~!")
except Exception as e:
    print(f"Rectangle creation failed: {e}")

# Camera setup
camera.position = (0, 0, -10)  # Close enough to see it spin
print("Camera positioned, darling~!")

# Lighting to make it visible
try:
    AmbientLight(color=color.rgba(100, 100, 100, 0.5))  # Soft ambient
    DirectionalLight(color=color.white, direction=(0, -1, -1))  # Direct light
    print("Lighting added to show off that red, darling~!")
except Exception as e:
    print(f"Lighting setup failed: {e}")

# Spin the rectangle in 3D
def update():
    try:
        red_rectangle.rotation_x += time.dt * 90   # Spin on X
        red_rectangle.rotation_y += time.dt * 120  # Spin on Y
        red_rectangle.rotation_z += time.dt * 70   # Spin on Z
    except Exception as e:
        print(f"Update failed: {e}")

# Run the app
try:
    print("Starting the app run, darling~!")
    app.run()
except Exception as e:
    print(f"App crashed during run: {e}")
