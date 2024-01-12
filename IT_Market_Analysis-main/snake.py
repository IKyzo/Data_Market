def snake_journey(length, wind_direction, start_coords):
    snake_path = []
    
    # Create a 2D grid
    grid = [[0 for _ in range(length)] for _ in range(length)]
    
    # Set the initial position of the snake
    x, y = start_coords
    grid[x][y] = 1
    
    # Define movement directions based on wind direction
    directions = {'n': (-1, 0), 's': (1, 0), 'w': (0, -1), 'e': (0, 1)}
    
    # Function to check if the next move is within bounds
    def is_valid_move(x, y):
        return 0 <= x < length and 0 <= y < length and grid[x][y] == 0
    
    # Function to check if the snake should move in the opposite direction of the wind
    def should_move_opposite(x, y, wind_direction):
        dx, dy = directions[wind_direction]
        new_x, new_y = x + dx, y + dy
        return is_valid_move(new_x, new_y) and (grid[new_x][new_y] == 0 or (x == length - 1 and y == length - 1))
    
    # Move the snake
    time = 1
    while time <= length * length:
        dx, dy = directions[wind_direction]
        new_x, new_y = x + dx, y + dy
        
        # Check if the snake should move in the opposite direction
        if should_move_opposite(x, y, wind_direction):
            x, y = new_x, new_y
        else:
            while not is_valid_move(x, y):
                # Change direction clockwise
                wind_direction = 'n' if wind_direction == 'e' else 'e' if wind_direction == 's' else 's' if wind_direction == 'w' else 'w'
                dx, dy = directions[wind_direction]
                new_x, new_y = x + dx, y + dy
            
            x, y = new_x, new_y
        
        grid[x][y] = time
        snake_path.append((x + 1, y + 1))  # Add 1 to coordinates to match 1-indexing
        
        time += 1
    
    return snake_path


# Sample Input 0
length_0 = 2
wind_direction_0 = 'e'
start_coords_0 = (1, 0)

# Sample Output 0
result_0 = snake_journey(length_0, wind_direction_0, start_coords_0)
print(" ".join(map(str, result_0)))

# Sample Input 1
length_1 = 4
wind_direction_1 = 'n'
start_coords_1 = (0, 0)

# Sample Output 1
result_1 = snake_journey(length_1, wind_direction_1, start_coords_1)
for row in result_1:
    print(" ".join(map(str, row)))
