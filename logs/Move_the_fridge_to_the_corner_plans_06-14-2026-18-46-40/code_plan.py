To allocate the tasks of moving the fridge to the corner, we need to analyze the subtasks and determine which robots can perform them based on their skills and mass capacity.

### Task Decomposition
1. **SubTask 1**: Go to the Fridge. (Skills Required: GoToObject)
2. **SubTask 2**: Pick up the Fridge. (Skills Required: PickupObject)
3. **SubTask 3**: Move to the corner. (Skills Required: GoToObject)
4. **SubTask 4**: Put down the Fridge. (Skills Required: PutObject)

### Robot Capabilities
- **Robot 1**
  - Skills: ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject']
  - Mass Capacity: 1.0

- **Robot 2**
  - Skills: ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject','Throw Object','Push Object','Pull Object']
  - Mass Capacity: 2.1

- **Robot 3**
   - Skills: ['GoTo Object','Open Object','Close Object','Break Object','Slice Object','Switch On','Switch Off','Pickup Object','Put Object','Drop Hand Object,'Throw object,'Push object,'Pull object']
   - Mass Capacity :0.9

### Analysis of Subtasks
- For **SubTask 1** (Go to the Fridge):
    - Any robot with `GoToobject` skill can perform this task.
    - All robots can perform this subtask.

- For **SubTask 2** (Pick up the Fridge):
    - The fridge's mass is likely greater than Robot 1's capacity (1.0) and Robot 3's capacity (0.9). 
    - Only Robot 2, with a mass capacity of 2.1, can pick up the fridge.

- For **SubTask 3** (Move to the corner):
    - Any robot with `GoToobject` skill can perform this task.
    - All robots can perform this subtask.

- For **SubTask 4** (Put down the Fridge):
    - Any robot with `Putobject` skill can perform this task.
    - All robots can perform this subtask.

### Task Allocation
Based on our analysis:
- Assign **SubTask 1** and **SubTask 3** to any robot, but we will choose Robot 1 for both since it has sufficient skills.
- Assign **SubTask 2** and **SubTask 4** to Robot 2 since it is the only robot capable of picking up and putting down the fridge.

### CODE Solution
```python
def move_fridge_to_corner(robot_list):
    # SubTask allocation
    # Robot list = [robot1, robot2]
    
    # SubTask 1: Go to the Fridge using robot1
    GoToObject(robot_list[0], 'Fridge')
    
    # SubTask 2: Pick up the Fridge using robot2
    PickupObject(robot_list[1], 'Fridge')
    
    # SubTask 3: Move to the corner using robot2
    GoToObject(robot_list[1], 'Corner')  
    
    # SubTask 4: Put down the Fridge using robot2
    PutObject(robot_list[1], 'Fridge', 'Corner')

# Execute task with allocated robots
move_fridge_to_corner([robots[0], robots[1]])

# Task move fridge to corner is done
```

### Explanation:
- The function `move_fridge_to_corner` takes a list of robots as input.
- It first directs Robot 1 to go to the fridge.
- Then, it has Robot 2 pick up the fridge due to its higher mass capacity.
- After that, Robot 2 moves to the corner where it places down the fridge.

This sequence ensures that all subtasks are completed efficiently while adhering to each robot's capabilities.