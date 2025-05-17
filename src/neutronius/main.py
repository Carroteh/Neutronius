from neutronius.game.Game import Game
import random

if __name__ == "__main__":
    random.seed(11)
    g = Game(500, 500, 11, False, 10000000)
    g.start()
 