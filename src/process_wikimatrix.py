"""
// Copyright 2020 Twitter, Inc.
// SPDX-License-Identifier: Apache-2.0
"""

import pandas as pd
import gzip
from pathlib import Path


def get_lines(filepath, min_score=1.05):
    with gzip.open(filepath, "rt", encoding="utf-8") as tsv:
        for line in tsv:
            line = line.strip()
            if not line:
                break
            fields = line.split("\t")
            fields[0] = float(fields[0])
            if fields[0] < min_score:
                continue
            fields[1] = fields[1].strip()
            fields[2] = fields[2].strip()
            yield fields[:3]


def process(source, target, file_prefix=None, data_dir="../data/wikimatrix"):
    """Process Wikimatrix dataset
    
    source: Wikimatrix language code: e.g. en for English
    target: Wikimatrix language code: e.g. ar for Arabic
    file_prefix: E.g. en_ar, this is what is used in the notebooks.
    data_dir: data folder
    """
    if file_prefix is None:
        file_prefix = f"{source[:2]}_{target[:2]}"
    filepath = Path(f"{data_dir}/WikiMatrix.{target}-{source}.tsv.gz").expanduser()
    df = pd.DataFrame(get_lines(filepath), columns=["score", "lang1", "lang2"])
    # Only select high quality translation pairs using score > 1.05
    # See: https://github.com/facebookresearch/LASER/tree/main/tasks/WikiMatrix#data-extraction-and-threshold-optimization
    df_cleaned = (
        df[df["score"] > 1.05]
        .dropna()
        .assign(
            unique_label_desc=lambda df_t: df_t.apply(
                lambda row: [row["lang1"], row["lang2"]], axis=1
            ),
            id=lambda df_t: df_t.index.astype("str"),
        )[["id", "unique_label_desc"]]
    )
    df_cleaned.to_json(
        f"{data_dir}/{file_prefix}_wikimatrix.json", orient="records", lines=True
    )
