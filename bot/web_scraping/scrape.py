# bossbadi's discord bot: everything web scraping related

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


# ---scrape chat bot---#
def scrape_math(content):
    if content.startswith("=calc"):
        content = content[5:]
    else:
        content = content[2:]

    if content == '':
        ans = None
        return ans

    content = content.replace('×', '*')
    content = content.replace('x', '*')
    content = content.replace('÷', '/')

    url = "https://api.mathjs.org/v4/?expr="
    problem = quote(content, safe='')
    url += problem
    source = requests.get(url).text
    soup = str(BeautifulSoup(source, 'html.parser'))
    ans = f"{content} = **{soup}**"
    if len(ans) > 2000: ans = ans[:1997] + "..."
    return ans