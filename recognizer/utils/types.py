import argparse

def natural_number_type(value):
    int_value = int(value)
    if int_value <= 0:
        raise argparse.ArgumentTypeError("Expected a natural number, i.e. a integral number greater than zero.")
    return int_value