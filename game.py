from __future__ import print_function
import math
from CYLGame import GameLanguage
from CYLGame import Game
from CYLGame import MessagePanel
from CYLGame import MapPanel
from CYLGame import StatusPanel
from CYLGame import PanelBorder


class ROBOTS(Game):
    MAP_WIDTH = 60
    MAP_HEIGHT = 30
    SCREEN_WIDTH = 60
    SCREEN_HEIGHT = MAP_HEIGHT + 6
    MSG_START = 20
    MAX_MSG_LEN = SCREEN_WIDTH - MSG_START - 1
    CHAR_WIDTH = 16
    CHAR_HEIGHT = 16
    GAME_TITLE = "ROBOTS"
    CHAR_SET = "terminal16x16_gs_ro.png"

    STAIR_DESCENT_RESPONSES = ["Maybe there's an exit this way!", "I wonder what's down here?", "Gotta escape these bots!", "Is this the last floor?", "What's this way?"]

    NUM_OF_BOTS_START = 4
    NUM_OF_BOTS_PER_LEVEL = 4
    MAX_TURNS = 300

    PLAYER = '@'
    STAIRS = '>'
    EMPTY = ' '
    ROBOT = 'O'

    def __init__(self, random):
        self.random = random
        self.running = True
        self.touching_bot = False
        centerx = self.MAP_WIDTH / 2
        centery = self.MAP_HEIGHT / 2
        self.player_pos = [centerx, centery]
        self.score = 0
        self.objects = []
        self.turns = 0
        self.level = 0
        self.msg_panel = MessagePanel(self.MSG_START, self.MAP_HEIGHT+1, self.SCREEN_WIDTH - self.MSG_START, 5)
        self.status_panel = StatusPanel(0, self.MAP_HEIGHT+1, self.MSG_START, 5)
        self.panels = [self.msg_panel, self.status_panel]
        self.msg_panel.add("Welcome to R0B0TS!!!")
        self.msg_panel.add("Descend stairs while avoiding robots!")

        self.__create_map()

    def __create_map(self):
        self.map = MapPanel(0, 0, self.MAP_WIDTH, self.MAP_HEIGHT+1, self.EMPTY,
                            border=PanelBorder.create(bottom="-"))
        self.panels += [self.map]

        self.map[(self.player_pos[0], self.player_pos[1])] = self.PLAYER

        self.place_stairs(1)
        self.place_bots(self.NUM_OF_BOTS_START)

    def place_stairs(self, count):
        self.place_objects(self.STAIRS, count)

    def place_bots(self, count):
        self.place_objects(self.ROBOT, count)

    def place_objects(self, char, count):
        placed_objects = 0
        while placed_objects < count:
            x = self.random.randint(0, self.MAP_WIDTH - 1)
            y = self.random.randint(0, self.MAP_HEIGHT - 1)

            if self.map[(x, y)] == self.EMPTY:
                self.map[(x, y)] = char
                placed_objects += 1

    def handle_key(self, key):
        self.turns += 1

        self.map[(self.player_pos[0], self.player_pos[1])] = self.EMPTY
        if key == "w":
            self.player_pos[1] -= 1
        if key == "s":
            self.player_pos[1] += 1
        if key == "a":
            self.player_pos[0] -= 1
        if key == "d":
            self.player_pos[0] += 1
        if key == "q":
            self.player_pos[1] -= 1
            self.player_pos[0] -= 1
        if key == "e":
            self.player_pos[1] -= 1
            self.player_pos[0] += 1
        if key == "c":
            self.player_pos[1] += 1
            self.player_pos[0] += 1
        if key == "z":
            self.player_pos[1] += 1
            self.player_pos[0] -= 1

        if key == "Q":
            self.running = False
            return

        self.player_pos[0] %= self.MAP_WIDTH
        self.player_pos[1] %= self.MAP_HEIGHT
        
        # if player gets to the stairs, the other robots don't get a
        # chance to take their turn
        if self.map[(self.player_pos[0], self.player_pos[1])] == self.STAIRS:
            self.score += 1
            self.msg_panel += [self.random.choice(list(set(self.STAIR_DESCENT_RESPONSES) - set(self.msg_panel.get_current_messages())))]
            self.level += 1
            self.place_stairs(1)
            self.place_bots(self.NUM_OF_BOTS_PER_LEVEL)

        # if a bot is touching a player, then set touching_bot to TRUE
        # and also update the map to show the attacking robot
        if self.map[(self.player_pos[0], self.player_pos[1])] == self.ROBOT:
            self.touching_bot = True
            self.map[(self.player_pos[0], self.player_pos[1])] = self.ROBOT
        else:
            self.map[(self.player_pos[0], self.player_pos[1])] = self.PLAYER

    def is_running(self):
        return self.running

    def find_closest_stairs(self, x, y):
        stairs_pos_dist = []
        for pos in self.map.get_all_pos(self.STAIRS):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    a_x, a_y = pos[0]+(self.SCREEN_WIDTH*i), pos[1]+(self.SCREEN_HEIGHT*j)
                    dist = math.sqrt((a_x-x)**2 + (a_y-y)**2)
                    direction = [a_x-x, a_y-y]
                    if direction[0] > 0:
                        direction[0] = 1
                    elif direction[0] < 0:
                        direction[0] = -1
                    if direction[1] > 0:
                        direction[1] = 1
                    elif direction[1] < 0:
                        direction[1] = -1
                    stairs_pos_dist += [(dist, direction)]

        stairs_pos_dist.sort()
        if len(stairs_pos_dist) > 0:
            return stairs_pos_dist[0][1]
        else:
            raise Exception("We can't find the stairs!")

    def get_vars_for_bot(self):
        bot_vars = {}

        x_dir, y_dir = self.find_closest_stairs(*self.player_pos)

        x_dir_to_char = {-1: ord("a"), 1: ord("d"), 0: 0}
        y_dir_to_char = {-1: ord("w"), 1: ord("s"), 0: 0}

        bot_vars = {"x_dir": x_dir_to_char[x_dir], "y_dir": y_dir_to_char[y_dir],
                    "pit_to_east": 0, "pit_to_west": 0, "pit_to_north": 0, "pit_to_south": 0}

        if self.map[((self.player_pos[0]+1)%self.MAP_WIDTH, self.player_pos[1])] == self.ROBOT:
            bot_vars["pit_to_east"] = 1
        if self.map[((self.player_pos[0]-1)%self.MAP_WIDTH, self.player_pos[1])] == self.ROBOT:
            bot_vars["pit_to_west"] = 1
        if self.map[(self.player_pos[0], (self.player_pos[1]-1)%self.MAP_HEIGHT)] == self.ROBOT:
            bot_vars["pit_to_north"] = 1
        if self.map[(self.player_pos[0], (self.player_pos[1]+1)%self.MAP_HEIGHT)] == self.ROBOT:
            bot_vars["pit_to_south"] = 1

        return bot_vars

    @staticmethod
    def default_prog_for_bot(language):
        if language == GameLanguage.LITTLEPY:
            return open("bot.lp", "r").read()

    def get_score(self):
        return self.score

    def draw_screen(self, libtcod, console):
        # End of the game
        if self.turns >= self.MAX_TURNS:
            self.running = False
            self.msg_panel.add("You are out of moves.")
        elif self.touching_bot:
            self.running = False
            self.msg_panel += ["A robot got you! :( "]

        if not self.running:
            self.msg_panel += ["GAME 0VER: Score:" + str(self.score)]

        libtcod.console_set_default_foreground(console, libtcod.white)

        # Update Status
        self.status_panel["Score"] = self.score
        self.status_panel["Move"] = str(self.turns) + " of " + str(self.MAX_TURNS)

        for panel in self.panels:
            panel.redraw(libtcod, console)


if __name__ == '__main__':
    from CYLGame import run
    run(ROBOTS)
