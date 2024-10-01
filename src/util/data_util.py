import pandas as pd

def save_content_to_path(content, path):
    if isinstance(content, pd.DataFrame):
        with open(path, "w") as f:
            content.to_csv(f, index=False)
    return