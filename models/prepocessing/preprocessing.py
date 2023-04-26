import pandas as pd
import string

df = pd.read_csv("models/model_data/dataset/course_recommendation/all_courses.csv")
df_drop = df.drop(
    [
        "Type",
        "Level",
        "Duration",
        "Rating",
        "Review Count",
        "Skills Covered",
        "Prerequisites",
        "Affiliates",
        "URL",
    ],
    axis=1,
)


def preprocess_data(df, col_list):
    for col in col_list:
        df[col] = df[col].str.lower()
        df[col].str.replace("[{}]".format(string.punctuation), "")
    return df


df_drop = preprocess_data(df_drop, ["Title", "Description"])
df_drop.dropna(inplace=True)
df_drop.to_csv("models/model_data/dataset/course_recommendation/preprocessed_data.csv")
