# Function to convert to lowercase with underscores
def convert_style(style):
    return (
        style.lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "_")
    )


def clean_data(data):

    data = data.dropna(
        subset=["Art Movement"],
    )
    data = data.drop(
        [
            "Theme",
            "Period",
            "Family and Relatives",
            "Series",
            "Pupils",
            "Teachers",
            "Original Title",
            "Dimensions",
            "Friends and Co-workers",
            "Influenced by",
            "Influenced on",
        ],
        axis=1,
    )

    return data


def get_most_common(data, column, thresh):
    perc = data[column].value_counts(normalize=True).cumsum()
    top = list(perc[perc < thresh].keys())
    top_df = data.loc[data[column].isin(top)]
    top_df[column] = top_df[column].apply(convert_style)

    return top_df
