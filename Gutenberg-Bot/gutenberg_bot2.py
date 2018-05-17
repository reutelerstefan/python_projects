import os 
import numpy as np
import re


def main():
    base_dir_folder = os.path.dirname(__file__)
    full_path = os.path.join(base_dir_folder, 'GUTINDEX.ALL')
    data_empty = []

    print(full_path)
    re = '.+, .+[ ]+[\d]+[\r\n]\s*(\w*\[.*\]\n)*'
    regex = '.+(, [\d\w\'.,& ]+).*[\d]+'

    with open(full_path, "r",encoding="utf8") as file:
        for line in file:
            if not "Gutenberg collection between" in line:
                data_empty.append(line)
                
            # print(line)
    data = " ".join(data_empty)
    # print(data)
    print(data)
    test_re = re.findall(regex,data)

    # print(dir(data_empty))
    # print("{},length: {}".format(data_empty,len(data_empty)))
    for n in test_re[0:10]:
          

        print(n.split('by'))

if __name__ == "__main__":
    main()