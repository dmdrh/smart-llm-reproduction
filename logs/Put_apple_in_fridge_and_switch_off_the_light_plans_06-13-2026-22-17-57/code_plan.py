To accomplish the task of putting an apple in the fridge and switching off the light, we can break it down into two independent subtasks:

1. **Put the apple in the fridge** (Skills Required: GoToObject, PickupObject, OpenObject, PutObject, CloseObject).
2. **Switch off the light** (Skills Required: GoToObject, SwitchOff).

Since these two subtasks are independent, we can execute them in parallel. Below is the code that implements this task:

```python
import threading

def put_apple_in_fridge():
    # 0: SubTask 1: Put apple in the fridge
    # 1: Go to the Apple.
    GoToObject('Apple')
    # 2: Pick up the Apple.
    PickupObject('Apple')
    # 3: Go to the Fridge.
    GoToObject('Fridge')
    # 4: Open the Fridge.
    OpenObject('Fridge')
    # 5: Put Apple in the Fridge
    PutObject('Apple', 'Fridge')
    # 6: Close Fridge
    CloseObject('Fridge')

def switch_off_light():
    # 0: SubTask 2: Switch off the light
    # 1: Go to the LightSwitch.
    GoToObject('LightSwitch')
    # 2: Switch off the Light.
    SwitchOff('LightSwitch')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=put_apple_in_fridge)
task2_thread = threading.Thread(target=switch_off_light)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task put apple in fridge and switch off the light is done
```

### Explanation:
- **put_apple_in_fridge**: This function handles all steps required to pick up the apple and place it in the fridge.
- **switch_off_light**: This function handles all steps required to go to the light switch and turn it off.
- Both functions are executed in parallel using threads, allowing for efficient task completion. After starting both threads, we wait for both to finish before concluding that both tasks are done.

### Task Allocation Analysis

#### Subtask Analysis:
- **Subtask 1 (Put Apple in Fridge)**:
   - Required Skills:
     - `GoToObject`
     - `PickupObject`
     - `OpenObject`
     - `PutObject`
     - `CloseObject`
   - Mass of Objects Involved:
     - Apple (0.2 kg)
     - Fridge (mass not relevant)

- **Subtask 2 (Switch Off Light)**:
   - Required Skills:
     - `GoToObject`
     - `SwitchOff`
   - Mass of Objects Involved:
     - LightSwitch (mass not relevant)

#### Robot Capabilities:
We have three robots available with identical skills and mass capacity:

```python
robots = [
    {'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass': 100},
    {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'Break Object','Slice Object','SwitchOn','SwitchOff','Pickup Object','Put Object','Drop Hand Object','Throw Object','Push Object','Pull Object'],'mass':100},
    {'name':'robot3','skills':['GoTo Object','Open Object','Close Object','Break Object','Slice Object','SwitchOn','SwitchOff','Pickup Object','Put Object','Drop Hand Object','Throw Object','Push Object','Pull Object'],'mass':100}
]
```

### Task Allocation Decision:
Since all robots possess all necessary skills for both subtasks and have sufficient mass capacity, any robot can be assigned either subtask. 

For optimal efficiency, we can assign one robot to each subtask:

- Assign **Robot 1** to handle putting the apple in the fridge.
- Assign **Robot 2** or **Robot 3** to handle switching off the light.

This way, both tasks can be executed simultaneously without any delays or conflicts.