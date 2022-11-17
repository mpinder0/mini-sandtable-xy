import pandas as pd
from pygcode import Line

bed_size_x = 45 # mm
bed_size_y = 45 # mm

filename = 'tests/gcode/square-spiral.gcode'
#filename = 'tests/gcode/axis-test.gcode'

def scale_pattern(pattern_df):
    pattern_max = pattern_df.max().max()
    pattern_min = pattern_df.min().min()
    bed_min = min(bed_size_x, bed_size_y)
    ratio = bed_min / (pattern_max - pattern_min)
    print('scaling ratio: ', ratio)

    return pattern_df.multiply(ratio).add(pattern_min)

def load_pattern():
    coords = []

    with open(filename, 'r') as fh:
        for line_text in fh.readlines():
            line = Line(line_text)
            if line.block:
                for gc in line.block.gcodes:
                    if gc.word_key == 'G01':
                        coords.append(gc.get_param_dict())

    pattern_df = pd.DataFrame.from_dict(coords)
    print('Loaded file as dataframe.')

    scaled_df = scale_pattern(pattern_df)
    print('Rescale to axis limits')

    return scaled_df
