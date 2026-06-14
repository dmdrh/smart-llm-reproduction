Here's how we can implement the task allocation for slicing a banana, taking into account the subtasks and the capabilities of the robots:

### Task Description: Slice the Banana

#### GENERAL TASK DECOMPOSITION
- **SubTask 1**: Go to the Banana and pick it up. (Skills Required: GoToObject, PickupObject)
- **SubTask 2**: Get the Knife. (Skills Required: GoToObject, PickupObject)
- **SubTask 3**: Slice the Banana. (Skills Required: SliceObject)
- **SubTask 4**: Put the Knife back. (Skills Required: PutObject)

### CODE

```python
def slice_banana(robot_list):
    # SubTask 1: Go to the Banana and pick it up using robot1
    GoToObject(robot_list[0], 'Banana')
    PickupObject(robot_list[0], 'Banana')
    
    # SubTask 2: Get the Knife using robot2
    GoToObject(robot_list[1], 'Knife')
    PickupObject(robot_list[1], 'Knife')
    
    # SubTask 3: Slice the Banana using robot3
    SliceObject(robot_list[2], 'Banana')
    
    # SubTask 4: Put the Knife back using robot1 (after completing Subtask 1)
    GoToObject(robot_list[0], 'CounterTop')  # Assuming we put the knife back on the counter
    PutObject(robot_list[0], 'Knife', 'CounterTop')

# Define robots with their skills and mass capacity
robots = [
    {'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 
                                   'SliceObject', 'SwitchOn', 'SwitchOff', 
                                   'PickupObject', 'PutObject', 
                                   'DropHandObject', 'ThrowObject', 
                                   'PushObject', 'PullObject'], 
     'mass': 100},
     
    {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 
                                   'BreakObject', 'SliceObject', 
                                   'SwitchOn', 'SwitchOff',
                                   'PickupObject', 'PutObject',
                                   'DropHandObject', 'ThrowObject',
                                   'PushObject', 'PullObject'], 
     'mass': 100},
     
    {'name': 'robot3', 'skills': ['GoToObject', 'OpenObject', 
                                   'CloseObject','BreakObject',
                                   'SliceObject','SwitchOn',
                                   "SwitchOff", "Pickupobject",
                                   "Putobject", "DropHandobject",
                                   "Throwobject", "Pushobject",
                                   "Pullobject"], 
     "mass": 100}
]

# Execute the task to slice a banana with allocated robots
slice_banana(robots)

# Task slice the banana is done
```

### Explanation:
1. **SubTask Allocation**:
   - Robot1 is assigned to go to and pick up the banana.
   - Robot2 is assigned to go get the knife.
   - Robot3 is responsible for slicing the banana.
   - After Robot1 completes picking up the banana, it will return to put back the knife.

2. **Execution Order**:
   - Each robot performs its assigned subtask in sequence, ensuring that all necessary actions are completed efficiently.

This code effectively completes all subtasks required for slicing a banana while utilizing multiple robots based on their skills and capabilities.