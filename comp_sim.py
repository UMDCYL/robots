#!/usr/bin/python
import sys
from game import ROBOTS
from littlepython import Compiler
from CYLGame.Database import GameDB
from CYLGame.Comp import sim_competition


assert len(sys.argv) >= 2

comp_token = sys.argv[1]
game = ROBOTS
compiler = Compiler()
gamedb = GameDB(sys.argv[2])
assert gamedb.is_comp_token(comp_token)
sim_competition(compiler=compiler, game=game, gamedb=gamedb, token=comp_token, runs=1000, debug=True)