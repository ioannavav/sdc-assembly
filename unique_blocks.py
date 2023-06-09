import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 unique_blocks.py <file>")
        return

    input_file = sys.argv[1]

    pairs = set()
    with open(input_file, "r") as f_in:
        for line in f_in:
            first, second, *_ = line.split()
            pair = (first, second)

            if pair not in pairs:
                print(first, second)
                pairs.add(pair)

if __name__ == "__main__":
    main()
