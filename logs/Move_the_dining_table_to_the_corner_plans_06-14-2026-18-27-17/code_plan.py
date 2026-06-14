```python
def move_dining_table_to_corner(robot):
    # 0: SubTask 1: Go to the Dining Table
    GoToObject(robot, 'DiningTable')
    
    # 1: SubTask 2: Pickup the Dining Table
    PickupObject(robot, 'DiningTable')
    
    # 2: SubTask 3: Move to the corner
    GoToObject(robot, 'Corner')  # Assuming 'Corner' is a defined location in the environment
    
    # 3: SubTask 4: Put the Dining Table in the corner
    PutObject(robot, 'DiningTable', 'Corner')

# TASK ALLOCATION
robots = [
    {'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 
                                   'BreakObject', 'SliceObject', 'SwitchOn', 
                                   'SwitchOff', 'PickupObject', 'PutObject', 
                                   'DropHandObject', 'ThrowObject', 
                                   'PushObject', 'PullObject'], 
     'mass': 100},
     
    {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject',
                                   'BreakObject', 'SliceObject', 
                                   'SwitchOn', 'SwitchOff',
                                   'PickupObject', 'PutObject',
                                   'DropHandObject', 
                                   'ThrowObject','PushObject','PullObject'], 
     'mass': 100},
     
    {'name': 'robot3', 
     skills': ['GoToObject','OpenObject','CloseObject',
               ‘Break Object’, ‘Slice Object’, ‘Switch On’,
               ‘Switch Off’, ‘Pickup Object’, ‘Put Object’,
               ‘Drop Hand Object’, ‘Throw Object’,
               ‘Push Object’,‘Pull Object’], 
     mass’: 100}
]

# Since all robots have the required skills and sufficient mass capacity,
# we can assign any robot to perform the task. Let's assign robot1.

move_dining_table_to_corner('robot1')

# Task move the dining table to the corner is done.
```

### Explanation:
- The function `move_dining_table_to_corner` takes a robot as an argument and executes each subtask sequentially.
- Each subtask is performed by calling appropriate functions with the specified robot.
- The task allocation analysis shows that any of the robots can perform all subtasks due to their identical skill sets and sufficient mass capacity. Thus, we chose `robot1` for this task. 

This approach ensures that the dining table is moved safely and efficiently to its new location in a structured manner.