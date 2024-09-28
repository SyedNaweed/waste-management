import sys
import json
import pygame
import random
import math
from dijkstra import dijkstra
import argparse

class ShortestPath:
    def __init__(self, name):
        pygame.init()

        self.name = name  # Store the town name
        
        # Load the map and initialize the display
        self.map = pygame.image.load(f'data/maps/{self.name}/{self.name}.png')
        self.screen = pygame.display.set_mode((self.map.get_width(), self.map.get_height()))
        self.screen.blit(self.map, (0, 0))

        # Load the graph and bin data
        self.graph = self.load_graph(f'data/maps/{self.name}/{self.name}.json')
        self.bins = self.get_bins()
        self.garage = self.get_garage()

        # Generate random garbage levels for each bin
        self.bin_garbage_levels = self.generate_random_garbage_levels()

        # Debugging print statement to check the garbage levels
        print(f"Garbage levels: {self.bin_garbage_levels}")

        # Get the active bins (bins with garbage level > 0)
        self.active_bins = [bin for bin, level in self.bin_garbage_levels.items() if level > 0]

        # Set up the starting position (garage) and trajectory
        self.current_position = self.garage
        self.trajectory = []

        # Compute the path to visit all active bins and return to the garage
        if self.active_bins:
            self.complete_path()

    def load_graph(self, path):
        """Load the graph from a JSON file."""
        with open(path) as file:
            return json.load(file)

    def get_bins(self):
        """Get all bins from the graph."""
        bins = []
        for node in self.graph:
            if self.graph[node]['type'] == 'bin':
                bins.append(node)
        return bins

    def get_garage(self):
        """Get the garage node from the graph."""
        for node in self.graph:
            if self.graph[node]['type'] == 'garage':
                return node
        return None

    def generate_random_garbage_levels(self):
        """Generate random garbage levels for bins."""
        garbage_levels = {}
        for bin in self.bins:
            # Random garbage level between 0 and 100%
            garbage_levels[bin] = random.randint(0, 100)
        return garbage_levels

    def complete_path(self):
        """Compute the path to visit all active bins and return to the garage."""
        bins_to_visit = self.active_bins.copy()
        visited_bins = set()

        while bins_to_visit:
            closest_bin = None
            min_cost = float('inf')
            path_to_closest_bin = []

            for bin in bins_to_visit:
                cost, path = dijkstra(self.graph, self.current_position, bin)
                if cost < min_cost:
                    closest_bin = bin
                    path_to_closest_bin = path
                    min_cost = cost

            if closest_bin:
                self.trajectory.extend(path_to_closest_bin[:-1])  # Exclude the last point since it's the current position
                self.current_position = closest_bin  # Update current position to closest bin
                visited_bins.add(closest_bin)  # Mark this bin as visited
                bins_to_visit.remove(closest_bin)  # Remove visited bin

        # Add path to garage at the end
        cost, path_to_garage = dijkstra(self.graph, self.current_position, self.garage)
        self.trajectory.extend(path_to_garage)  # Append path back to the garage

    def draw_bins(self):
        """Draw bins and current state on the screen."""
        font = pygame.font.Font(None, 24)  # Font for displaying garbage level

        for node in self.graph:
            if self.graph[node]['type'] == 'bin':
                bin_percentage = self.bin_garbage_levels.get(node, 0)
                
                # Red if garbage needs to be collected (percentage > 50), green otherwise
                color = (255, 0, 0) if bin_percentage > 50 else (0, 255, 0)
                
                # Draw the bin
                pygame.draw.circle(self.screen, color, (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)
                
                # Display garbage percentage
                text = font.render(f'{bin_percentage}%', True, (0, 0, 0))
                self.screen.blit(text, (self.graph[node]['pos']['x'] + 10, self.graph[node]['pos']['y'] - 10))

            elif self.graph[node]['type'] == 'garage':
                # Draw the garage in blue
                pygame.draw.circle(self.screen, (0, 0, 255), (self.graph[node]['pos']['x'], self.graph[node]['pos']['y']), 5)
                
                # Draw garage label
                label = font.render('Garage (Start)', True, (0, 0, 0))
                self.screen.blit(label, (self.graph[node]['pos']['x'] + 10, self.graph[node]['pos']['y'] + 10))

    def draw_arrow(self, start_pos, end_pos, color=(255, 0, 0)):
        """Draw an arrow pointing from start_pos to end_pos."""
        distance = math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
        if distance < 5:  # Skip drawing for very small distances
            return
        
        pygame.draw.line(self.screen, color, start_pos, end_pos, 2)
        
        # Calculate the direction of the arrow
        angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
        arrow_length = 10
        arrow_width = 5

        # Calculate the points for the arrowhead
        arrow_tip = end_pos
        left_wing = (end_pos[0] - arrow_length * math.cos(angle + math.pi / 6),
                    end_pos[1] - arrow_length * math.sin(angle + math.pi / 6))
        right_wing = (end_pos[0] - arrow_length * math.cos(angle - math.pi / 6),
                    end_pos[1] - arrow_length * math.sin(angle - math.pi / 6))

        # Draw the arrowhead
        pygame.draw.polygon(self.screen, color, [arrow_tip, left_wing, right_wing])

    def draw_trajectory(self):
        """Draw the current trajectory with arrows."""
        if len(self.trajectory) > 1:
            for i in range(len(self.trajectory) - 1):
                start_pos = (self.graph[self.trajectory[i]]['pos']['x'], self.graph[self.trajectory[i]]['pos']['y'])
                end_pos = (self.graph[self.trajectory[i + 1]]['pos']['x'], self.graph[self.trajectory[i + 1]]['pos']['y'])
                
                #print(f"Drawing trajectory from {start_pos} to {end_pos}")  # Debugging print statement
                
                # Set the color of the line as blue to show the path
                color = (0, 0, 255)  # Blue color for the line between points
                self.draw_arrow(start_pos, end_pos, color=color)

        # Draw endpoint (garage) at the end of the trajectory
        garage_pos = (self.graph[self.garage]['pos']['x'], self.graph[self.garage]['pos']['y'])
        pygame.draw.circle(self.screen, (255, 255, 0), garage_pos, 10)  # Yellow circle as endpoint
        endpoint_label = pygame.font.Font(None, 24).render('Garage (End)', True, (0, 0, 0))
        self.screen.blit(endpoint_label, (garage_pos[0] + 10, garage_pos[1] - 10))

    def update(self):
        """Handle events and update the screen."""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.blit(self.map, (0, 0))  # Clear the screen
        self.draw_bins()  # Draw bins on the map
        self.draw_trajectory()  # Draw the current trajectory to the next bin

        pygame.display.update()

def main():
    """Main function to start the step-by-step path visualization."""
    parser = argparse.ArgumentParser()
    parser.add_argument('map', type=str, help="Name of the town map")  # Changed to a positional argument
    
    # Initialize the ShortestPath class with the town name
    args = parser.parse_args()
    shortest_path = ShortestPath(args.map)
    
    running = True

    # Main loop to update the display
    while running:
        shortest_path.update()

if __name__ == "__main__":
    main()
