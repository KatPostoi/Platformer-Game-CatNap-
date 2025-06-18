"""
Platformer Game

python -m arcade.examples.platform_tutorial.03_more_sprites
"""
from random import randint
from typing import Dict, List
import arcade
import math
import arcade.gui

# Constants
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WINDOW_TITLE = "CatNap"

# Constants used to scale our sprites from their original size
TILE_SCALING = 1
COIN_SCALING = 1
ENEMY_SCALING = 0.13

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5

JUMP_MAX_HEIGHT = 180
JUMP_MAX_HEIGHT_2 = 360

PLAYER_X_SPEED = 5
PLAYER_Y_SPEED = 5

PLAYER_SPRITE_IMAGE_CHANGE_SPEED = 30

LEFT_FACING = -1
RIGHT_FACING = 1


class MainView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        self.player_texture = None
        self.player_sprite = None
        self.player_list = None

        self.wall_list = None

        self.camera = None
        self.camera_max = 0

        self.player_jump = False
        self.player_jump_2 = False
        self.player_start = None

        self.key_right_pressed = False
        self.key_left_pressed = False

        self.collide = False

        self.player_dx = PLAYER_X_SPEED
        self.player_dy = PLAYER_Y_SPEED

        self.gui_camera = None
        self.score = 0

        # SpriteList for coins the player can collect
        self.coin_list = None

        # SpriteList for enemies
        self.enemies_list: List[Enemy] = None

        # A variable to store our gui camera object
        self.gui_camera = None

        # This variable will store our score as an integer.
        self.score = 0

        # This variable will store the text for score that we will draw to the screen.
        self.score_text = None

        self.total_time = 0

        self.player_sprite_images_r = []

        self.manager = arcade.gui.UIManager()

        switch_menu_button = arcade.gui.UIFlatButton(text="||", width=50)

        # Initialise the button with an on_click event.
        @switch_menu_button.event("on_click")
        def on_click_switch_button(event):
            # Passing the main view into menu view as an argument.
            menu_view = MenuView(self)
            self.window.show_view(menu_view)

        # Use the anchor to position the button on the screen.
        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            anchor_x="right",
            anchor_y="top",
            child=switch_menu_button,
        )

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_show_view(self):
        """This is run once when we switch to this view"""
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Enable the UIManager when the view is showm.
        self.manager.enable()

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        # Загрузка изображения фона
        self.background_image = arcade.load_texture(
            "images/background.png")

        # Variable to hold our texture for our player
        self.player_texture = arcade.load_texture(
            "images\player1.png"
        )

        # Separate variable that holds the player sprite
        self.player_sprite = arcade.Sprite(self.player_texture, scale=0.3)
        self.player_sprite.center_x = 155
        self.player_sprite.center_y = 290

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
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.enemies_list = arcade.SpriteList(use_spatial_hash=True)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        # for x in range(0, 1250, 64):
        #     wall = arcade.Sprite(
        #         "images\ground.png", scale=TILE_SCALING)
        #     wall.center_x = x
        #     wall.center_y = 148
        #     self.wall_list.append(wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites

        PLATFORMS: List[Dict] = [{"x": 395, "y": 155, "img": arcade.Sprite(
            "images\platform1.png", scale=TILE_SCALING)},
            {"x": 1200, "y": 155, "img": arcade.Sprite(
                "images\platform2.png", scale=TILE_SCALING)},
            {"x": 1550, "y": 335, "img": arcade.Sprite(
                "images\platform3.png", scale=TILE_SCALING)},
            {"x": 2100, "y": 335, "img": arcade.Sprite(
                "images\platform4.png", scale=TILE_SCALING)},
            {"x": 2000, "y": 698, "img": arcade.Sprite(
                "images\platform5.png", scale=TILE_SCALING)},
            {"x": 2550, "y": 515, "img": arcade.Sprite(
                "images\platform6.png", scale=TILE_SCALING)},
            {"x": 2550, "y": 875, "img": arcade.Sprite(
                "images\platform7.png", scale=TILE_SCALING)},
            {"x": 3050, "y": 694, "img": arcade.Sprite(
                "images\platform8.png", scale=TILE_SCALING)},
            {"x": 3250, "y": 335, "img": arcade.Sprite(
                "images\platform9.png", scale=TILE_SCALING)},
            {"x": 4050, "y": 335, "img": arcade.Sprite(
                "images\platform10.png", scale=TILE_SCALING)},
            {"x": 5180, "y": 153, "img": arcade.Sprite("images\platform11.png", scale=TILE_SCALING)}]
        for item in PLATFORMS:
            # Add a crate platforms
            x = item.get("x")
            y = item.get("y")
            wall: arcade.Sprite = item.get("img")
            wall.position = [x, y]
            self.wall_list.append(wall)

        # Add coins to the world

        coins: List[Dict] = [{"x": 1550, "y": 435},
                             {"x": 2000, "y": 798},
                             {"x": 2350, "y": 615},
                             {"x": 2550, "y": 975},
                             {"x": 3250, "y": 435},
                             {"x": 3750, "y": 435}]
        for item in coins:
            # Add a crate coins
            coin = arcade.Sprite(
                "images\coin.png", scale=COIN_SCALING)
            x = item.get("x")
            y = item.get("y")
            coin.position = [x, y]
            self.coin_list.append(coin)

        # Create a Simple Physics Engine, this will handle moving our
        # player as well as collisions between the player sprite and
        # whatever SpriteList we specify for the walls.
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.wall_list)

        self.camera = arcade.Camera2D()

        # self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # Initialize our camera, setting a viewport the size of our window.
        self.camera = arcade.Camera2D()

        # Initialize our gui camera, initial settings are the same as our world camera.
        self.gui_camera = arcade.Camera2D()

        # Reset our score to 0
        self.score = 0

        # Initialize our arcade.Text object for score
        self.score_text = arcade.Text(f"Score: {self.score}", x=100, y=50)

        for i in range(1, 5):
            self.player_sprite_images_r.append(
                arcade.load_texture(f"images\player{i}.png"))
        ENEMIES = [
            {"x": 2650, "y": 580, "img": arcade.Sprite(
                "images\enemy1.png", scale=ENEMY_SCALING)},
            {"x": 4200, "y": 400, "img": arcade.Sprite(
                "images\enemy1.png", scale=ENEMY_SCALING)}
        ]
        for enemy in ENEMIES:
            sprite: arcade.Sprite = enemy.get("img")
            x = enemy.get("x")
            y = enemy.get("y")
            sprite.position = [x, y]
            custom_enemy = Enemy(sprite)
            custom_enemy.speed = randint(1, 4)
            self.enemies_list.append(custom_enemy)

        # enemies: List[Dict] = [{"x": 2650, "y": 600},
        #                        {"x": 4200, "y": 420}]
        # for item in enemies:
        #     # Add a crate enemies
        #     enemy = arcade.Sprite(
        #         "images\enemy1.png", scale=ENEMY_SCALING)
        #     x = item.get("x")
        #     y = item.get("y")
        #     enemy.position = [x, y]
        #     self.enemies_list.append(enemy)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        self.camera.use()

        # Рисуем фоновое изображение
        arcade.draw_texture_rect(self.background_image, arcade.LBWH(
            0, 0, 6016, WINDOW_HEIGHT))

        # Draw our sprites
        self.wall_list.draw()
        self.player_list.draw()

        self.coin_list.draw()

        self.enemies_list.draw()

        # Activate our GUI camera
        self.gui_camera.use()

        # Draw our Score
        self.score_text.draw()

        arcade.Text(f"Time: {self.total_time_print}", x=100, y=75).draw()

        # Draw the manager.
        self.manager.draw()

    def enemies_movement(self):
        for enemy in self.enemies_list:
            if enemy.center_x > enemy.initial_center_x + 15:
                enemy.facing_direction = LEFT_FACING
            if enemy.center_x < enemy.initial_center_x - 15:
                enemy.facing_direction = RIGHT_FACING
            enemy.center_x += enemy.speed * enemy.facing_direction

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

    def show_win_screen(self):
        pass

    def player_movement(self):
        if self.player_sprite.center_x >= 5100:
            return

        if self.collide:
            self.player_dy = 0
            # self.player_dx = 0
        else:
            self.player_dy = PLAYER_Y_SPEED
            self.player_dx = PLAYER_X_SPEED

        if self.key_left_pressed:
            self.player_sprite.center_x -= self.player_dx
        if self.key_right_pressed:
            self.player_sprite.center_x += self.player_dx
            self.player_sprite.texture = self.player_sprite_images_r[int(
                self.player_sprite.center_x / PLAYER_SPRITE_IMAGE_CHANGE_SPEED) % 4]
            if self.player_sprite.center_x >= 5100:
                exit()
                self.show_win_screen()

        if self.player_jump:
            self.player_sprite.center_y += self.player_dy
            if self.player_sprite.center_y > self.jump_start + JUMP_MAX_HEIGHT:
                self.player_jump = False
        elif self.player_jump_2:
            self.player_sprite.center_y += self.player_dy
            if self.player_sprite.center_y > self.jump_start + JUMP_MAX_HEIGHT_2:
                self.player_jump_2 = False
        else:
            self.player_sprite.center_y -= self.player_dy

    def calculate_collision(self):
        self.collide = False

        for block in self.wall_list:
            if block.center_x + block.width / 2 >= self.player_sprite.center_x >= block.center_x - block.width / 2 and \
                    block.center_y + block.height / 2 >= self.player_sprite.center_y - self.player_sprite.height / 2 >= block.center_y - block.height / 2:
                self.collide = True

    def on_update(self, delta_time):
        """Movement and Game Logic"""
        # self.player_sprite.center_x += 5

        self.center_camera_to_player()
        self.player_movement()

        if self.player_jump:
            self.collide = False
        else:
            self.calculate_collision()

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            self.score += 75
            self.score_text.text = f"Score: {self.score}"

        # See if we hit any enemies
        enemies_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.enemies_list
        )

        # Loop through each enemies we hit (if any) and remove it
        for enemy in enemies_hit_list:
            # Remove the enemy
            enemy.remove_from_sprite_lists()
            self.score -= 150
            self.score_text.text = f"Score: {self.score}"

        self.total_time += delta_time
        ms, sec = math.modf(self.total_time)
        minutes = int(sec) // 60
        seconds = int(sec) % 60
        msec = int(ms*100)
        self.total_time_print = f"{minutes:02d}:{seconds:02d}:{msec:02d}"

        self.enemies_movement()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.ESCAPE:
            self.setup()

        if key == arcade.key.UP or key == arcade.key.W:
            # self.player_sprite.center_y += 180
            if self.collide:
                self.player_jump = True
                self.jump_start = self.player_sprite.center_y
        elif key == arcade.key.LCTRL or key == arcade.key.E:
            # self.player_sprite.center_y += 180
            if self.collide:
                self.player_jump_2 = True
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


