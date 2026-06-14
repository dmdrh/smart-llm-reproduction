To turn on the light, we can create a simple function that utilizes the `SwitchOn` skill. This task is straightforward and does not require any complex decomposition or parallelization since it consists of a single action. 

Here's how you can implement the task to turn on the light:

```python
# Task Description: Turn on the light

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Turn on the light. (Skills Required: GoToObject, SwitchOn)

# CODE
def turn_on_light():
    # 0: SubTask 1: Turn on the light
    # 1: Go to the LightSwitch.
    GoToObject('LightSwitch')
    # 2: Switch on the Light.
    SwitchOn('LightSwitch')

# Execute SubTask 1
turn_on_light()

# Task turn on the light is done
```

### Explanation:
1. **GoToObject('LightSwitch')**: The robot moves to the location of the light switch.
2. **SwitchOn('LightSwitch')**: The robot activates the light switch to turn on the light.

This task is simple and can be executed immediately without any dependencies on other tasks.