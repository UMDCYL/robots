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

    SENSE_DIST = 20

    STAIR_DESCENT_RESPONSES = ["Maybe there's an exit this way!", "I wonder what's down here?", "Gotta escape these bots!", "Is this the last floor?", "What's this way?"]

    NUM_OF_BOTS_START = 4
    NUM_OF_BOTS_PER_LEVEL = 4
    MAX_TURNS = 300

    PLAYER = '@'
    STAIRS = '>'
    WRECKAGE = '<'
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

    def shortest_distance_between(self, x1, y1, x2, y2):
        dists = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                a_x, a_y = x1 + (self.MAP_WIDTH * i), y1 + (self.MAP_HEIGHT * j)
                d_x, d_y = math.abs(a_x - x2), math.abs(a_y - y2)
                dists += [max(d_x, d_y)]
        return min(dists)

    def shortest_distance_and_direction(self, x1, y1, x2, y2):
        dists = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                a_x, a_y = x1 + (self.MAP_WIDTH * i), y1 + (self.MAP_HEIGHT * j)
                d_x, d_y = abs(a_x - x2), abs(a_y - y2)
                direction = [a_x-x2, a_y-y2]
                if direction[0] > 0:
                    direction[0] = 1
                elif direction[0] < 0:
                    direction[0] = -1
                if direction[1] > 0:
                    direction[1] = 1
                elif direction[1] < 0:
                    direction[1] = -1
                dists += [(max(d_x, d_y), direction)]
        dists.sort()
        return dists[0]

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

    #def get_robot_positions(self):
    #    # returns an array of all x,y values at which there is a robot
    #    self.map.get_all_pos(self.ROBOT)
    #    for x in range(self.MAP_WIDTH):
    #        for y in range(self.MAP_HEIGHT):
    #            if self.map[(x,y)] == self.ROBOT:
    #                self.robots.append((x,y))

    def handle_key(self, key):
        print(self.get_vars_for_bot())
        self.turns += 1
        self.score += 1

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
        if key == "t":
            self.msg_panel += ["TELEP0RT!"]
            self.player_pos[0] = self.random.randint(0, self.MAP_WIDTH - 1)
            self.player_pos[1] = self.random.randint(0, self.MAP_HEIGHT - 1)

        if key == "Q":
            self.running = False
            return

        self.player_pos[0] %= self.MAP_WIDTH
        self.player_pos[1] %= self.MAP_HEIGHT

        # if player gets to the stairs, the other robots don't get a
        # chance to take their turn
        if self.map[(self.player_pos[0], self.player_pos[1])] == self.STAIRS:
            self.score += self.level * 10
            self.msg_panel += [self.random.choice(list(set(self.STAIR_DESCENT_RESPONSES) - set(self.msg_panel.get_current_messages())))]
            self.level += 1
            self.place_stairs(1)
            self.place_bots(self.NUM_OF_BOTS_PER_LEVEL)

        # if a bot is touching a player, then set touching_bot to TRUE
        # and also update the map to show the attacking robot
        if self.map[(self.player_pos[0], self.player_pos[1])] == self.ROBOT or \
            self.map[(self.player_pos[0], self.player_pos[1])] == self.WRECKAGE:
            self.touching_bot = True
            # redraw robot here -- it looks weird if the player is
            # visible but killed by an invisible robot
            #self.map[(self.player_pos[0], self.player_pos[1])] = self.ROBOT
        else:
            # player moved into a spot without a robot
            self.map[(self.player_pos[0], self.player_pos[1])] = self.PLAYER

        # go through the map and calculate moves for every robot based
        # on player's position

        robots = self.map.get_all_pos(self.ROBOT)

        # move each robot once
        for x, y in robots:
            print("found robot at (%d,%d)" % (x,y))
            if self.map[(x, y)] == self.WRECKAGE:
                # this robot got wrecked before it could move...
                # next robot please.
                continue

            # find the direction towards the player
            x_dir, y_dir = self.find_closest_player(x, y)

            print("\tI'm going to move (%d,%d) towards player" % (x_dir, y_dir))

            # get new location modulo map size
            newpos = ((x+x_dir) % self.MAP_WIDTH, (y+y_dir) % self.MAP_HEIGHT)

            if self.map[newpos] == self.STAIRS:
                # robot won't step on stairs (7 cycles bad robot luck)
                continue

            # erase robot in prep to move locations
            self.map[(x, y)] = self.EMPTY

            # draw the new robot into position and check for collisions
            if self.map[newpos] == self.ROBOT or self.map[newpos] == self.WRECKAGE:
                # already a robot here -- collision!
                print("collision!")
                self.map[newpos] = self.WRECKAGE
                self.score += 10
            else:
                self.map[newpos] = self.ROBOT

            # if a bot is touching a player, then set touching_bot to TRUE
            # and also update the map to show the attacking robot
            if self.map[(self.player_pos[0], self.player_pos[1])] == self.ROBOT:
                self.touching_bot = True
                break

    def is_running(self):
        return self.running

    # find the closest thing (foo) in the map relative to the given
    # x and y parameter (useful for finding stairs, players, etc.)
    def find_closest_foo(self, x, y, foo):
        foo_pos_dist = []
        for pos in self.map.get_all_pos(foo):
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
                    foo_pos_dist += [(dist, direction)]

        foo_pos_dist.sort()
        if len(foo_pos_dist) > 0:
            return foo_pos_dist[0][1]
        else:
            raise Exception("We can't find the foo you're looking for!")

    def find_closest_player(self, x, y):
        foo_pos_dist = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                a_x, a_y = self.player_pos[0]+(self.SCREEN_WIDTH*i), self.player_pos[1]+(self.SCREEN_HEIGHT*j)
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
                foo_pos_dist += [(dist, direction)]

        foo_pos_dist.sort()
        if len(foo_pos_dist) > 0:
            return foo_pos_dist[0][1]
        else:
            raise Exception("We can't find the foo you're looking for!")

    def get_vars_for_bot(self):
        bot_vars = {}

        # get values for x_dir and y_dir to direct player towards stairs
        x_dir, y_dir = self.find_closest_foo(self.player_pos[0], self.player_pos[1], self.STAIRS)

        x_dir_to_char = {-1: ord("a"), 1: ord("d"), 0: 0}
        y_dir_to_char = {-1: ord("w"), 1: ord("s"), 0: 0}

        bot_vars = {"x_dir": x_dir_to_char[x_dir], "y_dir": y_dir_to_char[y_dir],
                    "sense_n": 0, "sense_s": 0, "sense_e": 0, "sense_w": 0,
                    "sense_ne": 0, "sense_nw": 0, "sense_se": 0, "sense_sw": 0}

        robots = self.map.get_all_pos(self.ROBOT)
        x_dir_to_str = {-1: "w", 1: "e", 0: ""}
        y_dir_to_str = {-1: "n", 1: "s", 0: ""}

        for robot_x, robot_y in robots:
            dist, direction = self.shortest_distance_and_direction(robot_x, robot_y, self.player_pos[0], self.player_pos[1])
            dir_x, dir_y = direction
            dir_str = y_dir_to_str[dir_y] + x_dir_to_str[dir_x]
            if dir_str == "":
                continue
            if bot_vars["sense_" + dir_str] == 0:
                bot_vars["sense_" + dir_str] = dist
            elif bot_vars["sense_" + dir_str] > dist:
                bot_vars["sense_" + dir_str] = dist

        return bot_vars

    @staticmethod
    def default_prog_for_bot(language):
        if language == GameLanguage.LITTLEPY:
            return open("bot.lp", "r").read()

    @staticmethod
    def get_intro():
        return open("intro.md", "r").read()

    @staticmethod
    def get_move_consts():
        consts = Game.get_move_consts()
        consts.update({"teleport": ord("t")})
        return consts

    @staticmethod
    def get_move_names():
        names = Game.get_move_names()
        names.update({ord("t"): "Teleport"})
        return names

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
