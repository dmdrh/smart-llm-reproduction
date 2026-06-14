To accomplish the task of putting an apple in the fridge and switching off the light, we can break it down into two independent subtasks:

1. **Put the apple in the fridge** (Skills Required: GoToObject, PickupObject, OpenObject, PutObject, CloseObject).
2. **Switch off the light** (Skills Required: GoToObject, SwitchOff).

### Task Allocation Analysis

#### Subtask 1: Put the Apple in the Fridge
- **Required Skills**: 
  - GoToObject
  - PickupObject
  - OpenObject
  - PutObject
  - CloseObject

- **Mass of Objects Involved**:
  - Apple: approximately 0.2 kg
  - Fridge: mass is not relevant for this subtask as it is a receptacle.

#### Subtask 2: Switch Off the Light
- **Required Skills**:
  - GoToObject
  - SwitchOff

- **Mass of Objects Involved**:
  - LightSwitch: mass is not relevant for this subtask as it is a control object.

### Robot Capabilities

We have three robots available with identical skills and mass capacity:

```python
robots = [
    {'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass': 100},
    {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'Put Object','DropHand Object','Throw Object','Push Object','Pull Object'],'mass':100},
    {'name':'robot3','skills':['GoTo Object','Open