class MenuView(arcade.View):
    """Main menu view class."""

    def __init__(self, main_view):
        super().__init__()

        self.manager = arcade.gui.UIManager()

        resume_button = arcade.gui.UIFlatButton(text="Resume", width=150)
        start_new_game_button = arcade.gui.UIFlatButton(
            text="Start New Game", width=150)
        volume_button = arcade.gui.UIFlatButton(text="Volume", width=150)
        options_button = arcade.gui.UIFlatButton(text="Options", width=150)

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=320)

        # Initialise a grid in which widgets can be arranged.
        self.grid = arcade.gui.UIGridLayout(
            column_count=2, row_count=3, horizontal_spacing=20, vertical_spacing=20
        )

        # Adding the buttons to the layout.
        self.grid.add(resume_button, column=0, row=0)
        self.grid.add(start_new_game_button, column=1, row=0)
        self.grid.add(volume_button, column=0, row=1)
        self.grid.add(options_button, column=1, row=1)
        self.grid.add(exit_button, column=0, row=2, column_span=2)

        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid,
        )

        self.main_view = main_view

        @resume_button.event("on_click")
        def on_click_resume_button(event):
            # Pass already created view because we are resuming.
            self.window.show_view(self.main_view)

        @start_new_game_button.event("on_click")
        def on_click_start_new_game_button(event):
            # Create a new view because we are starting a new game.
            main_view = MainView()
            main_view.setup()
            self.window.show_view(main_view)

        @exit_button.event("on_click")
        def on_click_exit_button(event):
            arcade.exit()

        @volume_button.event("on_click")
        def on_click_volume_button(event):
            volume_menu = SubMenu(
                "Volume Menu",
                "How do you like your volume?",
                "Enable Sound",
                ["Play: Rock", "Play: Punk", "Play: Pop"],
                "Adjust Volume",
            )
            self.manager.add(volume_menu, layer=1)

        @options_button.event("on_click")
        def on_click_options_button(event):
            options_menu = SubMenu(
                "Funny Menu",
                "Too much fun here",
                "Fun?",
                ["Make Fun", "Enjoy Fun", "Like Fun"],
                "Adjust Fun",
            )
            self.manager.add(options_menu, layer=1)

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_show_view(self):
        """This is run once when we switch to this view"""

        # Makes the background darker
        arcade.set_background_color(
            [rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])

        # Enable the UIManager when the view is showm.
        self.manager.enable()

    def on_draw(self):
        """Render the screen."""
        # Clear the screen
        self.clear()
        self.manager.draw()


