import requests,json,re,time,sys
from bs4 import BeautifulSoup
from pushbullet import Pushbullet

#Import API key from key.json
with open('key.json') as key_file:
    key = json.load(key_file)

apiKey = key['apiKey']

timeout = [] #Define global timeout list, this list is used to blacklist pops once they've sent one notification so you don't get 100 notifications for an in stock pop.


def push_text(Title, Message):
    global apiKey
    pb = Pushbullet(apiKey)
    push = pb.push_note(Title, Message)


def push_link(Title, Link):
    global apiKey
    pb = Pushbullet(apiKey)
    push = pb.push_link(Title, Link)


def url_to_html(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def hottopic_stock(url):
    soup = url_to_html(url)
    html_source = soup.find_all("div", {"class" : "availability-msg"})
    match = re.search(r'\bIn Stock\b',str(html_source))
    if match: #Return true if In Stock
        return True
    else: #Return false if Out of Stock
        return False


def boxlunch_stock(url):
    soup = url_to_html(url)
    html_source = soup.find_all("div", {"class": "availability"})
    match = re.search(r'\bIn Stock\b', str(html_source))
    if match: #Return true if In Stock
        return True
    else: #Return false if Out of Stock
        return False


def walmart_stock(url):
    soup = url_to_html(url)
    html_source = soup.find_all("div", {"class": "prod-ProductPrimaryCTA"})
    match = re.search(r'\bAdd to Cart\b',str(html_source))
    if match: #Return True if in stock
        return True
    else: #Return False if out of stock
        return False

def barnesandnoble_stock(url):
    soup = url_to_html(url)
    html_source = soup.find_all("section", {"id": "skuSelection"})
    match = re.search(r'\bAdd to Bag\b',str(html_source))
    if match: #Return True if in stock
        return True
    else: #Return False if out of stock
        return False


def gamestop_stock(url):
    soup = url_to_html(url)
    html_source = soup.find_all("div", {"class": "button qq"})
    match = re.search(r'\bAdd to Cart\b',str(html_source))
    if match: #Return True if in stock
        return True
    else: #Return False if out of stock
        return False


def CheckFunko(Site, Title, url):
    global timout
    print("Checking: "+Site+" "+Title+" "+url)

    if Site == 'Hot Topic':
        status = hottopic_stock(url)
    elif Site == 'BoxLunch':
        status = boxlunch_stock(url)
    elif Site == 'Walmart':
        status = walmart_stock(url)
    elif Site == 'Barnes and Noble':
        status = barnesandnoble_stock(url)
    elif Site == 'GameStop':
        status = gamestop_stock(url)
    else:
        status = False
    if status == True:
        push_link(Site + " - In Stock: " + Title, url)

        # Set timeout for found pops, this prevents any future pushbullet notifications from going out.
        timeout.append(Title)
        print("Timeout Set: "+Site+" "+Title)


def pop_search(funkopop_links, sleep_interval=60):
    while True:
        global timeout

        for i in funkopop_links:
            if i['PopName'] not in timeout:
                CheckFunko(i['Store'], i['PopName'], i['URL'])
        time.sleep(sleep_interval) #Sleep for 1 minute (default unless defined) then loop.


if __name__ == '__main__':
    # Load in items from pops.json
    with open('pops.json') as data_file:
        json_pops = json.load(data_file)

    # Set sleep interval if defined as an argument and start pop_search, which runs once every "sleep_interval" on the links specified in pops.json
    if len(sys.argv) > 1:
        pop_search(json_pops, int(sys.argv[1]))
    else:
        pop_search(json_pops)