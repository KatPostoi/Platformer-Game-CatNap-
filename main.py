"""
Platformer Game

python -m arcade.examples.platform_tutorial.03_more_sprites
"""
import arcade

# Constants
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WINDOW_TITLE = "CatNap"

# Constants used to scale our sprites from their original size
TILE_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5

JUMP_MAX_HEIGHT = 180

PLAYER_X_SPEED = 5
PLAYER_Y_SPEED = 5


class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.player_texture = None
        self.player_sprite = None
        self.player_list = None

        self.wall_list = None

        self.camera = None
        self.camera_max = 0

        self.player_jump = False
        self.player_start = None

        self.key_right_pressed = False
        self.key_left_pressed = False

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        # Загрузка изображения фона
        self.background_image = arcade.load_texture(
            "images/background.png")

        # Variable to hold our texture for our player
        self.player_texture = arcade.load_texture(
            "images\player.png"
        )

        # Separate variable that holds the player sprite
        self.player_sprite = arcade.Sprite(self.player_texture, scale=0.3)
        self.player_sprite.center_x = 155
        self.player_sprite.center_y = 185

        # SpriteList for our player
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # SpriteList for our boxes and ground
        # Putting our ground and box Sprites in the same SpriteList
        # will make it easier to perform collision detection against
        # them later on. Setting the spatial hash to True will make
        # collision detection much faster if the objects in this
        # SpriteList do not move.
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(
                "images\ground.png", scale=TILE_SCALING)
            wall.center_x = x
            wall.center_y = 148
            self.wall_list.append(wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites

        PLATFORMS: list = [{"x": 100, "y": 100}, {"x": 200, "y": 200}, {
            "x": 300, "y": 300}, {"x": 400, "y": 400}]
        PLATFORMS[0] = arcade.Sprite(
            "images\ground.png", scale=TILE_SCALING)
        PLATFORMS[1] = arcade.Sprite(
            "images\ground.png", scale=TILE_SCALING)
        PLATFORMS[2] = arcade.Sprite(
            "images\ground.png", scale=TILE_SCALING)
        PLATFORMS[3] = arcade.Sprite(
            "images\ground.png", scale=TILE_SCALING)
        for items in PLATFORMS:
            # Add a crate platforms
            wall.position = items
            self.wall_list.append(PLATFORMS)

        #coordinate_list = [[512, 96], [256, 96], [768, 96]]
        # for coordinate in coordinate_list:
        #    # Add a crate on the ground
        #    wall = arcade.Sprite(
        #        ":resources:images/tiles/boxCrate_double.png", scale=TILE_SCALING)
        #    wall.position = coordinate
        #    self.wall_list.append(wall)

        # Create a Simple Physics Engine, this will handle moving our
        # player as well as collisions between the player sprite and
        # whatever SpriteList we specify for the walls.
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.wall_list)

        self.camera = arcade.Camera2D()

        #self.background_color = arcade.csscolor.CORNFLOWER_BLUE

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        self.camera.use()

        # Рисуем фоновое изображение
        arcade.draw_texture_rect(self.background_image, arcade.LBWH(
            0, 0, 6016, WINDOW_HEIGHT))

        # Draw our sprites
        self.player_list.draw()
        self.wall_list.draw()

    def center_camera_to_player(self):
        screen_center_y = self.player_sprite.center_y
        self.camera_max = 0

        if self.player_sprite.center_x - (self.camera.viewport_width / 4) >= self.camera_max:
            screen_center_x = self.player_sprite.center_x - \
                (self.camera.viewport_width / 4)
            self.camera_max = self.player_sprite.center_x - \
                (self.camera.viewport_width / 4)
        else:
            screen_center_x = self.camera_max

        if screen_center_x < self.camera.viewport_width / 2:
            screen_center_x = self.camera.viewport_width / 2
        if screen_center_y < self.camera.viewport_height / 2:
            screen_center_y = self.camera.viewport_height / 2

        player_centered = screen_center_x, screen_center_y
        self.camera.position = player_centered

    def player_movement(self):
        if self.key_left_pressed:
            self.player_sprite.center_x -= PLAYER_MOVEMENT_SPEED
        if self.key_right_pressed:
            self.player_sprite.center_x += PLAYER_MOVEMENT_SPEED

        if self.player_jump:
            self.player_sprite.center_y += 2
            if self.player_sprite.center_y > self.jump_start + JUMP_MAX_HEIGHT:
                self.player_jump = False
        else:
            if self.player_sprite.center_y >= 185:
                self.player_sprite.center_y -= 2

    def on_update(self, delta_time):
        """Movement and Game Logic"""
        #self.player_sprite.center_x += 5

        self.center_camera_to_player()
        self.player_movement()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.ESCAPE:
            self.setup()

        if key == arcade.key.UP or key == arcade.key.W:
            #self.player_sprite.center_y += 180
            self.player_jump = True
            self.jump_start = self.player_sprite.center_y
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.center_y -= 180
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.key_left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_right_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.key_left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_right_pressed = False


def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
