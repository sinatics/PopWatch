import requests,json,re,time,sys
from bs4 import BeautifulSoup
from pushbullet import Pushbullet

#Import API key from key.json
with open('key.json') as key_file:
    key = json.load(key_file)

apiKey = key['apiKey']

timeout = [] #Define global timeout list, this list is used to blacklist pops once they've sent one notification so you don't get 100 notifications for an in stock pop.

def PushText(Title,Message):
    global apiKey
    pb = Pushbullet(apiKey)
    push = pb.push_note(Title, Message)

def PushLink(Title, Link):
    global apiKey
    pb = Pushbullet(apiKey)
    push = pb.push_link(Title, Link)

def urlTohtml(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def HotTopicStock(url):
    soup = urlTohtml(url)
    html_source = soup.find_all("div", {"class" : "availability-msg"})
    match = re.search(r'\bIn Stock\b',str(html_source))
    if match: #Return true if In Stock
        return True
    else: #Return false if Out of Stock
        return False

def BoxLunchStock(url):
    soup = urlTohtml(url)
    html_source = soup.find_all("div", {"class": "availability"})
    match = re.search(r'\bIn Stock\b', str(html_source))
    if match: #Return true if In Stock
        return True
    else: #Return false if Out of Stock
        return False

def WalmartStock(url):
    soup = urlTohtml(url)
    html_source = soup.find_all("div", {"class": "prod-ProductPrimaryCTA"})
    match = re.search(r'\bAdd to Cart\b',str(html_source))
    if match: #Return True if in stock
        return True
    else: #Return False if out of stock
        return False

def CheckFunko(Site, Title, url):
    global timout
    print("Checking: "+Site+" "+Title+" "+url)

    if Site == 'Hot Topic':
        status = HotTopicStock(url)
    elif Site == 'BoxLunch':
        status = BoxLunchStock(url)
    elif Site == 'Walmart':
        status = WalmartStock(url)
    else:
        status = False
    if status == True:
        PushLink(Site+" - In Stock: "+Title,url)

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