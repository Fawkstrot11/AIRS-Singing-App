# Takes the raw value from the grader and turns it into stuff for the website to use
import noteUtils
from PIL import Image, ImageDraw
"""
        Makes an image to that represents the performance.
        :param data_list: the target notes, as a number (where C = 1, C# = 2,... B=12)
        :param dot_list: List of input values recorded, as Hz (from 261hz (C4) to 494(B5, I think? Our upper note).)
        :param output_filename: the name of the image created.
        """
def create_blocks_image(data_list, dot_list, numrows, output_filename='output.png', dotmin = 261, dotmax = 494):
    # Constants
    IMAGE_WIDTH, IMAGE_HEIGHT = 2430, 1620
    background_image_path = "assets/airs_output_background.png"
    EDITABLE_X_START, EDITABLE_X_END = 186, 2247
    EDITABLE_Y_START, EDITABLE_Y_END = 150, 1473
    ROW_HEIGHT = 105
    BORDER_SIZE = 6
    NUM_ROWS = 24
    EDITABLE_WIDTH = EDITABLE_X_END - EDITABLE_X_START
    DOT_MIN, DOT_MAX = dotmin, dotmax
    EDITABLE_HEIGHT = EDITABLE_Y_END - EDITABLE_Y_START

    # Calculate block width
    num_blocks = len(data_list)
    if num_blocks == 0:
        raise ValueError("The data list cannot be empty.")
    block_width = EDITABLE_WIDTH / num_blocks

    # Open background image
    img = Image.open(background_image_path).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Draw blocks
    for i, value in enumerate(data_list):
        if not (1 <= value <= NUM_ROWS):
            raise ValueError(f"List element {value} is out of valid range (1-{NUM_ROWS}).")

        # Calculate block position
        x0 = EDITABLE_X_START + i * block_width
        x1 = x0 + block_width

        row_index = NUM_ROWS - value  # Invert to make row 1 at the bottom
        y0 = EDITABLE_Y_START + row_index * (ROW_HEIGHT + BORDER_SIZE)
        y1 = y0 + ROW_HEIGHT

        # Draw the block
        color = (0, 128, 255)  # Blue blocks
        draw.rectangle([x0, y0, x1, y1], fill=color)

    # Draw dots and connecting lines
    num_dots = len(dot_list)
    if num_dots > 0:
        dot_spacing = EDITABLE_WIDTH / (num_dots - 1) if num_dots > 1 else 0

        prev_coords = None
        for i, value in enumerate(dot_list):
            if not (DOT_MIN <= value <= DOT_MAX):
                raise ValueError(f"Dot element {value} is out of valid range ({DOT_MIN}-{DOT_MAX}).")

            # Calculate dot position
            x = EDITABLE_X_START + i * dot_spacing
            normalized_value = (value - DOT_MIN) / (DOT_MAX - DOT_MIN)
            y = EDITABLE_Y_END - (normalized_value * EDITABLE_HEIGHT)

            # Draw connecting line
            if prev_coords:
                draw.line([prev_coords, (x, y)], fill='black', width=5)

            # Draw the dot
            dot_radius = 10
            draw.ellipse([x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius], fill='black', outline='black')

            prev_coords = (x, y)

    # Save the image
    img.save(output_filename)
    print(f"Image saved as {output_filename}")

# Example usage
# create_blocks_image([1, 5, 3, 12, 8, 2], [300, 400, 350, 450, 380], 'background.png')

def setup_formats(base, notes_in, hz_in):
    base_min, base_max = noteUtils.order_range(base)
    notes_min, notes_max = noteUtils.order_range(notes_in)

    true_min = min(base_min, notes_min)-1
    true_max = max(base_max, notes_max)+1

    target = []
    for i in base:
        target.append(noteUtils.note_to_order(i)-true_min)

    hz_min = noteUtils.note_name_to_hz(noteUtils.order_to_note(true_min))
    hz_max = noteUtils.note_name_to_hz(noteUtils.order_to_note(true_min+12))

    hertzes = []
    for i in hz_in:
        hertzes.append(i-hz_min)
    print(true_min,true_max)
    print(hz_min, hz_max)
    create_blocks_image(target, hz_in, true_max-true_min, dotmax=1600, dotmin=0)
