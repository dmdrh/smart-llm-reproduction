To allocate the task of moving the dining table to the corner, we will analyze the required skills for each subtask and match them with the available robots. 

### GENERAL TASK DECOMPOSITION
1. **SubTask 1**: Go to the Dining Table. (Skills Required: GoToObject)
2. **SubTask 2**: Pickup the Dining Table. (Skills Required: PickupObject)
3. **SubTask 3**: Move to the corner. (Skills Required: GoToObject)
4. **SubTask 4**: Put the Dining Table in the corner. (Skills Required: PutObject)

### ROBOT CAPABILITIES
- All three robots have identical skills:
    - Skills Available: `['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject']`
- Mass capacity of each robot is `100`.

### OBJECT MASS
- The mass of the Dining Table is `85`.

### TASK ALLOCATION ANALYSIS
1. **SubTask 1** - Go to Dining Table:
   - Any robot can perform this since all have `GoToObject` skill.
   
2. **SubTask 2** - Pickup Dining Table:
   - Any robot can perform this since all have `PickupObject` skill.

3. **SubTask 3** - Move to Corner:
   - Any robot can perform this since all have `GoToObject` skill.

4. **SubTask 4** - Put Dining Table in Corner:
   - Any robot can perform this since all have `PutObject` skill.

### SEQUENTIAL OR PARALLEL EXECUTION
Since moving a large object like a dining table requires careful handling and cannot be done simultaneously by multiple robots, we will execute these subtasks sequentially.

###