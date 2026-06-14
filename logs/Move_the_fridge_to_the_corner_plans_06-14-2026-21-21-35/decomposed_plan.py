To move the fridge to the corner, we need to consider the skills available and the constraints of the task. Given the skills you have listed, it seems like the most relevant actions would involve using `GoToObject`, `PushObject`, or `PullObject`. However, since the fridge is typically a heavy object, it might not be feasible to move it with the skills provided unless the robot is capable of handling such tasks.

Here's a general approach to moving the fridge to the corner:

### Task Decomposition
1. **Go to the Fridge**: Navigate to the fridge's current location.
2. **Assess the Fridge's Position**: Determine the best way to move the fridge to the corner.
3. **Move the Fridge**: Use a combination of pushing or pulling to move the fridge to the desired location.

### Code Implementation
```python
def move_fridge_to_corner():
    # 1: Go to the Fridge.
    GoToObject('Fridge')
    
    # 2: Assess the Fridge's Position (This step is conceptual and would depend on the robot's sensors and logic)
    # For simplicity, we assume the robot knows the direction to push or pull the fridge.
    
    # 3: Move the Fridge to the corner.
    # Assuming the robot can push the fridge, we use PushObject.
    # If the robot needs to pull, use PullObject instead.
    PushObject('Fridge')  # or PullObject('Fridge') depending on the situation

# Execute the task
move_fridge_to_corner()

# Task to move the fridge to the corner is done
```

### Considerations
- **Weight and Feasibility**: Ensure the robot can handle the weight of the fridge. If not, additional equipment or assistance might be needed.
- **Path Planning**: The robot should have a clear path to move the fridge without obstacles.
- **Safety**: Ensure the movement is safe for both the robot and the environment.

This code assumes the robot has the capability to push or pull heavy objects like a fridge. If the robot lacks this capability, you might need to consider alternative methods or tools to assist in moving the fridge.