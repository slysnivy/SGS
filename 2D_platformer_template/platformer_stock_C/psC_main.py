import os
import pickle
import pygame
import random
import math

DARK_RED = (139, 0, 0)
YELLOW = (235, 195, 65)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (30, 144, 255)
CYAN = (47, 237, 237)
RED = (194, 57, 33)
LIME_GREEN = (50, 205, 50)
LIGHT_RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (125, 125, 125)
LIGHT_PINK = (255, 182, 193)
DARK_GREEN = (1, 100, 32)
PURPLE = (181, 60, 177)
BROWN = (150, 75, 0)
DARK_GREY = (52, 52, 52)


class Text:
    """
    Class used to simplify text creation for pygame
    """

    def __init__(self, text, text_pos, font_size, font_type,
                 font_color, text_other):
        self.text = text  # Text as a string
        self.position = text_pos  # Text position as a tuple or list (x and y)
        self.font_size = int(font_size)  # Int determining how big the text is
        self.font_type = font_type  # String used to indicate what font
        """Font selection is determined by your computer and it's preset fonts
        """
        self.color = font_color
        """A constant string for a tuple or a tuple using RGB values"""
        self.other = text_other
        """PLACEHOLDER for any other variables needed or desired in text"""
        self.font = None  # Initialized here, defined in setup()
        self.text_rect = None  # Initialized here, defined in render()
        self.text_img = None  # Initialized here, defined in render()

        self.setup()  # Called to set up the font
        self.render()
        """Called to continuously update the position, rect, color, and text
        """

    def setup(self):
        """
        Uses font type and size to translate into pygame text font
        and to make self.font
        """
        self.font = pygame.font.SysFont(self.font_type, self.font_size)

    def render(self):
        """
        Creates self.text_img or the pygame image of the text using self.text,
            self.color.
        Creates self.text_rect, or a rect object using the size of the text.
        Then centers the rect around the text (or the defined position)
        """
        self.text_img = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_img.get_rect()
        self.text_rect.center = self.position

    def scale(self, width, height):
        self.position = list(self.position)
        self.position[0] = int(self.position[0] * width)
        self.position[1] = int(self.position[1] * height)
        self.position = tuple(self.position)
        self.font_size = int(self.font_size * max(width, height))

        # Apply those changes
        self.setup()
        self.render()


class Music:
    """
    Music class containing tracks available and the current music playing.
    Also responsible for music volume and music switching.
    """

    def __init__(self, perc_vol):
        self.music_tracks = []  # Put file_name for music here
        self.end = pygame.USEREVENT + 0  # Unique event, for when music ends
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 0)
        # Everytime music ends, return the event

        self.file_path = "put_file_path_for_music"  # File path for audio

        self.current_track_index = 0  # Everything but the main menu theme

        self.perc_vol = perc_vol  # Volume set by the player as a percentage
        self.music_vol = 0  # Adjustable music volume
        self.vol_time = pygame.time.get_ticks()  # Increment music with time
        self.max_vol = 1 * self.perc_vol / 100  # Max volume possible for music
        # Change 1 value for changing music

        """pygame.mixer.music.load(self.file_path + self.music_tracks[0])"""
        #   Load this music up upon loading

        pygame.mixer.music.set_volume(self.max_vol)  # Set to max for now
        # pygame.mixer.music.play(-1)   # Start with this song and play forever

        self.text_timer = pygame.time.get_ticks()
        # Display what's currently playing

    def switch_music(self):
        # Reset music display timer
        self.text_timer = pygame.time.get_ticks()

        # Choose a random track index
        self.music_vol = 0
        self.current_track_index = random.randint(1, len(self.music_tracks) - 2)
        # Set the boundaries between 2nd/1 and 2nd last/len - 2 to avoid
        # main menu and credits

        # Load the selected track
        pygame.mixer.music.load(self.file_path +
                                (self.music_tracks[self.current_track_index]))

        # Set the volume
        pygame.mixer.music.set_volume(self.music_vol)

        pygame.mixer.music.play(0, 0, 0)  # Play the music once

    def set_music(self, track_num, vol, loops, start, fade_in):
        # Set the max volume
        self.max_vol = 0.7 * self.perc_vol / 100

        # Reset music display timer
        self.text_timer = pygame.time.get_ticks()

        # Update the current track index
        self.current_track_index = track_num

        # Load the selected track
        pygame.mixer.music.load(self.file_path +
                                (self.music_tracks[self.current_track_index]))

        # Set the volume
        self.music_vol = vol * self.perc_vol / 100
        pygame.mixer.music.set_volume(self.music_vol)

        pygame.mixer.music.play(loops, start, fade_in)  # Play the music

    def transition_music(self):
        # Slowly increase volume of music (0.01 every 0.075 seconds)
        # until volume reaches the max (0.7 or self.max_vol)
        # set the new self.max_vol if changed
        self.max_vol = 0.7 * self.perc_vol / 100
        while self.music_vol < self.max_vol and \
                75 < pygame.time.get_ticks() - self.vol_time:
            self.music_vol += 0.01  # Increase volume
            pygame.mixer.music.set_volume(self.music_vol)  # Update volume
            self.vol_time = pygame.time.get_ticks()  # Reset timer


class Image:
    def __init__(self, folder, asset_name, x, y, img_width, img_height, img_id):
        self.img = pygame.image.load(folder + "/" + asset_name).convert_alpha()
        self.img_x = x
        self.img_y = y
        self.img_width = img_width
        self.img_height = img_height
        self.img_id = img_id

        self.render_id = 0

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()


