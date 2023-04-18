import pandas as pd

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
df_drop.dropna(inplace=True)
df_drop.to_csv("models/model_data/dataset/course_recommendation/preprocessed_data.csv")
