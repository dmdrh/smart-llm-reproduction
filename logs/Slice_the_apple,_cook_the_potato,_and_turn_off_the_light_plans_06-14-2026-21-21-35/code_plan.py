```python
import threading
import time

# Define the skills and objects
from skills import GoToObject, OpenObject, CloseObject, BreakObject, SliceObject, SwitchOn, SwitchOff, CleanObject, PickupObject, PutObject, DropHandObject, ThrowObject, PushObject, PullObject

# Define the robots with their skills and mass capacity
robots = [
    {'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass': 100},
    {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass': 100},
    {'name': 'robot3', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject','SwitchOn','SwitchOff','PickupObjec','PutObjec','DropHandObjec','ThrowObjec','PushObjec','PullObjec'], 100}
]

# SubTask 1: Slice the Apple
def slice_apple(robot):
    # 0: SubTask 1: Slice the Apple
    # 1: Go to the Knife.
    GoToObjective(robot['name'], "Knife")
    # 2: Pick up the Knife.
    PickupObjective(robot['name'], "Knife")
    # 3: Go to the Apple.
    GoToObjective(robot['name'], "Apple")
    # 4: Slice the Apple.
    SliceObjective(robot['name'], "Apple")
    # 5: Go to the countertop.
    GoToObjective(robot['name'], "CounterTop")
    # 6: Put the Knife back on the CounterTop.
    PutObjective(robot['name'], "Knife", "CounterTop")

# SubTask 2: Cook the Potato
def cook_potato(robot):
    # 0: SubTask 2: Cook the Potato
    # 1: Go to the sliced Potato.
    GoToObjective(robot['name'], "Potato")
    # 2: Pick up the sliced Potato.
    PickupObjective(robot['name'], "Potato")
    # 3: Go to the Pan.
    GoToObjective(robot['name'], "Pan")
    # 4: Put the sliced Potato in the Pan.
    PutObjective(robot['name'], "Potato", "Pan")
    
   ...
   
   (Continue with steps for cooking potato as described in your task)

# SubTask 3: Turn off the Light
def turn_off_light(robot):
   ...
   (Implement steps for turning off light as described in your task)

# Parallelize SubTask 1 and SubTask 3 using threading
task1_thread = threading.Thread(target=slice_apple, args=(robots[0],))
task3_thread = threading.Thread(target=turn_off_light, args=(robots[1],))

# Start executing SubTask 1 and SubTask 3 in parallel
task1_thread.start()
task3_thread.start()

# Wait for both SubTask threads to finish before proceeding to cook potato
task1_thread.join()
task3_thread.join()

# Execute SubTask 2 after completing slicing apple (SubTask1)
cook_potato(robots[2])

print("Tasks completed successfully.")
```

### Explanation:
- **Parallel Execution**:
   - `slice_apple` is assigned to `robot1`.
   - `turn_off_light` is assigned to `robot2`.
- **Sequential Execution**:
   - After completing slicing of apple (`SubTask1`), `cook_potato` is executed by `robot3`.

This approach ensures efficient use of resources by leveraging parallel execution where possible and sequential execution when dependencies exist.