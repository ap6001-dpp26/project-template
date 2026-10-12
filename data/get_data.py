"""Download the project's raw data into data/raw/.

Edit URL and FILE. Raw data are not committed (see .gitignore): this script is how anyone who
reproduces the project obtains them. If the data cannot be downloaded by a script, replace this
file's body with a docstring that gives the exact steps, and say so in the README.

Run with:  uv run python data/get_data.py
"""

import zipfile
from pathlib import Path
from urllib.request import urlretrieve

URL = "https://..."  # the official download link (INEGI, CONEVAL, datos.gob.mx, ...)
FILE = "data.zip"  # the name to save it under

RAW = Path(__file__).resolve().parent / "raw"


def main():
    if URL == "https://...":
        raise SystemExit("Edit URL and FILE in data/get_data.py first.")
    RAW.mkdir(parents=True, exist_ok=True)
    target = RAW / FILE
    if not target.exists():
        print(f"downloading {URL}")
        urlretrieve(URL, target)
    if target.suffix == ".zip":
        with zipfile.ZipFile(target) as z:
            z.extractall(RAW)
    print(f"data in {RAW}")


if __name__ == "__main__":
    main()
