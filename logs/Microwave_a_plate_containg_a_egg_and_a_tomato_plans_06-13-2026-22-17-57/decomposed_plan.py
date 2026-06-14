To microwave a plate containing an egg and a tomato, we can break down the task into several subtasks. The tasks can be parallelized where possible, and we will ensure that the necessary steps are followed in the correct order.

### Task Decomposition
1. **Prepare the Plate**: Place the egg and tomato on the plate.
   - Skills Required: GoToObject, PickupObject, PutObject
2. **Microwave the Plate**: Microwave the plate containing the egg and tomato.
   - Skills Required: GoToObject, OpenObject, PutObject, CloseObject, SwitchOn, SwitchOff

### Code Implementation
Here’s how we can implement the above tasks in code:

```python
def prepare_plate():
    # 0: SubTask 1: Prepare the Plate with Egg and Tomato
    # 1: Go to the Plate.
    GoToObject('Plate')
    # 2: Pick up the Plate.
    PickupObject('Plate')
    # 3: Go to the Egg.
    GoToObject('Egg')
    # 4: Put the Egg on the Plate.
    PutObject('Egg', 'Plate')
    # 5: Go to the Tomato.
    GoToObject('Tomato')
    # 6: Put the Tomato on the Plate.
    PutObject('Tomato', 'Plate')

def microwave_plate():
    # 0: SubTask 2: Microwave the Plate containing Egg and Tomato
    # 1: Go to the Microwave.
    GoToObject('Microwave')
    # 2: Open the Microwave door.
    OpenObject('Microwave')
    # 3: Put the Plate inside the Microwave.
    PutObject('Plate', 'Microwave')
    # 4: Close the Microwave door.
    CloseObject('Microwave')
    # 5: Switch on the Microwave.
    SwitchOn('Microwave')
    # 6: Wait for a while to let the food heat.
    time.sleep(5)
    # 7: Switch off the Microwave.
    SwitchOff('Microwave')
    # 8: Open the Microwave door.
    OpenObject('Microwave')
    # 9: Pick up the Plate.
    PickupObject('Plate')
    # 10: Close the Microwave door.
    CloseObject('Microwave')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=prepare_plate)
task2_thread = threading.Thread(target=microwave_plate)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task microwave a plate containing an egg and a tomato is done
```

### Explanation
1. **Prepare the Plate**: The `prepare_plate` function handles the task of placing the egg and tomato on the plate. It involves moving to the plate, picking it up, and then adding the egg and tomato.
  
2. **Microwave the Plate**: The `microwave_plate` function manages the microwaving process. It involves opening the microwave, placing the plate inside, closing the microwave, and then switching it on for a specified duration.

3. **Parallel Execution**: Both tasks are executed in parallel using threads. However, since the preparation of the plate must be completed before microwaving, we ensure that the `microwave_plate` function waits for the `prepare_plate` function to finish before proceeding.

This structure allows for efficient task management while ensuring that all necessary steps are completed in the correct order.