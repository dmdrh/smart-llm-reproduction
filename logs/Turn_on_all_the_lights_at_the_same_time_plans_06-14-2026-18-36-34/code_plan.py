```python
def turn_on_light(light_name, robot):
    # Function to turn on a specific light using the specified robot
    GoToObject(robot, light_name)  # Go to the light switch
    SwitchOn(robot, light_name)     # Switch on the light

# List of all light switches to turn on
light_switches = ['LightSwitch1', 'LightSwitch2', 'LightSwitch3', 'LightSwitch4']  # Add all light switches here

# Create a list to hold threads
light_threads = []

# Create and start a thread for each light switch using available robots
for i, light in enumerate(light_switches):
    robot = robots[i % len(robots)]  # Cycle through available robots
    thread = threading.Thread(target=turn_on_light, args=(light, robot['name']))
    light_threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in light_threads:
    thread.join()

# Task to turn on all the lights is done
```

### Explanation:
1. **Function Definition**: The `turn_on_light` function now takes an additional parameter `robot`, which specifies which robot will perform the action.
2. **List of Light Switches**: We define a list of all the light switches that need to be turned on.
3. **Thread Creation**: For each light switch, we determine which robot will handle it by cycling through the available robots using `i % len(robots)`. This ensures that if there are more lights than robots, we reuse the robots.
4. **Starting Threads**: Each thread is started immediately after creation.
5. **Joining Threads**: We wait for all threads to complete their execution using `join()`.

This approach allows us to efficiently allocate tasks among multiple robots while ensuring that each robot can independently handle its assigned task of turning on a specific light switch.