class Animate(Image):

    def __init__(self, file, asset_path, frame_delay, x, y, img_width, img_height, ani_id):
        Image.__init__(self, file, asset_path, x, y, img_width, img_height,
                       ani_id)

        self.img_rows = self.img.get_width() // self.img_width
        self.img_columns = self.img.get_height() // self.img_height

        self.img_frames = []

        self.frame_delay = frame_delay
        self.frame_time = 0

        self.len = 0

        self.ani_id = ani_id
        self.render_id = 1

        for y in range(self.img_columns):
            for x in range(self.img_rows):
                img_rect = pygame.Rect(x * self.img_width,
                                       y * self.img_height,
                                       self.img_width,
                                       self.img_height)
                img_rect.center = (self.img_x, self.img_y)
                self.img.set_clip(pygame.Rect(x * self.img_width,
                                              y * self.img_height,
                                              self.img_width,
                                              self.img_height))
                self.img_frames += [
                    self.img.subsurface(self.img.get_clip())]
                self.len += 1

        self.img_index = random.randint(0, self.len - 1)

    def update_render(self):
        if self.frame_delay < pygame.time.get_ticks() - self.frame_time:
            self.change_frame()
            self.frame_time = pygame.time.get_ticks()

    def change_frame(self):
        if self.img_index < self.len - 1:
            self.img_index += 1
        else:
            self.img_index = 0

    def render(self, screen, rect):
        screen.blit(self.img_frames[self.img_index], rect)


class Background(Animate):
    def __init__(self, file, asset_path, frame_delay, transparency, pf, x, y, img_width, img_height, bg_id):
        Animate.__init__(self, file, asset_path, frame_delay, x, y, img_width, img_height, bg_id)

        self.bg_id = bg_id
        self.transparency = transparency

        self.set_transparency()

        self.parallax_x = 0
        self.x_offset = 0
        self.parallax_y = 0
        self.y_offset = 0

        # How many in game units would it take to scroll the background
        self.parallax_factor = pf

    def set_transparency(self):
        for each_frame in self.img_frames:
            each_frame.set_alpha(self.transparency)

    def bg_pos_x(self, move_x):
        self.parallax_x += move_x
        if self.parallax_factor < self.parallax_x:
            self.x_offset += 1
            self.parallax_x = 0
        elif self.parallax_x < self.parallax_factor * -1:
            self.x_offset -= 1
            self.parallax_x = 0

    def bg_pos_y(self, move_y):
        self.parallax_y += move_y
        if self.parallax_factor < self.parallax_y:
            self.y_offset += 1
            self.parallax_y = 0
        elif self.parallax_y < self.parallax_factor * -1:
            self.y_offset -= 1
            self.parallax_y = 0

    def update_render(self):
        if self.frame_delay < pygame.time.get_ticks() - self.frame_time:
            self.change_frame()
            self.frame_time = pygame.time.get_ticks()

    def change_frame(self):
        if self.img_index < self.len - 1:
            self.img_index += 1
        else:
            self.img_index = 0

    def render(self, screen, pos):
        screen.blit(self.img_frames[self.img_index], (pos[0] + self.x_offset,
                                                      pos[1] + self.y_offset))


class Memory:
    """
    Class used to store, load, and save data across game instances
    """

    def __init__(self):
        self.res_width = 0
        self.res_height = 0
        self.music = None
        self.screen = None
        self.loaded = None

    def save_data(self, out_path, save_name):
        """ Save a single object to the pickle file"""
        with open(out_path + save_name, "wb") as game_file:
            self.compile_rect()
            pickle.dump(self.loaded, game_file)

    def load_data(self, in_path, save_name):
        """ Load one object from a preset pickle file. Files are
        usually modified or added to using the save_data
        function in this class"""
        if len(os.listdir(in_path)) < 1 or save_name not in os.listdir(in_path):
            self.loaded = []
        else:
            with open(in_path + save_name, "rb") as game_file:
                self.loaded = pickle.load(game_file)
                self.decompile_rect()

    def get_scene(self, in_path):
        """ Get specific level order from folder names"""
        self.loaded = []
        for level_name in os.listdir(in_path):
            self.loaded += [int(level_name.split("_")[-1])]

    def load_scene(self, in_path):
        """ Load a scene from a pickle file"""
        pass

    def load_image(self, in_path):
        """ Load images from a file path. These images are
        usually used to blit over existing Rects. Therefore,
        the x and y parameters are left at 0."""
        self.loaded = []
        for each_image in os.listdir(in_path):
            img_id = int(str(each_image).split("_")[1][:-4])
            in_img = Image(in_path, each_image,
                           0, 0, 0, 0, img_id)
            in_img.img_width = in_img.get_width()
            in_img.img_height = in_img.get_height()
            self.loaded += [in_img]

    def load_animation(self, in_path):
        """ Load animations from a file path. Files must be
        in the form of a spritesheet to use this method.
        The width and height must be specified for each animation asset
        in the file name. Spritesheet file names will follow this naming
        convention: FILENAME_ID_FRAMEDELAY_WIDTH_HEIGHT"""
        self.loaded = []
        def_x, def_y = 0, 0
        for each_image in os.listdir(in_path):
            in_img = each_image.split("_")
            ani_id = int(in_img[1])
            frame_delay = int(in_img[2])
            width = int(in_img[3])
            height = int(in_img[4].split(".")[0])
            in_ani = Animate(in_path, each_image, frame_delay,
                             def_x, def_y, width, height, ani_id)
            self.loaded += [in_ani]

    def load_bg(self, in_path):
        """ Load animated backgrounds from a file path. Files must be
                in the form of a spritesheet to use this method.
                The width and height must be specified for each animation asset
                in the file name. Spritesheet file names will follow this naming
                convention: FILENAME_ID_FRAMEDELAY_TRANSPARENCY_PARALLAXFACTOR_WIDTH_HEIGHT"""
        self.loaded = []
        def_x, def_y = 0, 0
        for each_image in os.listdir(in_path):
            in_img = each_image.split("_")
            bg_id = int(in_img[1])
            frame_delay = int(in_img[2])
            transparency = int(in_img[3])
            pf = int(in_img[4])
            width = int(in_img[5])
            height = int(in_img[6].split(".")[0])
            in_ani = Background(in_path, each_image, frame_delay, transparency,
                                pf, def_x, def_y, width, height, bg_id)
            self.loaded += [in_ani]

    def default_load(self, in_path, save_name):
        """ Default loading for built-in python types"""
        if len(os.listdir(in_path)) < 1 or save_name not in os.listdir(in_path):
            self.loaded = []
        else:
            with open(in_path + save_name, "rb") as game_file:
                self.loaded = pickle.load(game_file)

    def default_save(self, out_path, save_name):
        """ Default saving for built-in python types"""
        with open(out_path + save_name, "wb") as game_file:
            pickle.dump(self.loaded, game_file)

    def compile_rect(self):
        """ Converts self.loaded into a list of lists containing rect
        parameters. self.loaded must contain Rects"""
        foo_list = []
        # Check if list is empty. Then check if list is all rects:
        if len(self.loaded) < 1 or \
                type(self.loaded[0]) is not pygame.Rect or \
                type(self.loaded[-1]) is not pygame.Rect:
            return None

        for each_rect in self.loaded:
            if type(each_rect) is not pygame.Rect:
                # Check if any element in the list is not a rect
                return None
            foo_list += [[each_rect.x,
                          each_rect.y,
                          each_rect.width,
                          each_rect.height]]

        # All objects in loaded are rects, convert self.loaded
        self.loaded = foo_list

    def decompile_rect(self):
        if self.loaded is None or len(self.loaded) < 1:
            self.loaded = []
            return None

        foo_list = []
        for each_rect in self.loaded:
            if len(each_rect) != 4:
                # Put error handling here
                self.loaded = []
                return None
            foo_list += [pygame.Rect(each_rect[0],
                                     each_rect[1],
                                     each_rect[2],
                                     each_rect[3])]
        self.loaded = foo_list


