Here's how you can implement the task of turning on the light, including the task allocation based on the available robots:

```python
# Task Description: Turn on the light

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Turn on the light. (Skills Required: GoToObject, SwitchOn)

# CODE
def turn_on_light(robot):
    # 0: SubTask 1: Turn on the light
    # 1: Go to the LightSwitch using the selected robot.
    GoToObject(robot, 'LightSwitch')
    # 2: Switch on the Light using the selected robot.
    SwitchOn(robot, 'LightSwitch')

# TASK ALLOCATION
robots = [
    {'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass': 100},
    {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject','ThrowObject','PushObject','PullObject'], 'mass': 100},
    {'name': 'robot3', 'skills': ['GoToObject','Open Object','Close Object','Break Object','Slice Object','Switch On','Switch Off','Pickup Object','Put Object','Drop Hand Object','Throw Object','Push Object','Pull Object'], 'mass': 100}
]

# Since all robots have the required skills and mass capacity, we can choose any robot. Let's choose robot1.
turn_on_light('robot1')

# Task turn on the light is done
```

### Explanation:
1. **Function Definition**: The `turn_on_light` function takes a robot as an argument and performs two actions:
   - Moves to the `LightSwitch` using `GoToObject`.
   - Activates the `LightSwitch` using `SwitchOn`.

2. **Task Allocation**:
   - We have three robots available, all of which possess the necessary skills (`GoToObject` and `SwitchOn`) and have sufficient mass capacity to handle any negligible mass associated with operating a light switch.
   - In this case, we simply select `robot1` to perform this task.

3. **Execution**: The function is called with `robot1`, executing both steps sequentially.

This implementation is straightforward since it involves a single subtask that can be executed immediately without dependencies or complex coordination among multiple robots.