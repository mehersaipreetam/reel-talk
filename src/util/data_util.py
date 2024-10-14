import pandas as pd

def save_content_to_path(content, path):
    """
    Saves content to a file at the given path.

    Parameters
    ----------
    content : str or pd.DataFrame
        The content to be saved to a file.
    path : str
        The path to the file to be saved.

    Returns
    -------
    None
    """
    if isinstance(content, pd.DataFrame):
        with open(path, "w") as f:
            content.to_csv(f, index=False)
    return