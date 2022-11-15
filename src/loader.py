import pandas as pd
from pygcode import Line

filename = 'tests/gcode/square-spiral.gcode'
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
    return pattern_df
