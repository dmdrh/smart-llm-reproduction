To allocate the tasks of moving the fridge to the corner, we first need to analyze the subtasks and determine which robots can perform them based on their skills and mass capacity.

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

- For **SubTask 2** (Pick up the Fr