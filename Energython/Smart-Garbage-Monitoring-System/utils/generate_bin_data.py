import json
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--town_name', type=str, default="pondicherry_india")
    
    name = parser.parse_args().town_name
    file = open(f'data/maps/{name}/{name}.json')

    graph = json.load(file)  
    bin_data = {}

    for node in graph:
        if graph[node]['type'] == 'bin':
            bin_data[node] = {'lat': 0.0, 'lon': 0.0, 'state': 0}

    with open(f'data/maps/{name}/{name}_bin_data.json', 'w') as file:
        file.write(json.dumps(bin_data))
 
if __name__ == "__main__":
    main()