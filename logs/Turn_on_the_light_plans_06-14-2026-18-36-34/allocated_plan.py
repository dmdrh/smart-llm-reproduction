To allocate the task of turning on the light, we first need to analyze the subtasks, required skills, and available robots.

### Task Description: Turn on the light

#### GENERAL TASK DECOMPOSITION
- **SubTask 1**: Turn on the light. 
  - **Skills Required**: GoToObject, SwitchOn
  - **Mass of Object (LightSwitch)**: 0.0 (assumed negligible for this task)

### ROBOT ANALYSIS
We have three robots available:
1. **Robot 1**: Skills - ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], Mass Capacity - 100
2. **Robot 2**: Skills - ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject','ThrowObject','PushObject','PullObject'], Mass Capacity - 100
3. **Robot 3**: Skills - ['GoToObject','Open Object','Close Object','Break Object','Slice Object','Switch On','Switch Off','Pickup Object','Put Object','Drop Hand Object','Throw Object','Push Object,'Pull Object'], Mass Capacity - 100

### TASK ALLOCATION BASED ON SKILLS AND MASS CAPACITY
- For SubTask 1 (Turn on the light), any robot can perform it since all robots possess both required skills (`GoToobject` and `SwitchOn`) and have sufficient mass capacity to handle the negligible mass of the Light Switch.

### DECISION ON SEQUENTIAL OR PARALLEL EXECUTION
- Since there is only one subtask that does not depend on any other tasks, it can be executed immediately without waiting