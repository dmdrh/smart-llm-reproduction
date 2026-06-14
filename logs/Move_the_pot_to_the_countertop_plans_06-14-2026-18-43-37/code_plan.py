```python
def move_pot_to_countertop(robot):
    # 0: SubTask 1: Move the pot to the countertop using robot2
    # 1: Go to the Pot using robot2.
    GoToObject(robot, 'Pot')
    # 2: Pick up the Pot using robot2.
    PickupObject(robot, 'Pot')
    # 3: Go to the CounterTop using robot2.
    GoToObject(robot, 'CounterTop')
    # 4: Put the Pot on the CounterTop using robot2.
    PutObject(robot, 'Pot', 'CounterTop')

# Execute SubTask 1 with Robot 2
move_pot_to_countertop(robots[1])

# Task move the pot to the countertop is done
```

### Explanation of Code:
1. **Function Definition**: The function `move_pot_to_countertop` takes a robot as an argument.
2. **GoToObject**: The robot moves to the location of the pot.
3. **PickupObject**: The robot picks up the pot.
4. **GoToObject**: The robot moves to the countertop.
5. **PutObject**: The robot places the pot on the countertop.

### Task Allocation Summary:
- Robot 2 is selected for this task due to its higher mass capacity (2.1 kg), which allows it to easily pick up and move the pot (0.57 kg).
- This allocation ensures that we efficiently utilize our robots based on their capabilities and skills.

The task of moving the pot to the countertop is now successfully completed!