class Scene:
    """
    Class template for creating scene based games
    """

    def __init__(self):
        """
        self.this_scene will tell the current scene it's on at that moment.
        Currently, it's set to itself, which means the
        current scene is this one.
        """
        self.this_scene = self
        self.run_scene = True
        self.level_id = -1

    def input(self, pressed, held):
        # this will be overridden in subclasses
        """
        This function should contain the pressed for loop and other held
        buttons. Pressing or holding these buttons should cause something
        to change such as a class variable (+= 1, True/False, change str.. etc.)
        or call another function.

        :param pressed: Detect buttons that are pressed (like if held, it will
        only be updated with the initial press)
        :param held: Detect buttons that are held down
        :return:
        """
        pass

    def update(self):
        # this will be overridden in subclasses
        """
        This function should check for variables that need to be updated
        continuously. A good way to distinguish this from input is that this
        update function doesn't directly respond from a button press. For
        example, let's have input add to self.x by 1, or self.x += 1. Then, if
        we wanted to keep self.x within the bounds of 0 to 10, we check for that
        in update. In update, we'd use if self.x < 0 and 10 < self.x to check
        whenever self.x goes out of these bounds to then reset self.x.

        :return:
        """
        pass

    def render(self, screen):
        # this will be overridden in subclasses
        """
        This function is solely used for rendering purposes such as
        screen.blit or pygame.draw
        :param screen:
        :return:
        """
        pass

    def change_scene(self, next_scene):
        """
        This function is used in the main pygame loop. This function is
        responsible for formally changing the scene
        """
        self.this_scene = next_scene

    def close_game(self):
        """
        Set the current scene to nothing and is used to stop the game.
        This function is responsible for ending the game loop (or scene)
        formally.
        """
        self.change_scene(None)


