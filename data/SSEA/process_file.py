from glob import glob
import re


LABEL_MAP = {
    "NETEL": "NETE",
    "NET": "NETE",
    "NETL": "NETE",
    "NTE": "NETE",
    "K1": "NETE",
    "TERMS": "NETE",
    "NEPTE": "NETP",
    "NET1": "NETI",
    "NET0": "NETO",
    "NETOBE": "NETO",
    "NE0": "NEO",
    "NNEM": "NEM",
    "NTA": "NEA",
}


def parse_data(data):
    story_idx = -1
    sentence_idx = -1
    tokens = []
    label_type = None
    label_boundary = "O"
    for row in data:
        if row[0].startswith('<Story id="'):
            story_idx += 1
            continue
        if row[0].startswith('<Sentence id="'):
            sentence_idx += 1
            continue
        if row[0] == "</Sentence>":
            yield story_idx, sentence_idx, tokens
            tokens = []
            continue
        if row[0] == "</Story>":
            continue
        if len(row) == 3 and row[1] == "((":
            continue
        if len(row) == 4 and row[-1].startswith("<ne"):
            label_type = row[-1][:-1].split("=")[1]
            label_type = label_type.split("/")[0]
            label_type = label_type.upper().replace(" ", "").replace("/", "").strip()
            label_type = LABEL_MAP.get(label_type, label_type)
            label_boundary = None
            continue
        if len(row) == 2 and row[1] == "))":
            label_type = None
            label_boundary = "O"
            continue
        if row[0] == "":
            continue
        label_boundary = (
            "B" if label_type and (not label_boundary) else "I" if label_type else "O"
        )
        token = [row[1], label_boundary, label_type]
        tokens.append(token)
    return tokens


def print_tokens(tokens):
    get_label = lambda b, l: f"{b}-{l}" if l else b
    tokens_lines = "\n".join([f"{t[0]}\t{get_label(*t[1:])}" for t in tokens])
    return tokens_lines


def process_file(filepath):
    outfile = f"{filepath}.conll"
    with open(filepath) as fp, open(outfile, "w+") as fp_out:
        data = (line.rstrip().split("\t") for line in fp.readlines())
        for i, (story_id, sentence_id, tokens) in enumerate(parse_data(data)):
            print(print_tokens(tokens), file=fp_out, end="\n\n")
    print(f"Processed {i} sequences for {filepath}, saved to {outfile}")


if __name__ == "__main__":
    filepaths = glob("./training-*/*.utf8")
    for filepath in filepaths:
        process_file(filepath)
    filepaths = glob("./training-urdu/*.txt")
    for filepath in filepaths:
        process_file(filepath)
    filepaths = glob("./training-oriya/*")
    for filepath in filepaths:
        if filepath.endswith(".conll"):
            continue
        process_file(filepath)
    filepaths = glob("./training-telugu/*")
    for filepath in filepaths:
        if filepath.endswith(".conll"):
            continue
        process_file(filepath)
    filepaths = glob("./test-data-*.txt")
    for filepath in filepaths:
        process_file(filepath)

