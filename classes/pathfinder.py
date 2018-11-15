import math

class Pathfinder:
    def __init__(self, laby):
        self.nodes = laby.empty_positions
        self.laby = laby

        # Add special objects
        self.objects = laby.objects
        for _ in self.objects:
            self.nodes.add((_.line, _.column))
        
        self.player = laby.player
        self.nodes.add((self.player.line, self.player.column))
        
        self.paths = dict()
        
        self.neighbours = dict()
        
        self._build_neighbours()
        self.find_path()
        
    def remove_object(self, line, col):
        for o in self.objects:
            if o.line == line and o.column == col:
                self.objects.remove(o)

        self.paths = dict()
        # delete_keys = list()
        # for k in self.paths.keys():
        #     if (k[0], k[1]) == (line, col):
        #         delete_keys.append((start, end))
                
        # for k in delete_keys:
        #     del self.paths[k]

    def _build_neighbours(self):
        for p in self.nodes:
            combinations = []
            above = (p[0] - 1, p[1])
            below = (p[0] + 1, p[1])
            right = (p[0], p[1] + 1)
            left = (p[0], p[1] - 1)

            if p[0] == 0:
                combinations.append(below)
            elif p[0] == max:
                combinations.append(above)
            else:
                combinations.append(below)
                combinations.append(above)
            
            # First col
            if p[1] == 0:
                combinations.append(right)
            elif p[1] == max:
                # Last col
                combinations.append(left)
            else:
                combinations.append(right)
                combinations.append(left)

            self.neighbours.update({ p: [n for n in combinations if n in self.nodes] })

    def find_neighbours(self, line, col):
            return self.neighbours[(line, col)]

    def find_path(self):
        if not self.objects:
            return []

        for item in self.objects:
            # if not abs(item.line - self.player.line) < self.laby.num_lines / 2 or \
            #    not abs(item.column - self.player.column) < self.laby.num_cols / 2:
            #    continue

            if not self.paths.get(
                ((self.player.line, self.player.column),
                (item.line, item.column))
            ):
                self.paths.update(
                    {
                        ((self.player.line, self.player.column), (item.line, item.column)): self.a_star(
                            (self.player.line, self.player.column),
                            (item.line, item.column)
                        )
                    }
                )
        active_paths = sorted(
            [
                (p[1], self.paths[p])
                for p in self.paths.keys()
                if p[0] == (self.player.line, self.player.column)
            ],
            key=lambda i: len(i[1])
        )
        if not len(active_paths):
            return []

        best_item = active_paths[0][1][0]

        best_path = self.paths[(self.player.line, self.player.column), best_item]
        for idx_line, line in enumerate(self.laby.level):
            for col, elm in enumerate(line):
                if elm == '^':
                    self.laby.level[idx_line][col] = ' '

        for _ in best_path:
            if self.laby.level[_[0]][_[1]] == ' ':
                self.laby.level[_[0]][_[1]] = '^'

    def a_star(self, start, goal):
        closed_set = set()
        open_set = set([start])

        bigmap = {n: { 'g_score': math.inf, 'f_score': math.inf } for n in self.nodes}

        came_from = {}

        bigmap[start]['g_score'] = 0

        bigmap[start]['f_score'] = self.heuristic_cost_estimate(start, goal)

        while len(open_set):
            # smallest_fscore_value(nodes in open_set)
            current = sorted(
                [
                    (n, bigmap[n]['f_score'])
                    for n in open_set
                ],
                key = lambda i: i[1]
            )[0][0]

            if current == goal:
                return self.reconstruct_path(came_from, current)

            open_set.remove(current)
            closed_set.add(current)

            for n in self.find_neighbours(current[0], current[1]):
                if n in closed_set:
                    continue
                
                new_gscore = bigmap[current]['g_score'] + 1

                if n not in open_set:
                    open_set.add(n)
                elif new_gscore >= bigmap[n]['g_score']:
                    continue

                came_from[n] = current
                bigmap[n]['g_score'] = new_gscore
                bigmap[n]['f_score'] = bigmap[n]['g_score'] + self.heuristic_cost_estimate(n, goal)        


    def heuristic_cost_estimate(self, start, end):
        return abs(end[1] - start[1]) + abs(end[0] - start[0])

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        
        return path
