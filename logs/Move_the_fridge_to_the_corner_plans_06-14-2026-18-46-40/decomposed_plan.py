To move the fridge to the corner, we need to decompose the task into subtasks that involve navigating to the fridge, picking it up, moving it to the desired location, and placing it down. Since moving the fridge is a single task that requires sequential execution, we will not parallelize any subtasks.

### Task Decomposition
- **SubTask 1**: Go to the Fridge. (Skills Required: GoToObject)
- **SubTask 2**: Pick up the Fridge. (Skills Required: PickupObject)
- **SubTask 3**: Move to the corner. (Skills Required: GoToObject)
- **SubTask 4**: Put down the Fridge. (Skills Required: PutObject)

### CODE
```python
def move_fridge_to_corner():
    # 0: SubTask 1: Go to the Fridge
    GoToObject('Fridge')
    
    # 1: SubTask 2: Pick up the Fridge
    PickupObject('Fridge')
    
    # 2: SubTask 3: Move to the corner
    GoToObject('Corner')  # Assuming 'Corner' is the designated location
    
    # 3: SubTask 4: Put down the Fridge
    PutObject('Fridge', 'Corner')

# Execute the task to move the fridge to the corner
move_fridge_to_corner()

# Task move the fridge to the corner is done
```

### Explanation
1. **GoToObject('Fridge')**: The robot navigates to the fridge.
2. **PickupObject('Fridge')**: The robot picks up the fridge.
3. **GoToObject('Corner')**: The robot moves to the corner where the fridge is to be placed.
4. **PutObject('Fridge', 'Corner')**: The robot places the fridge down in the corner.

This sequence ensures that the fridge is moved safely and efficiently to the desired location.