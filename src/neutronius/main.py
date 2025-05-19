from neutronius.game.Game import Game
import random

if __name__ == "__main__":
    random.seed(4)
    g = Game(500, 500, True, 4, True, 1000000)
    g.start()
 