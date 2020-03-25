import requests

URLS = {
    "cases.xlsx": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTfinng5SDBH9RSJMHJk28dUlW3VVSuvqaBSGzU-fYRTVLCzOkw1MnY17L2tWsSOppHB96fr21Ykbyv/pub?output=xls"  # noqa
}

for fn, url in URLS.items():
    print(f"DOWNLOADING '{fn}'...")
    r = requests.get(url, allow_redirects=True)

    with open(fn, 'wb') as fp:
        fp.write(r.content)
