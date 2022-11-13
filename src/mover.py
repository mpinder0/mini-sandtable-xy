"""Simple test for using adafruit_motorkit with a stepper motor"""
import time
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
from move_utils import MoveUtils
import loader

bed_size_x = 450 # mm
bed_size_y = 450 # mm
distance_per_step = 0.45
speed = 1 # distance (mm) per second
s_per_step = 1/(speed/distance_per_step) # seconds per step for speed

kit = MotorKit(i2c=board.I2C(), steppers_microsteps=4)
move_util = MoveUtils(0.45)

def execute_pattern(pattern_df):
    # iterate over dataframe coords
    for row in pattern_df.itertuples():
        print('Move to X:', row['X'], ', Y:', row['Y'])
        
        # using target coordinates, get the step actions
        (direction, move) = move_util.get_move_actions_from_positions(row)
        
        # set directions
        x_direction = stepper.FORWARD if direction[0] == 'F' else stepper.BACKWARD
        y_direction = stepper.FORWARD if direction[1] == 'F' else stepper.BACKWARD
        
        # iterate over step actions with pause
        for step in move:
            if step[0]:
                kit.stepper1.onestep(direction=x_direction, style=stepper.MICROSTEP)
            if step[1]:
                kit.stepper2.onestep(direction=y_direction, style=stepper.MICROSTEP)
            time.sleep(s_per_step)


df = loader.load_pattern()
execute_pattern(df)
