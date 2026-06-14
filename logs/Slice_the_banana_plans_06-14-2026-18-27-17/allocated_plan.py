To allocate the tasks for slicing a banana, we need to analyze the subtasks, required skills, and the capabilities of the available robots. 

### Subtasks Breakdown
1. **SubTask 1**: Go to the Banana and pick it up.
   - Skills Required: `GoToObject`, `PickupObject`
2. **SubTask 2**: Get the Knife.
   - Skills Required: `GoToObject`, `PickupObject`
3. **SubTask 3**: Slice the Banana.
   - Skills Required: `SliceObject`
4. **SubTask 4**: Put the Knife back.
   - Skills Required: `PutObject`

### Robot Capabilities
All three robots have identical skills:
- Skills Available: 
  - `GoToObject`, 
  - `OpenObject`, 
  - `CloseObject`, 
  - `BreakObject`, 
  - `SliceObject`, 
  - `SwitchOn`, 
  - `SwitchOff`, 
  - `PickupObject`, 
  - `PutObject`,
  - `DropHandObject`,
  - `ThrowObject`,
  - `PushObject`,
  - `PullObject`
  
- Mass Capacity of each robot is **100 units**, which is more than sufficient for all objects involved in this task.

### Task Allocation Analysis
Since all robots have identical skills and mass capacity, we can allocate them based on availability:

1. **SubTask Allocation**:
   * SubTask1 (Go to Banana and pick it up) can be assigned to Robot1.
   * SubTask2 (Get Knife) can be assigned to Robot2.
   * SubTask3 (Slice Banana) can be assigned to Robot3 since it requires only one robot with slicing capability.
   * SubTask4 (Put Knife back) can be performed by any robot that finishes their task first; we will assign it back to Robot1 after completing Subtask1.

### Execution Order