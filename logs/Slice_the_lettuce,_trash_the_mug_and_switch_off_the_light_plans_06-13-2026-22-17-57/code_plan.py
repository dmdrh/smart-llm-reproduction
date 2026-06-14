To accomplish the tasks of slicing the lettuce, trashing the mug, and switching off the light, we can break down these tasks into subtasks and analyze them based on robot skills and mass capacity.

### Task Decomposition
- **SubTask 1**: Slice the Lettuce. (Skills Required: GoToObject, PickupObject, SliceObject, PutObject)
- **SubTask 2**: Trash the Mug. (Skills Required: GoToObject, PickupObject, PutObject)
- **SubTask 3**: Switch off the Light. (Skills Required: GoToObject, SwitchOff)

### Robot Analysis
We have three robots with their respective skills and mass capacities:
1. **Robot 1**
   - Skills: ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject']
   - Mass Capacity: 0.4

2. **Robot 2**
   - Skills: ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff','Pickup Object','Put Object','Drop Hand Object','Throw Object','Push Object','Pull Object']
   - Mass Capacity: 2.1

3. **Robot 3**
   - Skills: ['GoTo Object','Open Object','Close Object','Break Object','Slice Object','Switch On','Switch Off',
'Pickup Object,'Put object,'Drop Hand object,'Throw object,'Push object,'Pull object']
   - Mass Capacity: 1.0

### Subtask Analysis
#### SubTask 1: Slice the Lettuce
- Required Skills:
    - GoToObject
    - PickupObject
    - SliceObject
    - PutObject 
- The mass of Lettuce is approximately `0.47 kg`, which is within the capacity of Robot 2 (2.1 kg) and Robot 3 (1.0 kg). However, only Robot 2 has all required skills.

#### SubTask 2: Trash the Mug
- Required Skills:
    - GoToObject
    - PickupObject
    - PutObject 
- The mass of the Mug is approximately `1 kg`, which can be handled by Robot 2 (2.1 kg) and Robot 3 (1.0 kg). Both robots have all required skills.

#### SubTask 3: Switch off the Light
- Required Skills:
    - GoToobject
    - SwitchOff 
- This task can be performed by any robot since all have these skills.

### Task Allocation Strategy
Based on our analysis:
- **SubTask 1** (Slice Lettuce) will be assigned to **Robot 2**.
- **SubTask 2** (Trash Mug) can be assigned to either **Robot 2** or **Robot 3**, but we will assign it to **Robot 3** for load balancing.
- **SubTask 3** (Switch off Light) can be assigned to any robot; we will assign it to **Robot 1**.

### Implementation Code

```python
import threading

def slice_lettuce():
    # SubTask for slicing lettuce using Robot 2.
    GoToObject('Knife')
    PickupObject('Knife')
    GoToObject('Lettuce')
    SliceObject('Lettuce')
    GoToObject('CounterTop')
    PutObject('Knife', 'CounterTop')

def trash_mug():
    # SubTask for trashing mug using Robot 3.
    GoToObject('Mug')
    PickupObject('Mug')
    GoToObject('GarbageCan')
    PutObject('Mug', 'GarbageCan')

def switch_off_light():
    # SubTask for switching off light using Robot 1.
    GoToObject('LightSwitch')
    SwitchOff('LightSwitch')

# Create threads for each subtask to run in parallel.
task1_thread = threading.Thread(target=slice_lettuce)
task2_thread = threading.Thread(target=trash_mug)
task3_thread = threading.Thread(target=switch_off_light)

# Start executing all subtasks in parallel.
task1_thread.start()
task2_thread.start()
task3_thread.start()

# Wait for all subtasks to finish.
task1_thread.join()
task2_thread.join()
task3_thread.join()

# Task completion message.
print("Tasks completed: Sliced lettuce, trashed mug, switched off light.")
```

### Explanation of Code:
- Each subtask is defined as a function that utilizes specific robot skills to complete its task.
- Threads are created for each subtask allowing them to run concurrently.
- After starting all threads, we wait for their completion before printing a final message indicating that all tasks are done.

This approach ensures efficient use of resources while adhering to skill requirements and mass capacities of each robot involved in completing the tasks.