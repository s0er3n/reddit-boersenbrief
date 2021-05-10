import pypandoc
import re
import json
from urlextract import URLExtract
from PIL import Image
import requests
from reddit_scraping.redditscraper import give_example_selftext, top10
import os
extractor = URLExtract()

images = []


def replace_reddit_preview_urls_with_image(post_selftext):
    urls = extractor.find_urls(post_selftext)

    for i, url in enumerate(urls):
        try:
            response = requests.request("GET", url)
            filetype = response.headers["Fastly-Io-Info"].split(" ")[2][5:]
            name = f'{i}.{filetype}'
            with open(name, 'wb') as f:
                f.write(response.content)
            images.append((i, name))
        except Exception as e:
            pass

    for i, name in images:
        im = Image.open(name)
        im.save(name)

        post_selftext = post_selftext.replace(urls[i], f'![]({name})')

    return post_selftext


def make_pdf_from_md(md):
    pypandoc.convert_text(
        md, format='md', to="pdf", outputfile="output.pdf", extra_args=['--template', 'eisvogel.latex', "--listings",
                                                                        "--defaults=pdf.yaml", "--pdf-engine=lualatex"])
    for _, image in images:
        os.remove(image)


with open("emoji.json") as f:
    emojis = json.load(f)


def replace_emojis(md):
    md = md
    for emoji in emojis:
        if emoji["description"]:
            md = md.replace(
                emoji["emoji"],  " \\emoji{" + emoji["description"].replace(": ", "-").replace(" ", "-").lower() + "}")
    return md


def link_ticker(md):
    ticker_in_text = set(re.findall(r'[$][A-Za-z][A-Za-z.0-9]*', md))
    print(ticker_in_text)
    for ticker in ticker_in_text:
        print(ticker)
        md = md.replace(
            ticker, f" [{ticker}](https://de.finance.yahoo.com/quote/{ticker[1:]})")
    return md


if __name__ == "__main__":
    md = " ".join(top10("Wallstreetbets"))
    md = replace_emojis(md)
    md = replace_reddit_preview_urls_with_image(
        md)
    md = link_ticker(md)
    print(md)
    make_pdf_from_md(md)
