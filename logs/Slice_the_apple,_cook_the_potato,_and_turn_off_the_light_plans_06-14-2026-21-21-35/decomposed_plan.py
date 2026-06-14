# Task Description: Slice the apple, cook the potato, and turn off the light

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Slice the Apple. (Skills Required: GoToObject, PickupObject, SliceObject, PutObject)
# SubTask 2: Cook the Potato. (Skills Required: GoToObject, PickupObject, SliceObject, PutObject, SwitchOn, SwitchOff)
# SubTask 3: Turn off the Light. (Skills Required: GoToObject, SwitchOff)
# We can parallelize SubTask 1 and SubTask 3 because they don't depend on each other. SubTask 2 can be executed after SubTask 1.

# CODE

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
    # 5: Go to the countertop.
    GoToObject('CounterTop')
    # 6: Put the Knife back on the CounterTop.
    PutObject('Knife', 'CounterTop')

def cook_potato():
    # 0: SubTask 2: Cook the Potato
    # 1: Go to the sliced Potato.
    GoToObject('Potato')
    # 2: Pick up the sliced Potato.
    PickupObject('Potato')
    # 3: Go to the Pan.
    GoToObject('Pan')
    # 4: Put the sliced Potato in the Pan.
    PutObject('Potato', 'Pan')
    # 5: Pick up the pan with potato in it.
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
    # 11: Go to the Potato.
    GoToObject('Potato')
    # 12: Pick up the Potato.
    PickupObject('Potato')
    # 13: Go to the Plate.
    GoToObject('Plate')
    # 14: Put the cooked Potato on the Plate.
    PutObject('Potato', 'Plate')

def turn_off_light():
    # 0: SubTask 3: Turn off the Light
    # 1: Go to the LightSwitch.
    GoToObject('LightSwitch')
    # 2: Switch off the Light.
    SwitchOff('LightSwitch')

# Parallelize SubTask 1 and SubTask 3
task1_thread = threading.Thread(target=slice_apple)
task3_thread = threading.Thread(target=turn_off_light)

# Start executing SubTask 1 and SubTask 3 in parallel
task1_thread.start()
task3_thread.start()

# Wait for both SubTask 1 and SubTask 3 to finish
task1_thread.join()
task3_thread.join()

# Execute SubTask 2 after SubTask 1 is complete
cook_potato()

# Task Slice the apple, cook the potato, and turn off the light is done