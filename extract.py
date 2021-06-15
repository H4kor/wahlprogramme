""" extract text from all PDFs an store as txt file """

import os
from tika import parser


def main():
    for year in os.listdir("data/"):
        folder = os.path.join("data", year)
        if os.path.isdir(folder):
            for fname in os.listdir(folder):
                if fname.endswith(".pdf"):
                    oname = ".".join(fname.split(".")[:-1] + ["xml"])
                    raw = parser.from_file(os.path.join(folder, fname), xmlContent=True)
                    with open(os.path.join(folder, oname), "w") as out:
                        out.write(raw["content"])


if __name__ == "__main__":
    main()
