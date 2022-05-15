from argparse import ArgumentParser, BooleanOptionalAction
from .doubletmaker import find_doublet_path, find_swap_path

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("start")
    parser.add_argument("end")
    parser.add_argument("-d", "--discord", action=BooleanOptionalAction, default=False)
    parser.add_argument("-l", "--ladder", action=BooleanOptionalAction, default=False)
    args = parser.parse_args()
    fp = find_swap_path if args.ladder else find_doublet_path
    try:
        path = fp(args.start, args.end)
        line = 1
        for word in path:
            if args.discord and line != 1 and word != args.end.upper():
                word = "||" + word + "||"
            print(f"{line}. {word}")
            line += 1
    except:
        print(f"Could not create doublet from {args.start} to {args.end}")
