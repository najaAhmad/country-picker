"""Command-line interface for Country Picker application"""

import argparse
from .app import run_app

def parse_args():
    """Parse CLI arguments: --select for country preselect"""
    parser = argparse.ArgumentParser(description='Country Picker App')
    parser.add_argument(
        '--select', 
        type=str, 
        help='Pre-select a country'
    )
    return parser.parse_args()

def main():
    """Entry point: Parse args and launch app"""
    args = parse_args()
    run_app(args.select)

if __name__ == "__main__":
    main()