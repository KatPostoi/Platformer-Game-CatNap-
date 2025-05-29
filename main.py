"""
Platformer Game

python -m arcade.examples.platform_tutorial.01_open_window
"""
import arcade

# Constants
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WINDOW_TITLE = "CatNap"


class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class to set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        #self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        # Загрузка изображения фона
        self.background_image = arcade.load_texture(
            "images/background.png")

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""

        # The clear method should always be called at the start of on_draw.
        # It clears the whole screen to whatever the background color is
        # set to. This ensures that you have a clean slate for drawing each
        # frame of the game.
        self.clear()

        # Code to draw other things will go here

        # Очистка экрана
        arcade.start_render()

        # Рисуем фоновое изображение
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT,
                                      self.background_image)


def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
