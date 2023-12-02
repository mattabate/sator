import itertools


map = [[11, 10, 11, 14], [8, 6, 9, 9], [10, 4, 3, 1], [7, 6, 5, 0]]
color_map_templats = [['b', 'b', 'b', 'b'], ['b', 'b', 'b', 'b'], ['b', 'b', 'b', 'b'], ['b', 'b', 'b', 'b']]

# ANSI escape codes for colors
colors = {
    'b': '\033[94m',  # Blue
    'p': '\033[95m',  # Pink
    'g': '\033[92m',  # Green
    'y': '\033[93m',  # Yellow
    'reset': '\033[0m' # Reset to default color
}

def print_map(map, color_map):
    for row, color_row in zip(map, color_map):
        colored_row = [colors[color] + str(num) + colors['reset'] for num, color in zip(row, color_row)]
        print('\t'.join(colored_row))


if __name__ == '__main__':
    current = [1, 0]

    def make_color_map(current):
        color_map = color_map_templats

        can_jump = [(0, 1, 2), (0, 2, 1)]
        original_tuple = (0, 1, 2)
        permutations = itertools.permutations(original_tuple)
        permutations_list = list(permutations)

        color_map[3-current[0]][current[1]] = 'p'
        color_map[3-current[0]-2][current[1]] = 'y'
        color_map[3-current[0]-2][current[1]+1] = 'y'
        color_map[3-current[0]-1][current[1]] = 'y'
        color_map[3-current[0]][current[1]+2] = 'y'
        color_map[3-current[0]-1][current[1]+2] = 'y'
        color_map[3-current[0]][current[1]+1] = 'y'
        return color_map

    color_map = make_color_map(current)
    print_map(map, color_map=color_map)
