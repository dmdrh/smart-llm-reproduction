To throw the spatula in the trash, we can break down the task into a series of steps that involve moving to the spatula, picking it up, going to the trash can, and then throwing it away. Here's how we can implement this task:

### Task Description: Throw the Spatula in the Trash

### GENERAL TASK DECOMPOSITION
- **SubTask 1**: Throw the Spatula in the Trash. (Skills Required: GoToObject, PickupObject, GoToObject, ThrowObject)

### CODE
```python
def throw_spatula_in_trash():
    # 0: SubTask 1: Throw the Spatula in the Trash
    # 1: Go to the Spatula.
    GoToObject('Spatula')
    # 2: Pick up the Spatula.
    PickupObject('Spatula')
    # 3: Go to the Trash Can.
    GoToObject('GarbageCan')
    # 4: Throw the Spatula in the Trash.
    ThrowObject('Spatula')

# Execute SubTask 1
throw_spatula_in_trash()

# Task throw the spatula in the trash is done
```

### Explanation of the Code:
1. **GoToObject('Spatula')**: The robot moves to the location of the spatula.
2. **PickupObject('Spatula')**: The robot picks up the spatula.
3. **GoToObject('GarbageCan')**: The robot moves to the trash can (garbage can).
4. **ThrowObject('Spatula')**: The robot throws the spatula into the trash can.

This sequence of actions completes the task of throwing the spatula in the trash.