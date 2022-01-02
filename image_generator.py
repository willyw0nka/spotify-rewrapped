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

    def add_font(self, name: str, path: str, size: int):
        """Adds a font to the fonts dictionary.
        This font will be avaliable to use on the other methods.

        Args:
            name (str): Name that will be given to the font.
            path (str): Font.otf path.
            size (int): Size of the font.
        """
        self.fonts[name] = ImageFont.truetype(path, size)

    def save(self, path: str):
        """Saves the image to the specified path.

        Args:
            path (str): Destination path.
        """
        self.background.save(path)

    def write_text(self, text: str, font: str, position: tuple, horizontal_center: bool = False, color: tuple =  (255, 255, 255)):
        """Writes the specified text with the specified font on the specified position.

        Args:
            text (str): Text to write.
            font (str): Font to use. The given value must be a font name added previously with
            the add_font method.
            position (tuple): Tuple of type (x, y)
            horizontal_center (bool, optional): Center the text horizonally. Defaults to False.
            color (tuple, optional): Color to render the text. Tuple of type (r, g, b). Defaults to White.
        """
        text_color = self.colors['white']
        if color is not None:
            text_color = color
        draw = ImageDraw.Draw(self.background)
        w, h = draw.textsize(text, font=self.fonts[font])
        if horizontal_center:
            position = ((self.W-w)/2, position[1])
        draw.text(position, text, text_color,font=self.fonts[font])

    def paste_image(self, path: str, position: tuple):
        """Pastes the specified image on the specified position.

        Args:
            path (str): Path of the desired image.
            position (tuple): Tuple of type (x, y) where the image will be pasted.
        """
        plot = Image.open(path, 'r')
        self.background.paste(plot, position)

    def show_achievement(self, icon: str, position: tuple, size: int, title: str, description: str, achieved: bool):
        """Creates an achievement widget on the specified position.

        Args:
            icon (str): Character to display the achivement. This str is using FontAwesome5.
            position (tuple): Coordinates where the achievement widget will start its render
            (top-left corner). Tuple of type (x, y).
            size (int): Size of the achievement icon square.
            title (str): Title of the achievement.
            description (str): Description of the achievement.
            achieved (bool): Indicates wether the achievement is achieved or not. This affects the
            ahievement icon square background color.
        """
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
