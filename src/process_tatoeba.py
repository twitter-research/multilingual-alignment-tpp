"""
// Copyright 2020 Twitter, Inc.
// SPDX-License-Identifier: Apache-2.0
"""

import pandas as pd


def process(source, target, file_prefix=None, data_dir="../data/tatoeba"):
    """Process Tatoeba dataset
    
    source: Tatoeba language code: e.g. eng for English
    target: Tatoeba language code: e.g. ara for Arabic
    file_prefix: E.g. en_ar, this is what is used in the notebooks.
    data_dir: data folder
    """
    if file_prefix is None:
        file_prefix = f"{source[:2]}_{target[:2]}"

    df = pd.read_csv(f"{data_dir}/sentences.csv", sep="\t", header=None)
    df_links = pd.read_csv(f"{data_dir}/links.csv", sep="\t", header=None)

    df_lang_pairs = df[df[1].isin({source, target})]
    lang_counts = df_lang_pairs[1].value_counts()

    large_lang_items = df_lang_pairs[df_lang_pairs[1] == lang_counts.index[0]]

    small_lang_items = df_lang_pairs[df_lang_pairs[1] == lang_counts.index[-1]]

    df_paired = small_lang_items.merge(df_links, on=0).merge(
        large_lang_items, left_on="1_y", right_on=0
    )

    print((df_links[0] < df_links[1]).mean())

    df_paired_formatted = df_paired.assign(
        id=lambda t: t["0_x"].astype("str").str.cat(t["1_y"].astype("str"), sep="_"),
        unique_label_desc=lambda t: t.apply(
            lambda row: [row["2_y"], row["2_x"]], axis=1
        ),
    )[["id", "unique_label_desc"]]

    df_paired_formatted.to_json(
        f"{data_dir}/{file_prefix}_tatoeba.json", orient="records", lines=True
    )


def create_joint_data(data_dir="../data/tatoeba"):
    df = pd.concat(
        {
            k: pd.read_json(
                f"{data_dir}/{k}_tatoeba.json", orient="records", lines=True
            )
            for k in ["en_hi", "en_ja", "en_ar"]
        },
        names=["lang_pair"],
    ).reset_index(0)

    lang_pair_values = df.lang_pair.value_counts()
    max_value = lang_pair_values.max()
    max_pair = lang_pair_values.idxmax()
    df_new = pd.concat(
        [df]
        + [
            df[df.lang_pair == k].sample(
                max_value - lang_pair_values[k], replace=True, random_state=1337
            )
            for k in ["en_hi", "en_ja", "en_ar"]
            if k != max_pair
        ]
    ).sample(frac=1)

    df_new.to_json(
        f"{data_dir}/../tatoeba_multi/en_hi_ja_ar_equal_tatoeba.json",
        orient="records",
        lines=True,
    )

