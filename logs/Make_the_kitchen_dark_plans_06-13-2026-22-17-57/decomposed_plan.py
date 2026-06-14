To make the kitchen dark, we can assume that the task involves turning off the lights or any light sources in the kitchen. This can typically be done by interacting with a light switch. 

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

### Explanation
1. **GoToObject('LightSwitch')**: The robot navigates to the light switch.
2. **SwitchOff('LightSwitch')**: The robot turns off the light switch, effectively making the kitchen dark.

This simple task can be executed sequentially since it only involves one action.