class PlayLevel(Scene):

    def __init__(self, x_spawn, y_spawn, width, height, lv_id):
        """
        Set the current scene to this scene by passing this classes self to
        initialize it.
        """
        Scene.__init__(self)
        # Put pygame objects that need rendering into here
        self.platforms = []  # All platforms for that level (collision)
        self.death_zones = []  # All deaths for that level (death condition)
        self.win_zones = []  # All win areas for that level (win condition)
        self.respawn_zones = []  # Respawn area for the player
        self.invis_rect = pygame.Rect(x_spawn, y_spawn, 1, 1)   # rect comparing player position
        self.invis_rect.center = (x_spawn, y_spawn)

        # Render these objects
        self.render_objects = self.platforms + self.death_zones + \
                              self.win_zones + self.respawn_zones
        self.x_spawn = x_spawn  # x player spawn
        self.y_spawn = y_spawn  # y player spawn
        self.player = Player(self.x_spawn, self.y_spawn,
                             10, 10, PURPLE,
                             width,
                             height, 100)

        self.level_id = lv_id
        """Initialize player variable in the level using the x and y spawn,
        constant widths and heights of 10, the color PURPLE, and the difficulty
        defined by level_memory (settings dependent)
        """
        self.y_border = -1000  # How far the player can go past the y bounds
        self.deaths = 0  # Recorded deaths for that level instance
        self.play_time = 0  # Time accumulated in that level
        self.level_condition = False  # Check if player has won (touch win)

        # Text displayed when winning (touch the win_zones), uses time/counter

        self.pause_text = Text("PAUSED", (width / 2, 1 * (height / 10)),
                               100, "impact", DARK_RED, None)
        self.pause_text_2 = Text("Press esc to unpause", (width / 2, 3 * (height / 10)),
                                 30, "impact", DARK_RED, None)
        self.pause_text_3 = Text("Press q to quit", (width / 2, 5 * (height / 10)),
                                 30, "impact", DARK_RED, None)
        self.pause_text_4 = Text("Press b to return to menu",
                                 (width / 2, 7 * (height / 10)), 30,
                                 "impact", DARK_RED, None)
        self.pause_text_5 = Text("Press r to restart the level",
                                 (width / 2, 9 * (height / 10)), 30,
                                 "impact", DARK_RED, None)
        # Text displayed when player pauses the game (ESC)

        # Timer used to delay player jump
        self.jump_timer = pygame.time.get_ticks()

        self.res_height = height
        self.res_width = width

        self.held_delay = pygame.time.get_ticks()

        self.memory_win_warp = Memory()
        self.memory_win_warp.default_load("game_files/game_data/lv_" + str(self.level_id) + "/", "save_level")
        self.level_memory = self.memory_win_warp.loaded

        self.memory_plat = Memory()
        self.memory_plat.load_data("game_files/game_data/lv_" + str(self.level_id) + "/", "save_plat")
        self.platforms = self.memory_plat.loaded

        self.memory_win = Memory()
        self.memory_win.load_data("game_files/game_data/lv_" + str(self.level_id) + "/", "save_win")
        self.win_zones = self.memory_win.loaded

        self.memory_death = Memory()
        self.memory_death.load_data("game_files/game_data/lv_" + str(self.level_id) + "/",
                                    "save_death")
        self.death_zones = self.memory_death.loaded

        self.memory_respawn = Memory()
        self.memory_respawn.load_data("game_files/game_data/lv_" + str(self.level_id) + "/",
                                      "save_respawn")
        self.respawn_zones = self.memory_respawn.loaded

        self.memory_decor = Memory()
        self.memory_decor.load_data("game_files/game_data/lv_" + str(self.level_id) + "/",
                                    "save_decor")
        self.decorations = self.memory_decor.loaded

        self.memory_img = Memory()
        self.memory_img.load_image("game_files/psC_imgs")

        self.memory_ani = Memory()
        self.memory_ani.load_animation("game_files/psC_ani")

        self.memory_bg = Memory()
        self.memory_bg.load_bg("game_files/psC_bg")

        self.memory_asset_id = Memory()
        self.memory_asset_id.default_load("game_files/game_data/lv_" + str(self.level_id) + "/",
                                        "save_asset")

        self.memory_asset_type = Memory()
        self.memory_asset_type.default_load("game_files/game_data/lv_" + str(self.level_id) + "/",
                                        "save_asset_id")

        self.memory_bg_id = Memory()
        self.memory_bg_id.default_load("game_files/game_data/lv_" + str(self.level_id) + "/",
                                        "save_bg")

        if not self.memory_bg or not self.memory_bg_id.loaded:
            self.scene_bg = self.memory_bg.loaded[0]
        else:
            self.scene_bg = self.memory_bg.loaded[self.memory_bg_id.loaded]

        if self.memory_asset_id.loaded is None or \
                self.memory_asset_id.loaded == []:
            self.memory_asset_id.loaded = {
                0: [],
                1: [],
                2: [],
                3: [],
                4: []
            }

        if self.memory_asset_type.loaded is None or \
                self.memory_asset_type.loaded == []:
            self.memory_asset_type.loaded = {
                0: [],
                1: [],
                2: [],
                3: [],
                4: []
            }

        # Put all level elements into a single dictionary
        self.element = {
            0: self.platforms,
            1: self.win_zones,
            2: self.death_zones,
            3: self.respawn_zones,
            4: self.decorations
        }

    def input(self, pressed, held):
        for every_key in pressed:
            # Player movement bound to the middle of the screen
            if every_key is pygame.K_a and not self.player.disable_left and \
                    not self.player.freeze and \
                    self.player.alive:
                move_left = self.player.smart_left(self.platforms)
                self.update_plat_x(move_left)
                self.scene_bg.bg_pos_x(move_left)
            if every_key is pygame.K_d and not self.player.disable_right and \
                    not self.player.freeze and \
                    self.player.alive:
                move_right = self.player.smart_right(self.platforms)
                self.update_plat_x(move_right)
                self.scene_bg.bg_pos_y(move_right)

            # Pressing/tapping and not holding jump key to jump
            if every_key in [pygame.K_w, pygame.K_UP, pygame.K_SPACE] and not \
                    self.player.enable_gravity and \
                    self.player.alive and not \
                    self.player.freeze and \
                    150 <= pygame.time.get_ticks() - self.jump_timer:
                self.player.jump_ability = True  # Allow player to jump
                self.player.jump_boost = self.player.max_jump  # Setup jump
                # self.player.jump_sound_1.play()  # Play jump sound
                self.player.jumps += 1  # Add to a jump counter
                self.jump_timer = pygame.time.get_ticks()  # Reset jump timer

            # Pressing the jump key to stop player freezing and start level
            # This also updates the replay linked list
            if every_key in [pygame.K_w, pygame.K_UP, pygame.K_SPACE] \
                    and not self.player.alive:
                self.player.alive = True
                self.jump_timer = pygame.time.get_ticks()

            # Pausing the game and stopping player movement/action
            if every_key == pygame.K_ESCAPE and not self.level_condition:
                self.player.freeze = not self.player.freeze

            # If paused, press q to quit
            if every_key == pygame.K_q and self.player.freeze:
                self.run_scene = False

            # Restart the level from pause menu, which counts as a death
            if self.player.freeze and every_key == pygame.K_r:
                self.player.alive = False
                self.player.freeze = False
                self.deaths += 1
            # Press b to go back to main menu
            if self.player.freeze and every_key == pygame.K_b:
                self.change_scene(Scene())

        # Held controls for jumping
        if (held[pygame.K_SPACE] or held[pygame.K_w] or held[pygame.K_UP]) \
                and not self.player.enable_gravity and \
                self.player.alive and \
                not self.player.freeze and \
                150 <= pygame.time.get_ticks() - self.jump_timer:
            self.player.jump_ability = True  # Allow player to jump
            self.player.jump_boost = -1 * self.player.max_jump  # Setup jump
            # self.player.jump_sound_1.play()  # Play jump sound
            self.player.jumps += 1  # Add to a jump counter
            self.jump_timer = pygame.time.get_ticks()  # Reset jump timer

        if held[pygame.K_a] and \
                10 < pygame.time.get_ticks() - self.held_delay and \
                not self.player.disable_left and not self.player.freeze and \
                self.player.alive:
            move_left = self.player.smart_left(self.platforms)
            self.update_plat_x(move_left)
            self.scene_bg.bg_pos_x(move_left)
            self.held_delay = pygame.time.get_ticks()
        if held[pygame.K_d] and \
                10 < pygame.time.get_ticks() - self.held_delay and \
                not self.player.disable_right and not self.player.freeze and \
                self.player.alive:
            move_right = self.player.smart_right(self.platforms)
            self.update_plat_x(move_right)
            self.scene_bg.bg_pos_x(move_right)
            self.held_delay = pygame.time.get_ticks()

    def update(self):
        # Failsafe if player isn't rendered but level starts
        if self.player.square_render is None:
            return None  # Player is not rendered, skip function

        grav_y = self.player.gravity()
        self.update_plat_y(grav_y)
        self.scene_bg.bg_pos_y(grav_y)

        jump_y = self.player.jump()
        self.update_plat_y(jump_y)
        self.scene_bg.bg_pos_y(jump_y)

        # Player is alive, not paused and haven't run, then check collision
        if self.player.alive and not self.player.freeze and \
                not self.level_condition:
            # Check if player collided with death zones (returns 1 or 0)
            if 0 < self.player.death(self.death_zones):
                self.deaths += 1
                self.reload()
            else:
                self.player.collision_plat(
                    self.platforms)  # Top and bottom coll
                self.player.collision_wall(self.platforms)
                self.player.update_detection()  # Player movement

        """Respawn for square players, reset spawn position, set direction
        to right by default, reset gravity"""
        if not self.player.alive and not self.player.freeze and \
                not self.level_condition:
            self.jump_timer = pygame.time.get_ticks()  # Reset jump timer
            self.player.jump_boost = -1 * (self.player.max_jump - 1)
            self.player.jump_ability = False

        # If player is below the level, count as a death (out of bounds)
        if self.invis_rect.y < self.y_border:
            self.player.alive = False
            self.player.enable_gravity = False
            self.deaths += 1
            self.reload()

        # Check for win collision
        if self.player.alive and \
                self.player.square_render.collidelist(self.win_zones) != -1:
            self.level_condition = True
            self.player.alive = False
            next_index = self.player.square_render.collidelist(self.win_zones)
            self.next_level(self.memory_win_warp.loaded[next_index])

        # Respawn block collision
        if self.player.alive and \
                self.player.square_render.collidelist(self.respawn_zones) != -1:
            # Setup respawn block for readability
            respawn_block = self.player.square_render.collidelist(
                self.respawn_zones)
            # Set new x and y default spawns
            self.x_spawn = self.respawn_zones[respawn_block].x + (
                    self.respawn_zones[respawn_block].width / 2) - 5
            self.y_spawn = self.respawn_zones[respawn_block].y + (
                    self.respawn_zones[respawn_block].height / 2) - 5

    def next_level(self, lv_id):
        all_levels = Memory()
        all_levels.get_scene("game_files/game_data/")
        self.change_scene(PlayLevel(self.x_spawn, self.y_spawn,
                                    self.res_width, self.res_height,
                                    int(all_levels.loaded[lv_id])))

    def victory(self, screen):
        # Victory function played when win condition
        pass

    def render(self, screen):
        # Default rendering
        self.render_bg(screen)

        self.render_level(screen)
        self.player.render(screen)
        self.render_text(screen)

    def update_plat_x(self, move_x):
        self.invis_rect.x += move_x
        for plat in self.platforms + self.win_zones + \
                    self.death_zones + self.respawn_zones + \
                    self.decorations:
            plat.x += move_x

    def update_plat_y(self, move_y):
        if move_y is not None:
            self.invis_rect.y += int(move_y)
            for plat in self.platforms + self.win_zones + \
                        self.death_zones + self.respawn_zones + \
                        self.decorations:
                plat.y += int(move_y)

    def render_level(self, screen):
        """ This function will be altered in the child class"""
        for each_id in self.element:
            for obj_ind in range(len(self.element[each_id])):
                plat = self.element[each_id][obj_ind]
                if (0 <= plat.x + plat.width <= game_width or
                    0 <= plat.x <= game_width) and \
                        (0 <= plat.y + plat.height <= game_height or
                         0 <= plat.y <= game_height):
                    render_id = self.memory_asset_id.loaded[each_id][obj_ind]
                    render_type = self.memory_asset_type.loaded[each_id][
                        obj_ind]
                    if render_type == 0:
                        screen.blit(self.memory_img.loaded[render_id].img, plat)
                    else:
                        self.memory_ani.loaded[render_id].update_render()
                        self.memory_ani.loaded[render_id].render(screen, plat)

    def render_text(self, screen):
        """ Use this function to render important text for levels"""
        self.player.render(screen)

        if self.player.freeze:
            screen.blit(self.pause_text.text_img,
                        self.pause_text.text_rect)  # big bold for pausing
            screen.blit(self.pause_text_2.text_img,
                        self.pause_text_2.text_rect)  # instructions to unpause
            screen.blit(self.pause_text_3.text_img,
                        self.pause_text_3.text_rect)  # drawing quitting text
            # adding quitting thing draw here as well
            screen.blit(self.pause_text_4.text_img,
                        self.pause_text_4.text_rect)
            # added a way to formally return to the main menu
            screen.blit(self.pause_text_5.text_img,
                        self.pause_text_5.text_rect)

    def render_bg(self, screen):
        screen.fill(WHITE)
        if 0 <= len(self.memory_bg_id.loaded):
            self.scene_bg.update_render()
            self.scene_bg.render(screen, (
            (self.res_width - self.scene_bg.img_width) / 2,
            (self.res_height - self.scene_bg.img_height) / 2))

    def reload(self):
        self.change_scene(PlayLevel(self.x_spawn, self.y_spawn,
                                    self.res_width, self.res_height,
                                    self.level_id))


