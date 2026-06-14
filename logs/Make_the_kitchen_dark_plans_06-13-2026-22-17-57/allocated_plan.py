### Task Decomposition
- **SubTask 1**: Turn off the light switch. (Skills Required: GoToObject, SwitchOff)

### CODE
```python
def make_kitchen_dark():
    # 0: SubTask 1: Turn off the light switch
    # 1: Go to the Light Switch.
    GoToObject('LightSwitch')
    # 2: Switch off the Light Switch.
    SwitchOff('LightSwitch')

# Execute SubTask 1
make_kitchen_dark()

# Task to make the kitchen dark is done
```

### TASK ALLOCATION

#### Robot and Object Details:
- **Robots**:
  - `robot1`: 
    - Skills: ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject']
    - Mass Capacity: 100 kg

- **Objects**:
  - `LightSwitch`: mass = 0.0 kg (no mass constraint)

#### Analysis of Skills and Mass Capacity:
- The required skills for SubTask 1 (turning off the light) are `GoToObject` and `SwitchOff`.
- Robot1 possesses both required skills (`GoToObject` and `SwitchOff`).
- The mass of the object involved in this task (the LightSwitch) is negligible (0.0 kg), which is well within robot1's capacity of 100 kg.

#### Conclusion on Execution Order:
Since there is only one subtask that can be performed independently, it will be executed sequentially as there are no other subtasks to perform in parallel.

### Final Allocation Decision:
Assign **robot1** to perform **SubTask 1**:

```python
# Execute SubTask using robot1
make_kitchen_dark()
```

This allocation satisfies all