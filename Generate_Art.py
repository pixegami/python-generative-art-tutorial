from PIL import Image, ImageDraw, ImageChops
import random
import os
import colorsys
import argparse

from numpy import reciprocal

def random_point(image_size_px: int, padding: int) -> tuple:
    """Generate a random point within the given image size,
       and avoid the boundaries with the given padding value.

    Args:
        image_size_px (int): size of the image in pixels.
        padding (int): size of the padding of the boader to be avoided.
    
    Return:
        tuple: (x, y) coordinate.  
    """
    return (random.randint(padding, image_size_px - padding),
            random.randint(padding, image_size_px - padding))
    
def random_color() -> tuple:
    """First Generate a random color in HSV(Hue, Saturation, Value) format,
       with fully saturated and fully bright color and then convert the 
       color into RGB Format.

    Args:
        None
    
    Return:
        tuple: (R, G, B) color.
    """
    random_H = random.random()
    S = 1    
    V = 1
    color_RGB = colorsys.hsv_to_rgb(random_H, S, V)
    color_RGB = [int(channel * 255) for channel in color_RGB]
    
    return tuple(color_RGB) 

def interpolate(start_color: tuple, end_color: tuple, factor: float) -> tuple:
    """Return the blend color of start_color and end_color depending on the factor.
       or finding the color that is exactly factor (0.0 - 1.0) between the two colors.

    Args:
        start_color (tuple): (R, G, B) color format.
        end_color (tuple): (R, G, B) color format.
        factor (float): factor between 0 and 1.

    Returns:
        tuple: (R, G, B) color.
    """
    reciprocal = 1 - factor
    
    return (int(start_color[0]*reciprocal + end_color[0]*factor),
            int(start_color[1]*reciprocal + end_color[1]*factor),
            int(start_color[2]*reciprocal + end_color[2]*factor))
    
def generate_art(art_collection: str, art_name: str, art_size_px: int, total_line: int):
    """This is the main function to generate a art image,
       and store it in the given collection path with the 
       given name.

    Args:
        art_collection (str): path of the folder.
        art_name (str): name of the image.
        art_size_px (int): size of the image in px.
        total_line (int): Total number of lines to be drawn.
    """
    print("Generating Art!")
    
    # Create the path to the directory where we will store the images
    Art_Gallery_Path = os.path.join("Art Gallery", art_collection)
    Art_Path = os.path.join(Art_Gallery_Path, f"{art_name}.png")
    
    # Setting The Size Parameter
    RESCALE_FACTOR = 2
    Image_Size_Px = art_size_px * RESCALE_FACTOR
    PADDING = int(Image_Size_Px * 0.1)
    
    # Create the directory to store the Arts
    os.makedirs(Art_Gallery_Path, exist_ok = True)
    
    # Create an Canvas for the Art
    BACKGROUND_COLOR = (0, 0, 0)  # Black
    canvas = Image.new(mode = "RGB", size = (Image_Size_Px, Image_Size_Px), color = BACKGROUND_COLOR)
    
    # Generate random points for the lines
    points = []
    
    for _ in range(total_line):
        points.append(random_point(Image_Size_Px, PADDING))
    
    # Get The Minimum and Maximum x and y Coordinates.
    min_x = min([point[0] for point in points])
    max_x = max([point[0] for point in points])
    min_y = min([point[1] for point in points])
    max_y = max([point[1] for point in points])
    
    # centralize the art in the image.
    delta_x = min_x - Image_Size_Px + max_x
    delta_y = min_y - Image_Size_Px + max_y
    
    # Centralize all the points.
    points = [(point[0] - delta_x // 2, point[1] - delta_y // 2) for point in points]
    
    # Select Random Color 
    Start_Color = random_color()
    End_Color = random_color()
    
    # Line Drawing Parameter
    Thickness = 1
    THICKNESS_FACTOR = total_line // 5
    Total_Points = len(points)
    
    # Draw The Art
    for i, point in enumerate(points):
        # create a overlay canvas
        overlay_art = Image.new(mode = "RGB", size = (Image_Size_Px, Image_Size_Px), color = BACKGROUND_COLOR)
        overlay_draw = ImageDraw.Draw(overlay_art)
        
        if i == Total_Points - 1:
            # connect the last point back to the first point.
            second_point = points[0]
        else:
            # connect the next point.
            second_point = points[i + 1]
            
        # interpolate the colors
        interpolate_factor = i / (Total_Points - 1)
        line_color = interpolate(start_color = Start_Color, end_color = End_Color, factor = interpolate_factor)
        
        # Draw the line.
        overlay_draw.line(xy = (point, second_point), fill = line_color, width = Thickness)
        
        # Increase the thickness of the line.
        Thickness += THICKNESS_FACTOR
        
        # Add the overlay channel.
        canvas = ImageChops.add(overlay_art, canvas)
        
    # Art is Ready! Now resize it to be smooth.
    canvas = canvas.resize(size = (art_size_px, art_size_px),
                           resample = Image.ANTIALIAS)
    
    # Save the Art
    canvas.save(Art_Path)


if(__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type = int, default = 1, help = "Number of arts to be generated.")
    parser.add_argument("--gallery", type = str, help = "Art Collection Gallery name.")
    parser.add_argument("--size", type = int, default = 256, help = "Size of the Image.")
    parser.add_argument("--l", type = int, default = 10, help = "Total number of lines in the Image.")
    
    args = parser.parse_args()
    n = args.n
    gallery_collection = args.gallery
    image_size = args.size
    l = args.l
    
    for i in range(n):
        generate_art(gallery_collection, f"{gallery_collection}_image_{i}", image_size, l)