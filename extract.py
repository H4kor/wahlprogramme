""" extract text from all PDFs an store as txt file """

import os
from tika import parser


def main():
    for folder in ["2017", "2021"]:
        for fname in os.listdir(folder):
            if fname.endswith(".pdf"):
                oname = ".".join(fname.split(".")[:-1] + ["txt"])
                raw = parser.from_file(os.path.join(folder, fname))
                with open(os.path.join(folder, oname), "w") as out:
                    out.write(raw["content"])


if __name__ == "__main__":
    main()
