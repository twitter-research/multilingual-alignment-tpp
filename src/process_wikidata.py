"""
// Copyright 2020 Twitter, Inc.
// SPDX-License-Identifier: Apache-2.0

Run the below query in BigQuery and export the resulting table output as json file 
"""

import pandas as pd


QUERY_TEMPLATE = """
DECLARE filter_languages ARRAY <STRING>;
SET filter_languages = ["{source}", "{target}"];

WITH tbl AS (
SELECT 
id, descriptions, (
  SELECT ARRAY_AGG(DISTINCT CONCAT(l.value, " ", d.value)) AS unique_l_desc
  FROM (SELECT language AS lang, value FROM UNNEST(descriptions)) AS d
  JOIN (SELECT language AS lang, value FROM UNNEST(labels)) AS l
  USING(lang)
  WHERE lang IN UNNEST(filter_languages)
) AS unique_label_desc
FROM `bigquery-public-data.wikipedia.wikidata`
)

SELECT 
id, unique_label_desc,
FROM tbl
WHERE ARRAY_LENGTH(unique_label_desc) = ARRAY_LENGTH(filter_languages)
"""


def process(
    source, target, file_prefix=None, data_dir="../data/wikidata", project_id=None
):
    if file_prefix is None:
        file_prefix = f"{source[:2]}_{target[:2]}"

    query = QUERY_TEMPLATE.format(source=source, target=target)
    df = pd.read_gbq(query, project_id=project_id)

    df.to_json(f"{data_dir}/{file_prefix}_wikidata.json", orient="records", lines=True)
