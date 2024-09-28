import sys
import json
import pygame
import argparse

class GraphLoader:
    def __init__(self, name):
        pygame.init()

        self.name = name
        
        self.map = pygame.image.load(f'data/maps/{self.name}/{self.name}.png')
        self.screen = pygame.display.set_mode((self.map.get_width(), self.map.get_height()))
        self.screen.blit(self.map, (0, 0))

        self.load_graph(f'data/maps/{self.name}/{self.name}.json')

    def load_graph(self, path):
        file = open(path)
        self.graph = json.load(file)

    def update_graph(self):
        self.screen.blit(self.map, (0, 0))
        for node in self.graph:
            if self.graph[node]['type'] == 'bin':
                pygame.draw.circle(self.screen, (255,0,0), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)
            elif self.graph[node]['type'] == 'node':
                pygame.draw.circle(self.screen, (0,255,0), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)
            elif self.graph[node]['type'] == 'garage':
                pygame.draw.circle(self.screen, (0,0,255), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)

            for neighbor in self.graph[node]['neighbors']:
                pygame.draw.line(self.screen, (255, 0, 0), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), (self.graph[neighbor]['pos']['x'], self.graph[neighbor]['pos']['y']))


    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.update_graph()
        pygame.display.update()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--town_name', type=str, default="pondicherry_india")
    
    graph_loader = GraphLoader(parser.parse_args().town_name)
    
    running = True

    while running:
        graph_loader.update()   
 
if __name__ == "__main__":
    main()