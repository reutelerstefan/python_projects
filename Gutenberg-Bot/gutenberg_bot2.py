import os 
import numpy as np
import re


def main():
    base_dir_folder = os.path.dirname(__file__)
    full_path = os.path.join(base_dir_folder, 'GUTINDEX.ALL')
    data_empty = []

    print(full_path)
    regex = '.+,.+[ ]+[\d]+'

    with open(full_path, "r") as file:
        for line in file:
            data_empty.append(line)
            # print(line)

    test_re = re.findall(regex, " ".join(data_empty))

    print(dir(data_empty))
    print("{},length: {}".format(data_empty[0:300],len(data_empty)))
    print(test_re)

if __name__ == "__main__":
    main()