class Player:

    def __init__(self, x_spawn, y_spawn, width, height, rgb,
                 res_width, res_height, jump_vol):
        """
        self.square parameters: [
        [x_spawn, y_spawn],
        [width, height]
        [RGB value],
        difficuty_value
        ]
        """
        self.xpos = x_spawn  # Current x_position, initialized as spawn
        self.ypos = y_spawn  # Current y_position, initialized as spawn
        self.width = width  # Current width
        self.height = height  # Current height
        self.color = rgb  # Color of player as static constant or tuple
        self.square_render = pygame.Rect(res_width / 2, res_height / 2,
                                         self.width,
                                         self.height)  # Rect of the player
        self.square_render.center = (self.xpos, self.ypos)

        self.alive = False  # If the player is alive (able to move)
        self.freeze = False  # If the player is forced to pause

        self.jumps = 0  # Amount of jumps the player had done (remove)
        self.jump_ability = False  # If the player is able to jump
        self.enable_gravity = True  # If gravity is acting on the player
        self.max_jump = 50  # Limit for the jump loop to iterate
        self.jump_boost = -1 * (self.max_jump - 1)  # Counter for jump loop
        self.max_gravity = 95  # Limit for the gravity loop to iterate
        self.gravity_counter = self.max_gravity  # Counter for gravity loop

        asset_path = "assets/"
        # self.jump_sound_1 = pygame.mixer.Sound(sound_path + "jump_file")
        # Jump sound for player
        # self.jump_sound_1.set_volume(0.1 * (jump_vol / 100))  # out of 1 or 100%
        # Jump volume for the player, set at 0.1 out of 1, or 10%

        # Get location and info of surrounding blocks
        self.size_factor = 5    # Increase to have better detection
        self.collide_rect = pygame.Rect(self.xpos - self.width,
                                        self.ypos - self.height,
                                        self.width * 3 * self.size_factor,
                                        self.height * 3 * self.size_factor)
        self.collide_rect.center = (self.xpos, self.ypos)
        # Top, bottom, left and right collision
        self.left_col = pygame.Rect(self.xpos - self.width,
                                    self.ypos,
                                    self.width,
                                    self.height)
        self.left_col.center = (self.xpos - self.width * self.size_factor, self.ypos)
        self.left_col.width *= self.size_factor
        self.right_col = pygame.Rect(self.xpos + self.width,
                                     self.ypos,
                                     self.width,
                                     self.height)
        self.right_col.center = (self.xpos + self.width, self.ypos)
        self.right_col.width *= self.size_factor
        self.top_col = pygame.Rect(self.xpos,
                                   self.ypos - self.height,
                                   self.width,
                                   self.height)
        self.top_col.center = (self.xpos, self.ypos - self.height * self.size_factor)
        self.top_col.height *= self.size_factor
        self.bot_col = pygame.Rect(self.xpos,
                                   self.ypos + self.height,
                                   self.width,
                                   self.height)
        self.bot_col.center = (self.xpos, self.ypos + self.height)
        self.bot_col.height *= self.size_factor

        self.res_width = res_width
        self.res_height = res_height

        """One single larger rect for collision detection
        """
        self.grav_y = None
        self.jump_y = None
        self.left_x = None
        self.right_x = None

        self.disable_left = False
        self.disable_right = False
        self.corner_flag = False

    def update_detection(self):
        """
        Move the player by 4 units in the specific direction, multiplied
        by the difficulty factor (max of 1 usually)
        """
        # Move horizontally depending on the direction

        # Update collision logic position in real time with the player position
        pass

    def jump(self):
        # Jump that will change the player's y position in the game loop
        # print(self.jump_ability, self.jump_boost)
        if not self.alive:
            return 0

        if self.jump_ability and 0 <= self.jump_boost:
            jump_factor = ((self.jump_boost ** 2) * 0.004)
            if self.jump_y is not None and \
                    (self.res_width / 2) - self.jump_y < jump_factor:
                self.jump_ability = False
                self.jump_boost = -1
                self.enable_gravity = True
                return 0
            else:
                """Change the y position based on the counter and difficulty. 
                This creates a parabolic relationship from being squared."""
                self.jump_boost -= 2
                """Decrease the counter until it reaches 0
                This is used to create the first arc of the jump"""
                return jump_factor
        else:
            """Crucial for the second half of the jump, 
            allowing the player to fall"""
            self.jump_ability = False
            return 0

    def render(self, screen):
        # Visualize collision rect, uncomment to see
        """pygame.draw.rect(screen, (55, 230, 50), self.collide_rect)   # area
        pygame.draw.rect(screen, BLUE, self.left_col)  # left
        pygame.draw.rect(screen, BLUE, self.right_col)  # right
        pygame.draw.rect(screen, BLUE, self.top_col)  # top
        pygame.draw.rect(screen, BLUE, self.bot_col)  # bottom"""

        pygame.draw.rect(screen, self.color, self.square_render)
        # Update the square render/rect with the position (x and y)

    def collision_plat(self, object_list: [pygame.Rect]):
        # in reserve:
        """self.gravity()
        self.jump()"""
        # Get all the colliding rects with the bottom rect
        bot_collisions = self.collide_rect.collidelistall(object_list)

        """By default, set gravity to be true (we don't know if the player is on
        the ground or in the air)
        """
        all_y = []
        self.corner_flag = False
        self.enable_gravity = True
        for bcollide_id in bot_collisions:
            collide_y = object_list[bcollide_id].y
            if self.ypos + (self.height / 2) < collide_y and \
                    self.bot_col.colliderect(object_list[bcollide_id]) and not \
                    self.left_col.colliderect(object_list[bcollide_id]) and \
                    not self.right_col.colliderect(object_list[bcollide_id]):
                all_y += [collide_y]

            if (self.ypos + (self.height / 2) == collide_y or
                self.square_render.colliderect(object_list[bcollide_id])) and \
                    self.bot_col.colliderect(object_list[bcollide_id]) and not \
                    self.left_col.colliderect(object_list[bcollide_id]) and \
                    not self.right_col.colliderect(object_list[bcollide_id]):
                # If true, disable/reset gravity, enable jump
                self.enable_gravity = False
                self.jump_ability = True
                self.gravity_counter = self.max_gravity

            # Corner Detection
            if self.bot_col.colliderect(object_list[bcollide_id]) and \
                    (self.left_col.colliderect(object_list[bcollide_id]) or
                     self.right_col.colliderect(object_list[bcollide_id])):
                self.corner_flag = True

        if 0 < len(all_y):
            self.grav_y = min(all_y)
        else:
            self.grav_y = None

        all_yheight = []
        # Top ceiling collision
        top_collisions = self.collide_rect.collidelistall(object_list)
        for tcollide_id in top_collisions:
            collide_x = object_list[tcollide_id].x
            collide_y = object_list[tcollide_id].y
            collide_width = object_list[tcollide_id].width
            collide_height = object_list[tcollide_id].height

            if self.top_col.colliderect(object_list[tcollide_id]) and not \
                    self.left_col.colliderect(object_list[tcollide_id]) and \
                    not self.right_col.colliderect(object_list[tcollide_id]) \
                    and collide_y + collide_height < self.ypos - (
                    self.height / 2):
                all_yheight += [collide_y + collide_height]

            if (self.square_render.colliderect(object_list[tcollide_id]) or
                    (self.ypos - (
                            self.height / 2) == collide_y + collide_height) and
                    self.top_col.colliderect(object_list[tcollide_id]) and not
                    self.left_col.colliderect(object_list[tcollide_id]) and
                    not self.right_col.colliderect(object_list[tcollide_id])):
                self.jump_ability = False
                self.jump_boost = -1
                self.enable_gravity = True

        if 0 < len(all_yheight):
            self.jump_y = max(all_yheight)
        else:
            self.jump_y = None

    def collision_wall(self, object_list: [pygame.Rect]):
        self.disable_left = False
        self.disable_right = False

        # New collision logic:
        left_collision = self.collide_rect.collidelistall(object_list)
        right_collision = self.collide_rect.collidelistall(object_list)

        self.left_collision(object_list, left_collision)
        self.right_collision(object_list, right_collision)

    def smart_left(self, object_list):
        left_collision = self.collide_rect.collidelistall(object_list)
        return self.left_collision(object_list, left_collision)

    def smart_right(self, object_list):
        right_collision = self.collide_rect.collidelistall(object_list)
        return self.right_collision(object_list, right_collision)

    def left_collision(self, object_list, left_collision):
        all_xl = []
        # Left side collision, going left to turn right
        for lcollide_id in left_collision:
            collide_x = object_list[lcollide_id].x
            collide_y = object_list[lcollide_id].y
            collide_width = object_list[lcollide_id].width
            collide_height = object_list[lcollide_id].height

            if self.left_col.colliderect(object_list[lcollide_id]) and \
                    not self.top_col.colliderect(object_list[lcollide_id]) and \
                    not self.bot_col.colliderect(object_list[lcollide_id]) and \
                    collide_x + collide_width < self.xpos - self.width / 2:
                all_xl += [collide_x + collide_width]

            if lcollide_id != -1 and \
                    self.left_col.colliderect(object_list[lcollide_id]) and \
                    ((collide_x + collide_width) -
                     (self.xpos - (self.width / 2))) * -1 < 4:
                self.disable_left = True
                return ((collide_x + collide_width) -
                        (self.xpos - (self.width / 2))) * -1
            if lcollide_id != -1 and self.xpos - (
                    self.width / 2) <= collide_x + collide_width and \
                    self.left_col.colliderect(object_list[lcollide_id]) and \
                    collide_y < self.ypos + (self.height / 2) and \
                    self.ypos - (self.height / 2) < collide_y + collide_height:
                self.disable_left = True

        if 0 < len(all_xl):
            self.left_x = max(all_xl)
        else:
            self.left_x = None

        return 4

    def right_collision(self, object_list, right_collision):
        all_xr = []
        # Right side collision, going right to turn left
        for rcollide_id in right_collision:
            collide_x = object_list[rcollide_id].x
            collide_y = object_list[rcollide_id].y
            collide_width = object_list[rcollide_id].width
            collide_height = object_list[rcollide_id].height

            if self.right_col.colliderect(object_list[rcollide_id]) and \
                    not self.top_col.colliderect(object_list[rcollide_id]) and \
                    not self.bot_col.colliderect(object_list[rcollide_id]) and \
                    self.xpos + (self.width / 2) < collide_x:
                all_xr += [collide_x]

            if rcollide_id != -1 and \
                    self.right_col.colliderect(object_list[rcollide_id]) and \
                    -4 < self.xpos + (self.width / 2) - collide_x:
                self.disable_right = True
                return self.xpos + (self.width / 2) - collide_x
            if rcollide_id != -1 and collide_x < self.xpos + (
                    self.width / 2) and \
                    self.right_col.colliderect(object_list[rcollide_id]) and \
                    collide_y < self.ypos + (self.height / 2) and \
                    self.ypos - (self.height / 2) < collide_y + collide_height:
                self.disable_right = True

        if 0 < len(all_xr):
            self.right_x = min(all_xr)
        else:
            self.right_x = None

        return -4

    def gravity(self):
        if not self.alive:
            self.gravity_counter = self.max_gravity
            return 0

        if self.corner_flag:
            # set return for 0 for potential corner grab
            self.enable_gravity = False
            self.jump_ability = True
            self.gravity_counter = self.max_gravity
            return 1

        if self.enable_gravity and not self.jump_ability:
            gravity_y = ((self.gravity_counter ** 2) *
                         0.00015)
        else:
            gravity_y = 0

        if self.gravity_counter < 1100:
            self.gravity_counter += 2

        if self.enable_gravity and not self.jump_ability:
            if self.grav_y is not None and \
                    self.grav_y < gravity_y + self.ypos + (self.height / 2):
                self.enable_gravity = False
                self.jump_ability = True
                self.gravity_counter = self.max_gravity
                gravity_y = self.ypos + (self.height / 2) - (self.grav_y)
        if 0 < gravity_y:
            return gravity_y * -1
        elif gravity_y < 0:
            return gravity_y
        else:
            return 0

    def death(self, death_list: [pygame.Rect]):
        collide_id = self.square_render.collidelist(death_list)
        if collide_id != -1:
            self.alive = False
            return 1
        else:
            return 0


