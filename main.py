import argparse
from world import World


def main(args):
    """
    Main function to run the Game of Life simulation.

    Args:
    args (Namespace): Command line arguments containing window size and simulation speed.
    """
    try:
        world = World(window_size=args.window_size, speed=args.speed)
        world.play()
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the Game of Life simulation.")
    parser.add_argument('--window_size', type=int, default=750,
                        help='Size of the square window. Should be a positive integer.')
    parser.add_argument('--speed', type=float, default=0.1,
                        help='Duration of every step in seconds. Should be a positive number.')

    args = parser.parse_args()
    if args.window_size <= 0 or args.speed <= 0:
        print("Window size and speed should be positive values.")
    else:
        main(args)
