import pdb
import argparse
from src.config import *

# from src.Agent import Agent
from src.App import App


def main():
    # parse the path of the json config file
    arg_parser = argparse.ArgumentParser(description="")
    arg_parser.add_argument(
        'config',
        metavar='config_json_file',
        default='None',
        help='The Configuration file in json format')
    args = arg_parser.parse_args()

    # parse the config json file
    # config = process_config(args.config)
    config, _ = get_config_from_json(args.config)

    # Create the Agent and pass all the configuration to it then run it..
    app = App(config)
    app.run()


if __name__ == '__main__':
    main()
