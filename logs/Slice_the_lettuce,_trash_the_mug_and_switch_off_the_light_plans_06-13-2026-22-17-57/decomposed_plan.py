To accomplish the task of slicing the lettuce, trashing the mug, and switching off the light, we can break it down into three subtasks. These subtasks can be executed in parallel since they are independent of each other.

### Task Decomposition
- **SubTask 1**: Slice the Lettuce. (Skills Required: GoToObject, PickupObject, SliceObject, PutObject)
- **SubTask 2**: Trash the Mug. (Skills Required: GoToObject, PickupObject, PutObject)
- **SubTask 3**: Switch off the Light. (Skills Required: GoToObject, SwitchOff)

### Implementation
Here’s how we can implement this in code:

```python
def slice_lettuce():
    # 0: SubTask 1: Slice the Lettuce
    # 1: Go to the Knife.
    GoToObject('Knife')
    # 2: Pick up the Knife.
    PickupObject('Knife')
    # 3: Go to the Lettuce.
    GoToObject('Lettuce')
    # 4: Slice the Lettuce.
    SliceObject('Lettuce')
    # 5: Go to the CounterTop.
    GoToObject('CounterTop')
    # 6: Put the Knife back on the CounterTop.
    PutObject('Knife', 'CounterTop')

def trash_mug():
    # 0: SubTask 2: Trash the Mug
    # 1: Go to the Mug.
    GoToObject('Mug')
    # 2: Pick up the Mug.
    PickupObject('Mug')
    # 3: Go to the GarbageCan.
    GoToObject('GarbageCan')
    # 4: Put the Mug in the GarbageCan.
    PutObject('Mug', 'GarbageCan')

def switch_off_light():
    # 0: SubTask 3: Switch off the Light
    # 1: Go to the LightSwitch.
    GoToObject('LightSwitch')
    # 2: Switch off the Light.
    SwitchOff('LightSwitch')

# Parallelize SubTask 1, SubTask 2, and SubTask 3
task1_thread = threading.Thread(target=slice_lettuce)
task2_thread = threading.Thread(target=trash_mug)
task3_thread = threading.Thread(target=switch_off_light)

# Start executing all subtasks in parallel
task1_thread.start()
task2_thread.start()
task3_thread.start()

# Wait for all subtasks to finish
task1_thread.join()
task2_thread.join()
task3_thread.join()

# Task: Slice the lettuce, trash the mug, and switch off the light is done
```

### Explanation
1. **Slicing the Lettuce**: The robot goes to the knife, picks it up, goes to the lettuce, slices it, and then puts the knife back on the countertop.
2. **Trashing the Mug**: The robot goes to the mug, picks it up, goes to the garbage can, and puts the mug inside.
3. **Switching Off the Light**: The robot goes to the light switch and switches it off.

All three tasks are executed in parallel, making the process efficient. After all threads complete their execution, the task is considered done.