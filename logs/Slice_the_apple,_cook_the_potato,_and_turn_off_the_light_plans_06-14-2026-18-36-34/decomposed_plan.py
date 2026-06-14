To accomplish the task of slicing the apple, cooking the potato, and turning off the light, we can break it down into independent subtasks. The slicing of the apple and cooking of the potato can be done in parallel, while turning off the light can be done after these two tasks are completed.

### General Task Decomposition
- **SubTask 1**: Slice the Apple. (Skills Required: GoToObject, PickupObject, SliceObject, PutObject)
- **SubTask 2**: Cook the Potato. (Skills Required: GoToObject, PickupObject, OpenObject, PutObject, CloseObject, SwitchOn, SwitchOff)
- **SubTask 3**: Turn off the Light. (Skills Required: GoToObject, SwitchOff)

### Code Implementation
Here’s how we can implement this:

```python
def slice_apple():
    # 0: SubTask 1: Slice the Apple
    # 1: Go to the Knife.
    GoToObject('Knife')
    # 2: Pick up the Knife.
    PickupObject('Knife')
    # 3: Go to the Apple.
    GoToObject('Apple')
    # 4: Slice the Apple.
    SliceObject('Apple')
    # 5: Go to the CounterTop.
    GoToObject('CounterTop')
    # 6: Put the Knife back on the CounterTop.
    PutObject('Knife', 'CounterTop')

def cook_potato():
    # 0: SubTask 2: Cook the Potato
    # 1: Go to the Potato.
    GoToObject('Potato')
    # 2: Pick up the Potato.
    PickupObject('Potato')
    # 3: Go to the Pan.
    GoToObject('Pan')
    # 4: Put the Potato in the Pan.
    PutObject('Potato', 'Pan')
    # 5: Pick up the Pan with Potato in it.
    PickupObject('Pan')
    # 6: Go to the StoveBurner.
    GoToObject('StoveBurner')
    # 7: Put the Pan on the stove burner.
    PutObject('Pan', 'StoveBurner')
    # 8: Switch on the StoveKnob.
    SwitchOn('StoveKnob')
    # 9: Wait for a while to let the Potato cook.
    time.sleep(5)
    # 10: Switch off the StoveKnob.
    SwitchOff('StoveKnob')
    # 11: Go to the Plate.
    GoToObject('Plate')
    # 12: Put the cooked Potato on the Plate.
    PutObject('Potato', 'Plate')

def turn_off_light():
    # 0: SubTask 3: Turn off the Light
    # 1: Go to the LightSwitch.
    GoToObject('LightSwitch')
    # 2: Switch off the Light.
    SwitchOff('LightSwitch')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=slice_apple)
task2_thread = threading.Thread(target=cook_potato)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Execute SubTask 3 after SubTask 1 and SubTask 2 are complete
turn_off_light()

# Task slice the apple, cook the potato, and turn off the light is done
```

### Explanation
1. **Slicing the Apple**: The `slice_apple` function handles the process of slicing the apple using a knife.
2. **Cooking the Potato**: The `cook_potato` function manages the cooking of the potato in a pan on the stove.
3. **Turning Off the Light**: The `turn_off_light` function switches off the light after the first two tasks are completed.
4. **Parallel Execution**: The first two tasks are executed in parallel using threads, and the light is turned off only after both tasks are completed.

This approach ensures that the tasks are performed efficiently and in a timely manner.