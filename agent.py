# agent.py
def perceive_environment(environment, agent_pos, grid_size):
    """Perceive Stench, Breeze, Glitter."""
    x, y = agent_pos
    perceptions = []
    
    # Check adjacent cells
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < grid_size and 0 <= ny < grid_size:
            if environment[nx][ny] == "W":
                perceptions.append("Stench")
            elif environment[nx][ny] == "P":
                perceptions.append("Breeze")
    
    # Check current cell
    if environment[x][y] == "G":
        perceptions.append("Glitter")
    
    return perceptions

def move_agent(environment, agent_pos, action, grid_size):
    """Safe movement with boundary/hazard checks."""
    x, y = agent_pos
    new_x, new_y = x, y
    
    if action == "up": new_x = x-1
    elif action == "down": new_x = x+1
    elif action == "left": new_y = y-1
    elif action == "right": new_y = y+1
    
    # Validate move
    if (new_x < 0 or new_x >= grid_size or 
        new_y < 0 or new_y >= grid_size or
        environment[new_x][new_y] in ["W", "P"]):
        return (x, y), "failure"
    
    # Update position
    environment[x][y] = ""
    environment[new_x][new_y] = "A"
    return (new_x, new_y), "success"