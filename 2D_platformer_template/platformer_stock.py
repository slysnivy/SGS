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

        self.music_text = Text("PLAYING: " +
                               str(self.music_tracks[self.current_track_index]),
                               (1080 / 2, 556), 20, "impact", WHITE, None)
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

        # Update the music display text
        self.music_text = Text("PLAYING: " +
                               str(self.music_tracks[self.current_track_index]),
                               (1080 / 2, 556), 20, "impact", WHITE, None)

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

        # Update the music display text
        self.music_text = Text("PLAYING: " +
                               str(self.music_tracks[self.current_track_index]),
                               (1080 / 2, 556), 20, "impact", WHITE, None)

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

    def __init__(self, x_spawn, y_spawn, width, height):
        """
        Set the current scene to this scene by passing this classes self to
        initialize it.
        """
        Scene.__init__(self)
        # Put pygame objects that need rendering into here
        self.platforms = [
                        pygame.Rect(0, 566, 1080, 10),
                        pygame.Rect(510, 544, 60, 22)
            ]  # All platforms for that level (collision)
        self.death_zones = []  # All deaths for that level (death condition)
        self.win_zones = []  # All win areas for that level (win condition)
        self.respawn_zones = []  # Respawn area for the player

        # Render these objects
        self.render_objects = self.platforms + self.death_zones + \
                                self.win_zones + self.respawn_zones

        self.x_spawn = x_spawn * width  # x player spawn
        self.y_spawn = y_spawn * height  # y player spawn
        self.player = Player(self.x_spawn, self.y_spawn,
                             10, 10, PURPLE,
                             width,
                             height, 100)
        """Initialize player variable in the level using the x and y spawn,
        constant widths and heights of 10, the color PURPLE, and the difficulty
        defined by level_memory (settings dependent)
        """
        self.deaths = 0  # Recorded deaths for that level instance
        self.play_time = 0  # Time accumulated in that level
        self.level_condition = False  # Check if player has won (touch win)

        # Text displayed when winning (touch the win_zones), uses time/counter

        self.pause_text = Text("PAUSED", (540, 213),
                               100, "impact", DARK_RED, None)
        self.pause_text.scale(width, height)
        self.pause_text_2 = Text("Press esc to unpause", (540, 280),
                                 30, "impact", DARK_RED, None)
        self.pause_text_2.scale(width, height)
        self.pause_text_3 = Text("Press q to quit", (540, 315),
                                 30, "impact", DARK_RED, None)
        self.pause_text_3.scale(width, height)
        self.pause_text_4 = Text("Press b to return to menu",
                                 (540, 350), 30,
                                 "impact", DARK_RED, None)
        self.pause_text_4.scale(width, height)
        self.pause_text_5 = Text("Press r to restart the level",
                                 (540, 385), 30,
                                 "impact", DARK_RED, None)
        self.pause_text_5.scale(width, height)
        # Text displayed when player pauses the game (ESC)

        # Timer used to delay player jump
        self.jump_timer = pygame.time.get_ticks()

        self.res_height = height
        self.res_width = width

    def input(self, pressed, held):
        for every_key in pressed:
            # Player movement bound to the middle of the screen
            if every_key is pygame.K_a:
                self.player.xpos += 4 * self.res_width
            if every_key is pygame.K_d:
                self.player.xpos -= 4 * self.res_width

            # Pressing/tapping and not holding jump key to jump
            if every_key in [pygame.K_w, pygame.K_UP, pygame.K_SPACE] and not \
                    self.player.enable_gravity and \
                    self.player.alive and not \
                    self.player.freeze and \
                    150 <= pygame.time.get_ticks() - self.jump_timer:
                self.player.jump_ability = True  # Allow player to jump
                self.player.jump_boost = self.player.max_jump  # Setup jump
                #self.player.jump_sound_1.play()  # Play jump sound
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
            self.player.jump_boost = self.player.max_jump  # Setup jump
            #self.player.jump_sound_1.play()  # Play jump sound
            self.player.jumps += 1  # Add to a jump counter
            self.jump_timer = pygame.time.get_ticks()  # Reset jump timer

        if held[pygame.K_a]:
            self.player.xpos += 4 * self.res_width
        if held[pygame.K_d]:
            self.player.xpos -= 4 * self.res_width

    def update(self):
        # Failsafe if player isn't rendered but level starts
        if self.player.square_render is None:
            return None  # Player is not rendered, skip function

        self.player.gravity()
        self.player.jump()

        # Player is alive, not paused and haven't run, then check collision
        if self.player.alive and not self.player.freeze and \
                not self.level_condition:
            # Check if player collided with death zones (returns 1 or 0)
            self.deaths += self.player.death(self.death_zones)
            self.player.collision_plat(self.platforms)  # Top and bottom coll
            self.player.collision_wall(self.platforms)  # Side collision
            self.player.update_detection()  # Player movement

        """Respawn for square players, reset spawn position, set direction
        to right by default, reset gravity"""
        if not self.player.alive and not self.player.freeze and \
                not self.level_condition:
            self.jump_timer = pygame.time.get_ticks()  # Reset jump timer
            self.player.jump_boost = -1 * (self.player.max_jump - 1)
            self.player.jump_ability = False
            self.player.xpos = self.x_spawn
            self.player.ypos = self.y_spawn
            self.player.direction = 1
            self.player.gravity_counter = self.player.max_gravity

        # If player is below the level, count as a death (out of bounds)
        if (576 * self.res_height) + self.player.height < self.player.ypos:
            self.player.alive = False
            self.deaths += 1

        # Check for win collision
        if self.player.alive and \
                self.player.square_render.collidelist(self.win_zones) != -1:
            self.level_condition = True
            self.player.alive = False

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

    def victory(self, screen):
        # Victory function played when win condition
        pass

    def render(self, screen):
        # Default rendering
        screen.fill(WHITE)

        self.render_level(screen)
        self.player.render(screen)
        self.render_text(screen)

    def render_level(self, screen):
        x_factor = self.player.xpos - (1080 / 2) + self.player.width
        """ This function will be altered in the child class"""
        for plat in self.platforms:
            if 0 <= plat.x + plat.width + x_factor <= 1080 or \
                    0 <= plat.x + x_factor <= 1080:
                pygame.draw.rect(screen, BLACK, [plat.x + x_factor,
                                                 plat.y,
                                                 plat.width,
                                                 plat.height])

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
        self.xpos = x_spawn # Current x_position, initialized as spawn
        self.ypos = y_spawn  # Current y_position, initialized as spawn
        self.width = math.ceil(width * res_width)  # Current width, always 10
        self.height = math.ceil(
            height * res_height)  # Current height, always 10
        self.color = rgb  # Color of player as static constant or tuple
        self.square_render = None  # Pygame.draw rect of the player
        self.alive = False  # If the player is alive (able to move)
        self.freeze = False  # If the player is forced to pause

        self.jumps = 0  # Amount of jumps the player had done (remove)
        self.jump_ability = False  # If the player is able to jump
        self.enable_gravity = True  # If gravity is acting on the player
        self.max_jump = 50  # Limit for the jump loop to iterate
        self.jump_boost = -1 * (self.max_jump - 1)  # Counter for jump loop
        self.max_gravity = 95  # Limit for the gravity loop to iterate
        self.gravity_counter = self.max_gravity  # Counter for gravity loop

        sound_path = "file_path"
        #self.jump_sound_1 = pygame.mixer.Sound(sound_path + "jump_file")
        # Jump sound for player
        #self.jump_sound_1.set_volume(0.1 * (jump_vol / 100))  # out of 1 or 100%
        # Jump volume for the player, set at 0.1 out of 1, or 10%

        # Get location and info of surrounding blocks
        self.collide_rect = pygame.Rect(self.xpos - (30 * res_width),
                                        self.ypos - (30 * res_height),
                                        self.width + (60 * res_width),
                                        self.height + (80 * res_height))
        # Top, bottom, left and right collision
        self.left_col = pygame.Rect(self.xpos - self.width - (10 * res_width),
                                    self.ypos + (res_height * 1),
                                    self.width + (res_width * 10),
                                    8 * res_height)
        self.right_col = pygame.Rect(self.xpos + self.width,
                                     self.ypos + (res_height * 1),
                                     self.width + (10 * res_width),
                                     8 * res_height)
        self.top_col = pygame.Rect(self.xpos,
                                   self.ypos - self.height - (10 * res_height),
                                   10 * res_width,
                                   self.height + (10 * res_height))
        self.bot_col = pygame.Rect(self.xpos, self.ypos + self.height,
                                   10 * res_width, self.height * 4)

        self.res_width = res_width
        self.res_height = res_height

        """One single larger rect for collision detection
        """
        self.grav_y = None
        self.jump_y = None
        self.left_x = None
        self.right_x = None

    def update_detection(self):
        """
        Move the player by 4 units in the specific direction, multiplied
        by the difficulty factor (max of 1 usually)
        """
        # Move horizontally depending on the direction
        # todo: move everything but collision updates to the level
        """Player movement: move_factor = 4 * self.res_width

        if self.left_x is not None and \
                self.xpos + move_factor <= self.left_x:
            self.xpos = self.left_x
        elif self.right_x is not None and \
                self.right_x <= self.xpos + move_factor + self.width:
            self.xpos = self.right_x - self.width
        else:
            self.xpos += move_factor"""

        """# Gravity and jump functions
        self.gravity()
        self.jump()"""

        # Update collision logic position in real time with the player position
        self.collide_rect.x = self.xpos - (30 * self.res_width)
        self.collide_rect.y = self.ypos - (30 * self.res_height)
        self.left_col.x = self.xpos - self.width - (10 * self.res_width)
        self.left_col.y = self.ypos + (self.res_height * 1)
        self.right_col.x = self.xpos + self.width
        self.right_col.y = self.ypos + (self.res_height * 1)
        self.top_col.x = self.xpos
        self.top_col.y = self.ypos - self.height - (10 * self.res_height)
        self.bot_col.x = self.xpos
        self.bot_col.y = self.ypos + self.height

    def jump(self):
        # Jump that will change the player's y position in the game loop
        if self.jump_ability and 0 <= self.jump_boost:
            jump_factor = ((self.jump_boost ** 2) * 0.002)
            if self.jump_y is not None and \
                    self.ypos - self.jump_y < jump_factor:
                self.ypos = self.jump_y
                self.jump_ability = False
                self.jump_boost = -1
                self.enable_gravity = True
            else:
                self.ypos -= jump_factor * self.res_height
                """Change the y position based on the counter and difficulty. 
                This creates a parabolic relationship from being squared."""
                self.jump_boost -= 2
                """Decrease the counter until it reaches 0
                This is used to create the first arc of the jump"""
        else:
            """Crucial for the second half of the jump, 
            allowing the player to fall"""
            self.jump_ability = False

    def render(self, screen):
        # Visualize collision rect, uncomment to see
        """pygame.draw.rect(screen, (55, 230, 50), self.collide_rect)   # area
        pygame.draw.rect(screen, BLUE, self.left_col)  # left
        pygame.draw.rect(screen, BLUE, self.right_col)  # right
        pygame.draw.rect(screen, BLUE, self.top_col)  # top
        pygame.draw.rect(screen, BLUE, self.bot_col)  # bottom"""

        self.square_render = pygame.draw.rect(screen, self.color, [((1080 / 2)) * self.res_width,
                                                                   self.ypos,
                                                                   self.width,
                                                                   self.height])
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
        self.enable_gravity = True
        for bcollide_id in bot_collisions:
            """
            The if statement checks for if the player is on top of a platform
            and does so by checking:
            - If there's any rect that collided (id != -1)
            - If the player's bottom (self.ypos + self.height) is touching
                the bottom platform (collide_y <=) or a bit inside the platform
                (<= collide_y + self.height)
            - and If the player is within the bounds of the platform.

                The left boundary is collide_x < self.xpos + self.width, or if
                the right side of the player (self.xpos + self.width) is within 
                the left side of the platform (collide_x).

                The right boundary is self.xpos < collide_x + collide_width, or
                if the left side of the player (self. xpos) is within the
                right side of the platform (collide_x + collide_width)
            """
            collide_y = object_list[bcollide_id].y
            if self.ypos < collide_y and \
                    self.bot_col.colliderect(object_list[bcollide_id]) and not \
                    self.left_col.colliderect(object_list[bcollide_id]) and \
                    not self.right_col.colliderect(object_list[bcollide_id]):
                all_y += [collide_y]

            if (self.ypos + self.height == collide_y or
                self.square_render.colliderect(object_list[bcollide_id])) and \
                    self.bot_col.colliderect(object_list[bcollide_id]) and not \
                    self.left_col.colliderect(object_list[bcollide_id]) and \
                    not self.right_col.colliderect(object_list[bcollide_id]):
                # If true, disable/reset gravity, enable jump
                self.enable_gravity = False
                self.jump_ability = True
                self.gravity_counter = self.max_gravity

                if collide_y < self.ypos + self.height:
                    self.ypos = collide_y - self.height

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

            """
            This if statement checks for if the player's top touches the ceiling
                or the bottom of a platform:
                - If there's any rect that collided (id != -1)
                - 
            """
            if self.top_col.colliderect(object_list[tcollide_id]) and not \
                    self.left_col.colliderect(object_list[tcollide_id]) and \
                    not self.right_col.colliderect(object_list[tcollide_id]) \
                    and collide_y + collide_height < self.ypos:
                all_yheight += [collide_y + collide_height]

            if (self.square_render.colliderect(object_list[tcollide_id]) or
                self.ypos == collide_y + collide_height) and \
                    self.top_col.colliderect(object_list[tcollide_id]) and not \
                    self.left_col.colliderect(object_list[tcollide_id]) and \
                    not self.right_col.colliderect(object_list[tcollide_id]):
                self.jump_ability = False
                self.jump_boost = -1
                self.enable_gravity = True

                if self.ypos < collide_y + collide_height and \
                        self.xpos < collide_x + collide_width and \
                        collide_x < self.xpos + self.width:
                    self.ypos = collide_y + collide_height

        if 0 < len(all_yheight):
            self.jump_y = max(all_yheight)
        else:
            self.jump_y = None

    def collision_wall(self, object_list: [pygame.Rect]):
        # New collision logic:
        left_collision = self.collide_rect.collidelistall(object_list)
        right_collision = self.collide_rect.collidelistall(object_list)

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
                    collide_x + collide_width < self.xpos:
                all_xl += [collide_x + collide_width]

            if lcollide_id != -1 and self.square_render.colliderect(
                    object_list[lcollide_id]) and \
                    self.left_col.colliderect(object_list[lcollide_id]) and \
                    collide_y < self.ypos + self.height and \
                    self.ypos < collide_y + collide_height:

                if self.xpos < collide_x + collide_width and \
                        not self.top_col.colliderect(object_list[lcollide_id]):
                    self.xpos = collide_x + collide_width

        all_xr = []
        # Right side collision, going right to turn left
        for rcollide_id in right_collision:
            collide_x = object_list[rcollide_id].x
            collide_y = object_list[rcollide_id].y
            collide_height = object_list[rcollide_id].height

            if self.right_col.colliderect(object_list[rcollide_id]) and \
                    not self.top_col.colliderect(object_list[rcollide_id]) and \
                    not self.bot_col.colliderect(object_list[rcollide_id]) and \
                    self.xpos + self.width < collide_x:
                all_xr += [collide_x]

            if rcollide_id != -1 and self.square_render.colliderect(
                    object_list[rcollide_id]) and \
                    self.right_col.colliderect(object_list[rcollide_id]) and \
                    collide_y < self.ypos + self.height and \
                    self.ypos < collide_y + collide_height:

                if collide_x < self.xpos + self.width and \
                        not self.top_col.colliderect(object_list[rcollide_id]):
                    self.xpos = collide_x - self.width

        if 0 < len(all_xl):
            self.left_x = max(all_xl)
        else:
            self.left_x = None
        if 0 < len(all_xr):
            self.right_x = min(all_xr)
        else:
            self.right_x = None

    def gravity(self):
        # fix turning off gravity
        if self.enable_gravity and not self.jump_ability:
            gravity_y = ((self.gravity_counter ** 2) *
                         0.00015) * self.res_height
        else:
            gravity_y = 0

        if self.enable_gravity and not self.jump_ability:
            if self.grav_y is not None and \
                    self.grav_y < gravity_y + self.ypos + self.height:
                self.ypos = self.grav_y - self.height
                self.enable_gravity = False
                self.jump_ability = True
                self.gravity_counter = self.max_gravity
            else:
                self.ypos += gravity_y

        if self.gravity_counter < 1100:
            self.gravity_counter += 2

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
        """self.memory = Memory(width / 1080, height / 576) 
        # Initialize game memory
        self.memory.load_all_levels()   # Load all levels from different files

        self.memory.init_replays()
        self.memory.load_save()
        self.memory.music = Music(self.memory.total_music_per)"""

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

    file_path = "put_icon_file_path_here"
    """pygame.display.set_caption("display_window") # game window caption
    icon = pygame.image.load(file_path + "file_image_name") # loading image
    default_icon_image_size = (32, 32) # reducing size of image
    icon = pygame.transform.scale(icon, default_icon_image_size) 
    # scaling image correctly
    pygame.display.set_icon(icon) # game window icon"""

    start_game = Program()  # Initialize running the game with Program
    start_scene = PlayLevel((game_width + 10) / 2,
                            (game_height + 10) / 2,
                            game_width / 1080, game_height / 576)
    # Initialize the first scene/starting scene shown to the player
    start_game.run(game_width, game_height, start_scene)  # Run the game loop
    """The game loop will be stuck at this line (start_game.run) until the
    while loop (while self.running:) is no longer true. When self.running is
    False, the program will move onto the next line to quit"""

    pygame.quit()  # Quit the game/pygame instance
