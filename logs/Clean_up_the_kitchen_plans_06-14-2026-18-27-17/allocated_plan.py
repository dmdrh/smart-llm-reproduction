To allocate the cleaning tasks to the available robots, we need to analyze the skills required for each subtask and ensure that the robots assigned have the necessary skills. Additionally, we will check if any subtasks can be performed in parallel or if they must be done sequentially.

### Subtasks and Requirements
1. **SubTask 1:** Clean the Countertop.
   - Skills Required: GoToObject, PickupObject, CleanObject, PutObject
2. **SubTask 2:** Clean the Dining Table.
   - Skills Required: GoToObject, PickupObject, CleanObject, PutObject
3. **SubTask 3:** Clean the Sink.
   - Skills Required: GoToObject, PickupObject, CleanObject, PutObject
4. **SubTask 4:** Clean the Floor.
   - Skills Required: GoToObject, PickupObject, CleanObject, PutObject
5. **SubTask 5:** Clean the Fridge.
   - Skills Required: GoToObject, OpenObject, CleanObject, CloseObject

### Robot Capabilities
All three robots (robot1, robot2 and robot3) have identical skills:
- Skills: ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHand Object', 'Throw Object', 'Push Object', 'Pull Object']
- Mass Capacity: 100

### Task Allocation Analysis

#### Parallel Execution of SubTasks 1 to 4:
Since all four subtasks (cleaning countertop, dining table, sink and floor) require similar skills and can be performed independently of each other:

- **Robot Assignment**:
    - Assign `robot1` to clean Countertop (SubTask 1).
    - Assign `robot2` to clean Dining Table (SubTask 2).
    - Assign `robot3` to clean Sink (SubTask