class Program:
    """
    Class responsible for how the game runs
    """

    def __init__(self) -> None:
        self.running = True  # Determines if the game is running
        # Initialize level/scene order from folders
        self.levels = Memory()
        self.levels.get_scene("game_files/game_data/")

    def run(self, width, height, current_scene):
        """
        Where the actual game loop is running.
        Everything game related is defined in scene.
        Scene is initialized by running Program (in main
        which is outer scope) with the screen size and scene.
        At this point in time, scene is run as MenuScene.

        Everything relating to calling the scene is called here, such as
        input, update, and render while the game is running.

        If the game isn't running, then in the final loop (or the loop when
        the game is told to close by various means), self.running is set to
        false and the scene is changed to nothing. Then the game is safe to
        close.

        This is also where inputs are collected before they are sent to
        the inputs for scene.

        Finally, this is where FPS is set and where the display is updated.
        """
        # self.memory.screen = pygame.display.set_mode([width, height])
        screen = pygame.display.set_mode([width, height])  # Set screen size

        scene = current_scene  # Set scene currently shown through a parameter
        # Start game loop
        while self.running:
            keys_pressed = []  # Keys pressed/tapped (key press)
            keys_held = pygame.key.get_pressed()  # Keys held collected
            for event in pygame.event.get():  # Collect all key presses
                # Quit condition if you press the X on the top right
                if event.type == pygame.QUIT:
                    # self.memory.write_save()
                    self.running = False  # Stop running this loop
                    pygame.mixer.music.stop()  # Stop the music
                    scene.run_scene = False  # Tell scene to stop running
                # If player does a keypress, append to our list for key presses
                if event.type == pygame.KEYDOWN:
                    keys_pressed.append(event.key)

                """if event.type == self.memory.music.end:
                    self.memory.music.switch_music()"""

            # Stop the game using other conditions (running, but scene says off)
            if self.running and not scene.run_scene:
                # self.memory.write_save()
                self.running = False  # Stop running this loop
                pygame.mixer.music.stop()  # Stop the music
                scene.close_game()  # Tell scene to shut off
            else:
                # Functional game loop

                scene.input(keys_pressed, keys_held)  # Call to use keys in
                scene.update()  # Call to dynamically use/update/check changes
                scene.render(screen)  # Visually render desired graphics
                scene = scene.this_scene
                """This line is important to allow changing scenes (if
                this_scene is different like using
                scene.change_scene(next_scene). Otherwise, scene will not be
                changed and will continue being this scene (same memory
                address, no change)."""

                """if 0 != scene.level_id:
                    self.memory.music.transition_music()"""

            fps.tick(120)  # 120 frames per second
            pygame.display.update()  # Update the visual output dynamically


if __name__ == "__main__":
    pygame.init()  # Initialize pygame
    pygame.mixer.init()  # Initialize pygame's sound

    fps = pygame.time.Clock()  # Initialize the frame rate

    # Alter these values to change the resolution
    game_width = 1080
    game_height = 576

    pygame.display.set_mode([game_width, game_height])

    file_path = "put_icon_file_path_here"
    """pygame.display.set_caption("display_window") # game window caption
    icon = pygame.image.load(file_path + "file_image_name") # loading image
    default_icon_image_size = (32, 32) # reducing size of image
    icon = pygame.transform.scale(icon, default_icon_image_size)
    # scaling image correctly
    pygame.display.set_icon(icon) # game window icon"""

    start_game = Program()  # Initialize running the game with Program
    start_scene = PlayLevel(game_width / 2,
                            game_height / 2,
                            game_width, game_height,
                            start_game.levels.loaded[0])
    # Initialize the first scene/starting scene shown to the player
    start_game.run(game_width, game_height, start_scene)  # Run the game loop
    """The game loop will be stuck at this line (start_game.run) until the
    while loop (while self.running:) is no longer true. When self.running is
    False, the program will move onto the next line to quit"""

    pygame.quit()  # Quit the game/pygame instance
