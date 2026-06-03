from pymaze import maze, agent, textLabel
from PIL import Image, ImageDraw

# Parameters for image size
mm_width = 80  # Width in mm
ppi = 203  # Print DPI
width_in_pixels = int(mm_width * ppi / 25.4)  # Convert mm to pixels (80mm * 203 / 25.4mm per inch)

# Create a maze of appropriate size
m = maze(width_in_pixels // 20, width_in_pixels // 20)  # Maze dimensions (can adjust cell size)

# Generate the maze using Prim's algorithm (default)
m.CreateMaze()

# Drawing the maze to an image
def draw_maze_image(maze_obj, img_width, img_height):
    img = Image.new('1', (img_width, img_height), 1)  # Create a white background
    draw = ImageDraw.Draw(img)
    cell_size = img_width // maze_obj.rows  # Determine the size of each cell based on maze size

    # Draw the walls of the maze
    for cell in maze_obj.grid.values():
        x1, y1 = cell.x * cell_size, cell.y * cell_size
        x2, y2 = (cell.x + 1) * cell_size, (cell.y + 1) * cell_size

        if cell.walls['N']:
            draw.line([x1, y1, x2, y1], fill=0)  # Draw north wall
        if cell.walls['S']:
            draw.line([x1, y2, x2, y2], fill=0)  # Draw south wall
        if cell.walls['E']:
            draw.line([x2, y1, x2, y2], fill=0)  # Draw east wall
        if cell.walls['W']:
            draw.line([x1, y1, x1, y2], fill=0)  # Draw west wall

    return img

# Generate the maze image
maze_image = draw_maze_image(m, width_in_pixels, width_in_pixels)
maze_image.save('pymaze_square_maze.png')  # Save as PNG
maze_image.show()  # Display the image
