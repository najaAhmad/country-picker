
import argparse
from .app import run_app

def parse_args():
    parser = argparse.ArgumentParser(description='Country Picker Application')
    parser.add_argument(
        '--select', 
        type=str, 
        help='Pre-select a country'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    run_app(args.select)

if __name__ == "__main__":
    main()