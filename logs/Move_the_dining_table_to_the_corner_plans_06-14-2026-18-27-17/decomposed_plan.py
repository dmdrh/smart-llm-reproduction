To move the dining table to the corner, we can break down the task into a series of subtasks. Since moving a large object like a dining table typically requires careful handling, we will not parallelize the subtasks. Instead, we will execute them sequentially.

### GENERAL TASK DECOMPOSITION
- **SubTask 1**: Go to the Dining Table. (Skills Required: GoToObject)
- **SubTask 2**: Pickup the Dining Table. (Skills Required: PickupObject)
- **SubTask 3**: Move to the corner. (Skills Required: GoToObject)
- **SubTask 4**: Put the Dining Table in the corner. (Skills Required: PutObject)

### CODE
```python
def move_dining_table_to_corner():
    # 0: SubTask 1: Go to the Dining Table
    GoToObject('DiningTable')
    
    # 1: SubTask 2: Pickup the Dining Table
    PickupObject('DiningTable')
    
    # 2: SubTask 3: Move to the corner
    GoToObject('Corner')  # Assuming 'Corner' is a defined location in the environment
    
    # 3: SubTask 4: Put the Dining Table in the corner
    PutObject('DiningTable', 'Corner')

# Execute the task to move the dining table to the corner
move_dining_table_to_corner()

# Task move the dining table to the corner is done
```

### Explanation
1. **GoToObject('DiningTable')**: The robot navigates to the location of the dining table.
2. **PickupObject('DiningTable')**: The robot picks up the dining table.
3. **GoToObject('Corner')**: The robot moves to the designated corner location.
4. **PutObject('DiningTable', 'Corner')**: The robot places the dining table in the corner.

This sequence ensures that the dining table is moved safely and efficiently to the desired location.