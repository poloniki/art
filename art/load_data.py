import pandas as pd
from art.params import *


def load_data(path):
    data = pd.read_csv(
        path,
        delimiter="\t",
        encoding="utf-8",
        on_bad_lines="skip",
        header=None,
        names=COLUMN_NAMES,
    )

    return data
