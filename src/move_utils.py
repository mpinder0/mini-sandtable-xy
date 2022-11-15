from operator import sub, eq
import math

class MoveUtils:

    distance_per_step = 0.0
    last_position = None

    def __init__(self, distance_per_step):
        self.distance_per_step = distance_per_step

    def mm_to_steps(self, mm, distance_per_step = None):
        if not distance_per_step:
            distance_per_step = self.distance_per_step
        return round(mm / distance_per_step)

    def limit(self, value, maximum):
        return min(value, maximum)

    def scale(self, value, v_min, v_max, out_min, out_max):
        # y = mx+c
        pass

    def get_move_actions_from_positions(self, new_position):
        if not self.last_position:
            self.last_position = new_position

        distance_to_move = tuple(map(sub, new_position, self.last_position))
        steps_to_move = tuple(map(self.mm_to_steps, distance_to_move))
        print(new_position, distance_to_move, steps_to_move)

        step_list = self.get_move_steps_from_step_distance(steps_to_move)
        step_actions = self.get_move_actions_from_step_list(step_list)
        return step_actions
    
    def get_move_steps_from_step_distance(self, steps_to_move):
        axis_max = max(map(abs,steps_to_move))
        if axis_max != 0:
            x_ratio = steps_to_move[0] / axis_max
            y_ratio = steps_to_move[1] / axis_max

            step_numbers = range(axis_max + 1)
            x_steps = [math.floor(x_ratio*n) for n in step_numbers]
            y_steps = [math.floor(y_ratio*n) for n in step_numbers]
            steps = list(zip(x_steps, y_steps))
            return steps
        else:
            return []

    def get_move_actions_from_step_list(self, move_step_counts):
        if len(move_step_counts) < 1:
            return ((None, None), [])

        x_direction = 'R' if move_step_counts[-1][0] < 0 else 'F'
        y_direction = 'R' if move_step_counts[-1][1] < 0 else 'F'
        directions = (x_direction, y_direction)
        
        current = move_step_counts[0]
        step_actions = []
        for step_count in move_step_counts:
            do_step_x = step_count[0] != current[0]
            do_step_y = step_count[1] != current[1]
            step_actions.append((do_step_x, do_step_y))
            current = step_count

        return (directions, step_actions)

#mv = MoveUtils(0.45)
##print(mv.get_move_steps_from_positions((0,0), (5,10)))
#mv_counts = mv.get_move_steps_from_step_distance((0,10))
#print(mv_counts)
#mv_steps = mv.get_move_actions_from_step_list(mv_counts)
#print(mv_steps)
