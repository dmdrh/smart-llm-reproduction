To cook the potato and put it in the fridge, we can break down the task into several subtasks. The cooking process will involve preparing the potato, frying it, and then placing it in the fridge. Here's how we can structure the code for this task:

### Task Decomposition
1. **Prepare the Potato**: Slice the potato.
2. **Fry the Potato**: Cook the sliced potato in a pan on the stove.
3. **Put the Fried Potato in the Fridge**: After frying, place the potato in the fridge to cool.

### Code Implementation
We can execute the first two subtasks sequentially, as they depend on each other, and then execute the last subtask after the frying is complete.

```python
def prepare_potato():
    # 0: SubTask 1: Prepare the Potato
    # 1: Go to the Knife.
    GoToObject('Knife')
    # 2: Pick up the Knife.
    PickupObject('Knife')
    # 3: Go to the Potato.
    GoToObject('Potato')
    # 4: Slice the Potato.
    SliceObject('Potato')
    # 5: Go to the countertop.
    GoToObject('CounterTop')
    # 6: Put the Knife back on the CounterTop.
    PutObject('Knife', 'CounterTop')

def fry_potato():
    # 0: SubTask 2: Fry the Potato
    # 1: Go to the sliced Potato.
    GoToObject('Potato')
    # 2: Pick up the sliced Potato.
    PickupObject('Potato')
    # 3: Go to the Pan.
    GoToObject('Pan')
    # 4: Put the sliced Potato in the Pan.
    PutObject('Potato', 'Pan')
    # 5: Pick up the pan with potato in it.
    PickupObject('Pan')
    # 6: Go to the StoveBurner.
    GoToObject('StoveBurner')
    # 7: Put the Pan on the stove burner.
    PutObject('Pan', 'StoveBurner')
    # 8: Switch on the StoveKnob.
    SwitchOn('StoveKnob')
    # 9: Wait for a while to let the Potato fry.
    time.sleep(5)
    # 10: Switch off the StoveKnob.
    SwitchOff('StoveKnob')

def put_fried_potato_in_fridge():
    # 0: SubTask 3: Put the Fried Potato in the Fridge
    # 1: Go to the Pan.
    GoToObject('Pan')
    # 2: Pick up the Pan with the fried Potato.
    PickupObject('Pan')
    # 3: Go to the Fridge.
    GoToObject('Fridge')
    # 4: Open the Fridge.
    OpenObject('Fridge')
    # 5: Put the Pan in the Fridge.
    PutObject('Pan', 'Fridge')
    # 6: Close the Fridge.
    CloseObject('Fridge')

# Execute SubTask 1
prepare_potato()

# Execute SubTask 2
fry_potato()

# Execute SubTask 3
put_fried_potato_in_fridge()

# Task cook the potato and put it in the Fridge is done
```

### Explanation
1. **Prepare the Potato**: The `prepare_potato` function handles slicing the potato using a knife.
2. **Fry the Potato**: The `fry_potato` function takes the sliced potato, places it in a pan, and cooks it on the stove.
3. **Put the Fried Potato in the Fridge**: The `put_fried_potato_in_fridge` function retrieves the pan with the fried potato and places it in the fridge to cool.

This structure ensures that each step is executed in the correct order, and the potato is properly prepared, cooked, and stored.