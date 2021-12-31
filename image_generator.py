"""This module contains the ImageGenerator class which is responsible of generating the final png."""
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class ImageGenerator:
    """ImageGenerator. Contains the methods that allow creating the final png."""
    def __init__(self, size=(1500, 2000)):
        self.colors = {'background': (25, 20, 20),
                       'foreground': (29, 185, 84),
                       'light-gray': (83, 83, 83),
                       'white': (255, 255, 255)}
        self.foreground_color = (29, 185, 84)
        self.W, self.H = size
        self.fonts = {}
        self.background = Image.new('RGB', (self.W, self.H), color = self.colors['background'])

    def add_font(self, name, path, size):
        """Adds a font to the fonts dictionary, this font will be avaliable to
        use on the other methods."""
        self.fonts[name] = ImageFont.truetype(path, size)

    def save(self, path):
        """Saves the image to the specified path."""
        self.background.save(path)

    def write_text(self, text, font, position, horizontal_center=False, color=None):
        """Writes the specified text on the specified position."""
        text_color = self.colors['white']
        if color is not None:
            text_color = color
        draw = ImageDraw.Draw(self.background)
        w, h = draw.textsize(text, font=self.fonts[font])
        if horizontal_center:
            position = ((self.W-w)/2, position[1])
        draw.text(position, text, text_color,font=self.fonts[font])

    def paste_image(self, path, position):
        """Pastes the specified image on the specified position."""
        plot = Image.open(path, 'r')
        self.background.paste(plot, position)

    def show_achievement(self, icon, position, size, title, description, achieved):
        """Creates an achievement widget on the specified position."""
        draw = ImageDraw.Draw(self.background)
        rect_coords = [position,
                       (position[0] + size[0], position[1] + size[1])]
        rect_color = self.colors['foreground'] if achieved else self.colors['light-gray']
        draw.rounded_rectangle(rect_coords, fill=rect_color, radius=7)

        w, h = draw.textsize(icon, font=self.fonts['icons'])
        icon_position = (position[0] + (size[0]-w)/2,
                         (position[1] + (size[1]-h)/2))
        self.write_text(icon, 'icons', icon_position, color=self.colors['background'])

        title_position = (position[0] + size[0] + 25, position[1] + 5)
        self.write_text(title, 'achievement-title', title_position)

        body_position = (position[0] + size[0] + 25, position[1] + 35)
        self.write_text(description, 'achievement-body', body_position)
