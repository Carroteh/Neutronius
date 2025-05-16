from neutronius.game.Game import Game
import random

if __name__ == "__main__":
    random.seed(6)
    g = Game(500, 500, 6, True, 6000000)
    g.start()
 