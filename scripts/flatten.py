import json
import sys


def flatten(filename: str, uniq: str, mult: str) -> None:
    with open(filename, "r") as json_file:
        out = []

        data = json.load(json_file)
        for each in data:

            for _id in each[mult]:
                json_obj = {}
                json_obj[uniq] = each[uniq]
                json_obj[mult] = _id
                out.append(json_obj)

        print(json.dumps(out, indent=4))


if __name__ == "__main__":
    filename = sys.argv[1]
    uniqprop = sys.argv[2]
    multprop = sys.argv[3]

    flatten(filename, uniqprop, multprop)
