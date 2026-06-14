To solve the task of moving the fridge to the corner, we need to consider both the skills and mass capacity of the available robots. Here's how we can approach this:

### Task Decomposition
1. **Go to the Fridge**: Navigate to the fridge's current location.
2. **Move the Fridge**: Use a combination of pushing or pulling to move the fridge to the desired location.

### Task Allocation
Given that all robots have similar skills but different mass capacities, we will focus on mass capacity for this task allocation.

#### SubTask 1: Go to the Fridge
- **Skills Required**: `GoToObject`
- All robots have this skill, so any robot can perform this subtask.

#### SubTask 2: Move the Fridge
- **Skills Required**: `PushObject` or `PullObject`
- The fridge has a mass of 0 (as per provided data), which seems incorrect for a real-world scenario. Assuming it requires significant force due to its size and typical weight, we'll consider using multiple robots if needed.
  
### Robot Mass Capacities:
- Robot 1: 1.0 kg
- Robot 2: 2.1 kg
- Robot 3: 0.9 kg

Since moving a fridge typically requires more force than any single robot's capacity here, we'll assume that forming a team is necessary despite its listed zero mass.

### Team Formation:
For moving heavy objects like a fridge:
- Combine Robots with sufficient combined mass capacity.
  
Given our constraints:
- Forming a team with Robots 1 and 2 gives us a combined capacity of \(1.0 + 2.1 = 3.1\) kg.
  
This team should be able to handle moving an object like a fridge in terms of collaborative effort.

### Execution Plan:
Since both subtasks are dependent on each other (you can't move it without first going there), they must be performed sequentially