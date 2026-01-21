import pdb
import argparse
from src.config import *

from src.Tagger import Tagger


def main():
    # parse the path of the json config file
    arg_parser = argparse.ArgumentParser(description="")
    arg_parser.add_argument(
        'config',
        metavar='config_json_file',
        default='None',
        help='The Configuration file in json format')
    arg_parser.add_argument(
        'start',
        metavar='start_date',
        default='None',
        help='The start date for manual tagging')
    arg_parser.add_argument(
        'end',
        metavar='end_date',
        default='None',
        help='The end date for manual tagging')
    args = arg_parser.parse_args()

    # parse the config json file
    # config = process_config(args.config)
    config, _ = get_config_from_json(args.config)

    # Create the Agent and pass all the configuration to it then run it..
    tagger = Tagger(config)
    tagger.run(args.start, args.end)


if __name__ == '__main__':
    main()
