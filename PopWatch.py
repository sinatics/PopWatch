import requests,re,time,os
import ConfigParser
from bs4 import BeautifulSoup
from pushbullet import Pushbullet

#Import API key from key.ini
config = ConfigParser.ConfigParser()
file = (os.path.join(os.getcwd(),'key.ini'))
config.read(file)
apiKey = config.get("data", "apiKey")

timeout = [] #Define global timeout list, this list is used to blacklist pops once they've sent one notification so you don't get 100 notifications for an in stock pop.

def PushText(Title,Message):
    global apiKey
    pb = Pushbullet(apiKey)
    push = pb.push_note(Title, Message)

def PushLink(Title,Link):
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

def CheckFunko(Site,Title,url):
    global timout
    print(Site+" "+Title+" "+url)

    if Site == 'Hot Topic':
        status = HotTopicStock(url)
    elif Site == 'BoxLunch':
        status = BoxLunchStock(url)
    else:
        status = False
    if status == True:
        PushLink(Site+" - In Stock: "+Title,url)
        timeout.append(Title)

def run():
    while True:
        global timeout
        funkos = [('Hot Topic','Anti-Venom Exclusive','http://www.hottopic.com/product/funko-marvel-pop-anti-venom-vinyl-bobble-head-hot-topic-exclusive/10398985.html'),
              ('Hot Topic','Carnage Exclusive','http://www.hottopic.com/product/funko-marvel-pop-carnage-vinyl-bobble-head-hot-topic-exclusive/10398983.html'),
              ('BoxLunch','Anti-Venom GITD Exclusive','http://www.boxlunchgifts.com/product/funko-pop-marvel-anti-venom-vinyl-bobble-head/10519590.html')]

        for i in range(len(funkos)):
            Site, Title, url = funkos[i][0], funkos[i][1], funkos[i][2]
            if Title not in timeout:
                CheckFunko(Site, Title, url)
        time.sleep(60) #Sleep for 1 minute then loop.

if __name__ == '__main__':
    run()