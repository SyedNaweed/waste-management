import sys
import json
import math
import pygame
import argparse

class GraphGenerator:
    def __init__(self, name):
        pygame.init()

        self.name = name
        
        self.map = pygame.image.load(f'data/maps/{self.name}/{self.name}.png')
        self.screen = pygame.display.set_mode((self.map.get_width(), self.map.get_height()))
        self.screen.blit(self.map, (0, 0))

        # self.graph = {
        #     0: {'pos': {'x': 10, 'y': 20}, 
        #         'type': 'bin', 
        #         'neighbors': {1: 100, 2: 300}},
        #     1: {'pos': {'x': 40, 'y': 50}, 
        #         'type': 'node', 
        #         'neighbors': {4: 230, 2: 530}}
        # }

        self.graph = {}
        self.num_of_nodes = 0
        self.current_node_idx = 0

        self.first_point = None

    def node_exists(self, pos):
        for node in self.graph:
            if self.distance(pos, [self.graph[node]['pos']['x'], self.graph[node]['pos']['y']]) <= 5:
                return node

        return None

    def distance(self, node1, node2):
        return math.sqrt((node2[0] - node1[0])**2 + (node2[1] - node1[1])**2)

    def add_node(self, pos, type):
        self.graph[self.current_node_idx] = {'pos': {'x': pos[0], 'y': pos[1]}, 'type': type, 'neighbors': {}}
        self.current_node_idx += 1
        self.num_of_nodes += 1
        print(self.graph)

    def delete_node(self, idx):
        self.graph.pop(idx)
        self.num_of_nodes -= 1
        for node in self.graph.copy():
            for neighbor in self.graph[node]['neighbors'].copy():
                if neighbor == idx:
                    self.graph[node]['neighbors'].pop(neighbor)
                    
        print(self.graph)

    def add_edge(self, neighbor):
        self.graph[self.first_point]['neighbors'][neighbor] = self.distance([self.graph[self.first_point]['pos']['x'], self.graph[self.first_point]['pos']['y']], [self.graph[neighbor]['pos']['x'], self.graph[neighbor]['pos']['y']])
        self.graph[neighbor]['neighbors'][self.first_point] = self.distance([self.graph[self.first_point]['pos']['x'], self.graph[self.first_point]['pos']['y']], [self.graph[neighbor]['pos']['x'], self.graph[neighbor]['pos']['y']])
        print(self.graph)

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("saving graph")
                    print(self.graph)

                    with open(f'data/maps/{self.name}/{self.name}.json', 'w') as file:
                        file.write(json.dumps(self.graph))

                if event.key == pygame.K_x:
                    pos = pygame.mouse.get_pos()
                    node_nearby = self.node_exists(pos)
                    if node_nearby is not None:
                        print("deleting node")
                        self.delete_node(node_nearby)

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                node_nearby = self.node_exists(pos)

                if node_nearby == None:
                    if (event.button == 1):
                        print("adding node")
                        self.add_node(pos, 'node')

                    if (event.button == 2):
                        print("adding garage")
                        self.add_node(pos, 'garage')

                    if (event.button == 3):
                        print("adding bin")
                        self.add_node(pos, 'bin')
                
                else:
                    print("node exists")
                    if self.first_point is None:
                        print("first point selected, click on next point to create edge")
                        self.first_point = node_nearby

                    else:
                        print("second point selected, creating edge")
                        self.add_edge(node_nearby)
                        self.first_point = None

        self.update_graph()
        pygame.display.update()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--town_name', type=str, default="pondicherry_india")
    
    graph_generator = GraphGenerator(parser.parse_args().town_name)
    
    running = True

    while running:
        graph_generator.update()   
 
if __name__ == "__main__":
    main()