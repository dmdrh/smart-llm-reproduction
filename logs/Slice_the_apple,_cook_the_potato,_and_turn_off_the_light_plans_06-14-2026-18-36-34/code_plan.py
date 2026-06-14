To allocate the tasks of slicing the apple, cooking the potato, and turning off the light among the available robots, we can implement a solution that utilizes the skills of each robot effectively. Given that all robots have identical skills and sufficient mass capacity, we can assign each task to any robot. 

### Task Allocation
1. **SubTask 1**: Slice the Apple - Assigned to Robot 1
2. **SubTask 2**: Cook the Potato - Assigned to Robot 2
3. **SubTask 3**: Turn off the Light - Assigned to Robot 3

### Code Implementation
Here’s how we can implement this:

```python
import time
import threading

# Define functions for each subtask

def slice_apple(robot):
    # SubTask 1: Slice the Apple
    GoToObject(robot, 'Knife')
    PickupObject(robot, 'Knife')
    GoToObject(robot, 'Apple')
    SliceObject(robot, 'Apple')
    GoToObject(robot, 'CounterTop')
    PutObject(robot, 'Knife', 'CounterTop')

def cook_potato(robot):
    # SubTask 2: Cook the Potato
    GoToObject(robot, 'Potato')
    PickupObject(robot, 'Potato')
    GoToObject(robot, 'Pan')
    PutObject(robot, 'Potato', 'Pan')
    PickupObject(robot, 'Pan')
    GoToObject(robot, 'StoveBurner')
    PutObject(robot, 'Pan', 'StoveBurner')
    SwitchOn(robot, 'StoveKnob')
    
    # Wait for a while to let the Potato cook.
    time.sleep(5)
    
    SwitchOff(robot, 'StoveKnob')
    GoToObject(robot, 'Plate')
    PutObject(robot, 'Potato', 'Plate')

def turn_off_light(robot):
    # SubTask 3: Turn off the Light
    GoToObject(robot, 'LightSwitch')
    SwitchOff(robot, 'LightSwitch')

# Define robots with their skills and mass capacity
robots = [
    {'name': 'robot1', 
     'skills': ['GoToObject', 'OpenObject', 
                'CloseObject', 
                'BreakObject', 
                'SliceObject', 
                'SwitchOn', 
                'SwitchOff', 
                'PickupObject', 
                'PutObject'], 
     'mass': 100},
     
     {'name': 'robot2',
     'skills': ['GoToObject', 
                'OpenObject',
                "CloseObject", 
                "BreakObject", 
                "SliceObject", 
                "SwitchOn", 
                "SwitchOff", 
                "PickupObject", 
                "PutObject"],  
     "mass": 100},
     
     {'name': "robot3",
     "skills": ["GoToObject", 
                 "OpenObject",
                 "CloseObject",  
                 "BreakObject",  
                 "SliceObject",  
                 "SwitchOn",  
                 "SwitchOff",  
                 "Pickupobject",
                 "Putobject"],  
     "mass": 100}
]

# Create threads for each subtask using different robots
task1_thread = threading.Thread(target=slice_apple, args=(robots[0],))
task2_thread = threading.Thread(target=cook_potato, args=(robots[1],))
task3_thread = threading.Thread(target=turn_off_light,args=(robots[2],))

# Start executing SubTasks in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish before executing SubTask 3
task1_thread.join()
task2_thread.join()

# Execute SubTask 3 after both tasks are complete
task3_thread.start()
task3_thread.join()

# All tasks are done!
print("Tasks completed: Sliced apple, cooked potato and turned off light.")
```

### Explanation:
- **Slicing the Apple**: The `slice_apple` function is executed by `robot1`, which goes through all necessary steps to slice an apple.
- **Cooking the Potato**: The `cook_potato` function is executed by `robot2`, which handles all steps required to cook a potato.
- **Turning Off the Light**: The `turn_off_light` function is executed by `robot3`, which turns off the light switch after both previous tasks are completed.
- **Parallel Execution**: The first two tasks (slicing and cooking) are executed in parallel using threads. The third task (turning off the light) waits until both previous tasks are finished.

This approach ensures efficient use of resources while completing all tasks successfully.