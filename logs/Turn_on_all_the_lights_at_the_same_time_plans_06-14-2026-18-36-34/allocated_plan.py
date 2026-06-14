To allocate the task of turning on all the lights using the available robots, we need to analyze the subtasks, required skills, and robot capabilities.

### Task Description: Turn on all the lights at the same time

### GENERAL TASK DECOMPOSITION
- **SubTask 1**: Turn on each light switch. (Skills Required: GoToObject, SwitchOn)

### Available Robots
- **Robot 1**: Skills - ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], Mass - 100
- **Robot 2**: Skills - ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject','ThrowObject','PushObject','PullObject'], Mass - 100
- **Robot 3**: Skills - ['GoToObject','Open Object','Close Object','Break Object','Slice Object','Switch On','Switch Off','Pickup Object','Put Object','Drop Hand Object','Throw Object','Push Object,'Pull Object'], Mass - 100

### Analysis of Subtasks and Robot Capabilities
1. Each light switch requires a robot to go to it and turn it on.
2. All robots have the necessary skills (`GoTo` and `SwitchOn`) to perform this task.
3. The mass capacity of each robot is sufficient for handling any light switch since they are not heavy objects.

### Parallel Execution Feasibility
Since turning on each light switch is an independent action that does not depend on other actions being completed first, we can execute these subtasks in parallel.

### Robot Allocation Strategy
Given that there are three robots available and assuming there are multiple light switches (let's say