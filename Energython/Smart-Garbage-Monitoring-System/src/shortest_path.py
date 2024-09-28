import sys
import json
import pygame
from dijkstra import dijkstra
from firebase_reader import FirebaseReader
import argparse

class ShortestPath:
    def __init__(self, name):
        pygame.init()
        self.firebase_reader = FirebaseReader()

        self.name = name
        
        self.map = pygame.image.load(f'data/maps/{self.name}/{self.name}.png')
        self.screen = pygame.display.set_mode((self.map.get_width(), self.map.get_height()))
        self.screen.blit(self.map, (0, 0))

        self.graph = self.load_graph(f'data/maps/{self.name}/{self.name}.json')
        self.bins = self.get_bins()
        self.garage = self.get_garage()

        self.active_bins = self.firebase_reader.get_active_bins()
        
        if len(self.active_bins) > 0:
            trajectory = self.compute_path(self.active_bins.copy())
            self.draw_bins(trajectory)

    def load_graph(self, path):
        with open(path) as file:  # Using 'with' for safe file handling
            return json.load(file)

    def get_bins(self):
        bins = []
        for node in self.graph:
            if self.graph[node]['type'] == 'bin':
                bins.append(node)
        return bins

    def get_garage(self):
        for node in self.graph:
            if self.graph[node]['type'] == 'garage':
                return node
        return None
        
    def compute_path(self, bins):
        trajectory = []
        start = self.garage
        unvisited_bins = bins.copy()

        while unvisited_bins:
            # Get the closest bin from the current position
            min_cost = float('inf')
            closest_bin = None
            path_to_closest_bin = []

            for bin in unvisited_bins:
                cost, path = dijkstra(self.graph, start, bin)
                if cost < min_cost:
                    min_cost = cost
                    closest_bin = bin
                    path_to_closest_bin = path

            if closest_bin is not None:
                # Append the path to the trajectory
                trajectory.extend(path_to_closest_bin)
                start = closest_bin
                unvisited_bins.remove(closest_bin)  # Mark as visited

        # Return to the garage after visiting all bins
        cost, path_to_garage = dijkstra(self.graph, start, self.garage)
        trajectory.extend(path_to_garage)

        return trajectory

    def draw_bins(self, trajectory):
        for node in self.graph:
            if self.graph[node]['type'] == 'bin':
                if node in self.active_bins:
                    pygame.draw.circle(self.screen, (255, 0, 0), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)
                else:
                    pygame.draw.circle(self.screen, (0, 255, 0), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)
            
            if self.graph[node]['type'] == 'garage':
                pygame.draw.circle(self.screen, (0, 0, 255), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)

        if trajectory:
            for i in range(len(trajectory) - 1):
                pygame.draw.line(self.screen, (255, 0, 0), 
                                 (self.graph[trajectory[i]]['pos']['x'], self.graph[trajectory[i]]['pos']['y']),
                                 (self.graph[trajectory[i + 1]]['pos']['x'], self.graph[trajectory[i + 1]]['pos']['y']))

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--town_name', type=str, default="pondicherry_india")
    
    shortest_path = ShortestPath(parser.parse_args().town_name)
    
    running = True

    while running:
        shortest_path.update()   

if __name__ == "__main__":
    main()