class SubMenu(arcade.gui.UIMouseFilterMixin, arcade.gui.UIAnchorLayout):
    """Acts like a fake view/window."""

    def __init__(
        self,
        title: str,
        input_text: str,
        toggle_label: str,
        dropdown_options: List[str],
        slider_label: str,
    ):
        super().__init__(size_hint=(1, 1))

        # Setup frame which will act like the window.
        frame = self.add(arcade.gui.UIAnchorLayout(
            width=300, height=400, size_hint=None))
        frame.with_padding(all=20)

        # Add a background to the window.
        # Nine patch smoothes the edges.
        frame.with_background(
            texture=arcade.gui.NinePatchTexture(
                left=7,
                right=7,
                bottom=7,
                top=7,
                texture=arcade.load_texture(
                    ":resources:gui_basic_assets/window/dark_blue_gray_panel.png"
                ),
            )
        )

        back_button = arcade.gui.UIFlatButton(text="Back", width=250)
        # The type of event listener we used earlier for the button will not work here.
        back_button.on_click = self.on_click_back_button

        title_label = arcade.gui.UILabel(
            text=title, align="center", font_size=20, multiline=False)
        # Adding some extra space around the title.
        title_label_space = arcade.gui.UISpace(
            height=30, color=arcade.color.DARK_BLUE_GRAY)

        input_text_widget = arcade.gui.UIInputText(
            text=input_text, width=250).with_border()

        # Load the on-off textures.
        on_texture = arcade.load_texture(
            ":resources:gui_basic_assets/simple_checkbox/circle_on.png"
        )
        off_texture = arcade.load_texture(
            ":resources:gui_basic_assets/simple_checkbox/circle_off.png"
        )

        # Create the on-off toggle and a label
        toggle_label = arcade.gui.UILabel(text=toggle_label)
        toggle = arcade.gui.UITextureToggle(
            on_texture=on_texture, off_texture=off_texture, width=20, height=20
        )

        # Align toggle and label horizontally next to each other
        toggle_group = arcade.gui.UIBoxLayout(vertical=False, space_between=5)
        toggle_group.add(toggle)
        toggle_group.add(toggle_label)

        # Create dropdown with a specified default.
        dropdown = arcade.gui.UIDropdown(
            default=dropdown_options[0], options=dropdown_options, height=20, width=250
        )

        slider_label = arcade.gui.UILabel(text=slider_label)
        pressed_style = arcade.gui.UISlider.UIStyle(
            filled_track=arcade.color.GREEN, unfilled_track=arcade.color.RED
        )
        default_style = arcade.gui.UISlider.UIStyle()
        style_dict = {
            "press": pressed_style,
            "normal": default_style,
            "hover": default_style,
            "disabled": default_style,
        }
        # Configuring the styles is optional.
        slider = arcade.gui.UISlider(value=50, width=250, style=style_dict)

        widget_layout = arcade.gui.UIBoxLayout(align="left", space_between=10)
        widget_layout.add(title_label)
        widget_layout.add(title_label_space)
        widget_layout.add(input_text_widget)
        widget_layout.add(toggle_group)
        widget_layout.add(dropdown)
        widget_layout.add(slider_label)
        widget_layout.add(slider)

        widget_layout.add(back_button)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="top")

    def on_click_back_button(self, event):
        # Removes the widget from the manager.
        # After this the manager will respond to its events like it previously did.
        self.parent.remove(self)


class Enemy(arcade.Sprite):
    def __init__(self, sprite: arcade.Sprite):
        super().__init__()

        self.facing_direction = RIGHT_FACING

        self.texture = sprite.texture

        self.center_x = sprite.center_x
        self.center_y = sprite.center_y
        self.scale = sprite.scale

        self.initial_center_x = self.center_x
        self.initial_center_y = self.center_y

        self.speed = 2


def main():
    """Main function"""
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    main_view = MainView()
    main_view.setup()
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main()
