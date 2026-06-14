Here's the complete code solution for the task allocation of cleaning the kitchen, including the assignment of robots to each subtask based on their skills:

```python
import threading

# Define cleaning functions for each subtask
def clean_countertop(robot):
    # 0: SubTask 1: Clean the Countertop
    GoToObject(robot, 'CounterTop')
    PickupObject(robot, 'DishSponge')
    CleanObject('CounterTop')
    PutObject('DishSponge', 'CounterTop')

def clean_dining_table(robot):
    # 0: SubTask 2: Clean the Dining Table
    GoToObject(robot, 'DiningTable')
    PickupObject(robot, 'DishSponge')
    CleanObject('DiningTable')
    PutObject('DishSponge', 'DiningTable')

def clean_sink(robot):
    # 0: SubTask 3: Clean the Sink
    GoToObject(robot, 'Sink')
    PickupObject(robot, 'DishSponge')
    CleanObject('Sink')
    PutObject('DishSponge', 'Sink')

def clean_floor(robot):
    # 0: SubTask 4: Clean the Floor
    GoToObject(robot, 'Floor')
    PickupObject(robot, 'DishSponge')
    CleanObject('Floor')
    PutObject('DishSponge', 'Floor')

def clean_fridge(robot):
    # 0: SubTask 5: Clean the Fridge
    GoToObject(robot, 'Fridge')
    OpenObject('Fridge')
    CleanObject('Fridge')
    CloseObject('Fridge')

# Define robots with their skills and mass capacity
robots = [
    {'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 
                                   'BreakObject', 'SliceObject', 
                                   'SwitchOn', 'SwitchOff', 
                                   'PickupObject', 'PutObject',
                                   'DropHandObject', 
                                   'ThrowObject', 
                                   'PushObject', 
                                   'PullObject'], 
     'mass': 100},
    
    {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 
                                   'CloseObject','Break Object',
                                   'Slice Object','Switch On',
                                   'Switch Off','Pickup Object',
                                   'Put Object','Drop Hand Object',
                                   'Throw Object','Push Object',
                                   'Pull Object'], 
     'mass': 100},
    
   {'name': "robot3", "skills": ['GoTo Object','Open Object',
                                  "Close Object","Break Object",
                                  "Slice Object","Switch On",
                                  "Switch Off","Pickup Object",
                                  "Put Object","Drop Hand Object",
                                  "Throw Object","Push Object",
                                  "Pull Object"],
     "mass":100}
]

# Create threads for parallel execution of cleaning tasks
task1_thread = threading.Thread(target=clean_countertop, args=(robots[0]['name'],))
task2_thread = threading.Thread(target=clean_dining_table, args=(robots[1]['name'],))
task3_thread = threading.Thread(target=clean_sink, args=(robots[2]['name'],))
task4_thread = threading.Thread(target=clean_floor, args=(robots[0]['name'],)) # Reusing robot1

# Start executing SubTasks in parallel
task1_thread.start()
task2_thread.start()
task3_thread.start()
task4_thread.start()

# Wait for all cleaning tasks to finish
task1_thread.join()
task2_thread.join()
task3_thread.join()
task4_thread.join()

# Execute SubTask 5 after other tasks are complete (sequentially)
clean_fridge(robots[1]['name']) # Assigning robot2 to clean fridge

# Task Clean up the kitchen is done
print("Kitchen cleaning is complete.")
```

### Explanation:
- **Subtasks**: Each cleaning function corresponds to a specific area or object in the kitchen that needs to be cleaned.
- **Robot Assignment**:
   - `robot1` is assigned to clean the countertop and floor.
   - `robot2` is assigned to clean the dining table and fridge.
   - `robot3` is assigned to clean the sink.
- **Parallel Execution**: The first four subtasks are executed in parallel using threads since they can be performed independently.
- **Sequential Execution**: The fridge cleaning task is executed after all other tasks are completed.

This approach ensures efficient use of resources while maintaining clarity in task allocation.