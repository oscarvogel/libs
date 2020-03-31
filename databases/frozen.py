import os
import pathlib
import json
import datetime as dt

import requests


PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

URLS = {
    "cases.xlsx": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTfinng5SDBH9RSJMHJk28dUlW3VVSuvqaBSGzU-fYRTVLCzOkw1MnY17L2tWsSOppHB96fr21Ykbyv/pub?output=xls",  # noqa
    "cases.csv": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTfinng5SDBH9RSJMHJk28dUlW3VVSuvqaBSGzU-fYRTVLCzOkw1MnY17L2tWsSOppHB96fr21Ykbyv/pub?output=csv"  # noqa
}

UPDATES_FNAME = "updates.json"


def frozen(path=PATH):
    if not isinstance(path, pathlib.Path):
        path = pathlib.Path(path)

    updates = {}
    updates_path = path / UPDATES_FNAME

    for fn, url in URLS.items():
        fpath = path / fn
        if updates_path == fpath:
            raise ValueError(f"Colision {updates_path} <-> {fpath}")

        print(f"DOWNLOADING '{fpath}'...")
        r = requests.get(url, allow_redirects=True)

        with open(fpath, 'wb') as fp:
            fp.write(r.content)

        updates[fn] = dt.datetime.utcnow().isoformat()

    with open(updates_path, "w") as fp:
        print(f"Writing {updates_path}...")
        json.dump(updates, fp, indent=2)


if __name__ == "__main__":
    frozen()
