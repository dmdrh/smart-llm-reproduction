To allocate the tasks of slicing the apple, cooking the potato, and turning off the light among the available robots, we need to analyze each subtask's requirements in terms of skills and mass capacity. 

### General Task Decomposition
1. **SubTask 1**: Slice the Apple.
   - **Skills Required**: GoToObject, PickupObject, SliceObject, PutObject
   - **Mass of Objects**: Knife (0.18 kg), Apple (0.2 kg)
   
2. **SubTask 2**: Cook the Potato.
   - **Skills Required**: GoToObject, PickupObject, OpenObject, PutObject, CloseObject, SwitchOn
   - **Mass of Objects**: Potato (0.18 kg), Pan (0.67 kg), StoveBurner (mass negligible for this task)

3. **SubTask 3**: Turn off the Light.
   - **Skills Required**: GoToObject, SwitchOff
   - **Mass of Objects**: LightSwitch (mass negligible)

### Robot Capabilities
All three robots have identical skills:
- Skills Available: ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject']
- Mass Capacity for each robot is 100 kg.

### Task Allocation Analysis

#### SubTask 1: Slice the Apple
- All robots can perform this task since they possess all required skills.
- The total mass involved is 0.38 kg which is well within any robot's capacity.

#### SubTask 2: Cook the Potato
- All robots can perform this task as they have all required skills.
- The total mass involved is approximately 0.85 kg which is also within any robot's capacity.

#### SubTask 3: Turn off the