# Task Description: Slice the banana

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Slice the Banana. (Skills Required: GoToObject, PickupObject, SliceObject, PutObject)
# We can execute SubTask 1.

# CODE
def slice_banana():
    # 0: SubTask 1: Slice the Banana
    # 1: Go to the Knife.
    GoToObject('Knife')
    # 2: Pick up the Knife.
    PickupObject('Knife')
    # 3: Go to the Banana.
    GoToObject('Banana')
    # 4: Slice the Banana.
    SliceObject('Banana')
    # 5: Go to the countertop.
    GoToObject('CounterTop')
    # 6: Put the Knife back on the CounterTop.
    PutObject('Knife', 'CounterTop')

# Execute SubTask 1
slice_banana()

# Task slice the banana is done