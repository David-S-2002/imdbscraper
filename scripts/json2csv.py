import json
import csv
import sys


def json2csv(json_filename, csv_filename):
    with open(json_filename) as json_file:
        jsondata = json.load(json_file)

        data_file = open(csv_filename, 'w', newline='')
        csv_writer = csv.writer(data_file)

        count = 0
        for data in jsondata:
            if count == 0:
                header = data.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(data.values())

        data_file.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python json2csv.py json_filename csv_filename", file=sys.stderr)
        sys.exit(1)

    json_filename = sys.argv[1]
    csv_filename = sys.argv[2]

    json2csv(json_filename, csv_filename)
