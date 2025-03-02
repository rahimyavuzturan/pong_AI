import pygame
from pong import Game
import neat
import os



class PongGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)

        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball


    def test_ai(self):
    
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run
                    break

            # tuşlarla çalışması için
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.game.move_paddle(left=True, up=True)
            if keys[pygame.K_s]:
                self.game.move_paddle(left=True, up=False)


            game_info = self.game.loop()
            self.game.draw(False, True) # kaç hit olduğunu göstercek
            pygame.display.update()

        pygame.quit()

def eval_genomes(genomes, config):
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))

    for i, (genome_id1, genome1) in enumerate(genomes):

        if i == len(genomes) - 1:
            break
        
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome_id2.fitness = 0 if genome_id2.fitness is None else genome_id2.fitness
            game = PongGame(window, width, height)
            game.train_ai(genome1, genome2, config),

def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    
    run_neat(config)