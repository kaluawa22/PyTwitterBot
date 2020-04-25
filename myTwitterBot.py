
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
from time import sleep
import random
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import json
import threading

#Kalu Awa

print("This is my Twitter Bot")


#This is a simple twitter bot that posts tweets based on a set interval from a text file
#More functionality will be added soon

CONSUMER_KEY = '7tr56KY7FKMjDnafPmfPRaqAh'
CONSUMER_SECRET = 'lE9YPRch0Sa1EiXF3DkOuAeLUpL4KKotz9RFxYPmxKNCfVHK4B'
ACCESS_KEY = '1246567239341441032-kwimhmtF3tMHkmsIopOcFMiM9tmo9h'
ACCESS_SECRET = 't50X5FO4EczihRHz4QudDOpXAxrTJDEeKj856Udzi0PUl'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


#### Code for the video downloader
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json',json.dumps(raw))
    return status




















#####Tweepy active Stream Creation Code. This will allow me to stream data from twitter in real time.
class StdOutListener(tweepy.StreamListener):


    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

############################*****************************************************#


def isValidUrl(url):        # Checks to see if the given url is valid
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)




def getAllImages(url):
    soup = bs(requests.get(url).content, "html.parser")
    urls = []

    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:     #if the image does not contain src attribute, just skip over it
            continue

        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        if isValidUrl(img_url):
            urls.append(img_url)
    return urls

def download(url, pathname):
    #if a path does not exist , make that path dir

    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    #Download the body of reponse by chunk, not immediately
    response = requests.get(url, stream = True)
    # get the total file size

    file_size = int(response.headers.get("Content-Length", 0))

    #get the file name

    filename = os.path.join(pathname, url.split("/")[-1])

    #Progress bar, changing the unit to bytes instead of iteration(Default by Tqdm)

    progress = tqdm(response.iter_content(buffer_size), f"Download {filename}", total = file_size, unit = "B", unit_scale = True, unit_divisor = 1024)

    with open(filename, "wb") as f:
        for data in progress:
            #Write data read to the file
            f.write(data)
            #Update the progress bar manually
            progress.update(len(data))


def main(url, path):
    #Get all images
    imgs = getAllImages(url)
    for img in imgs:
        #for each image , download it
        download(img, path)





def postStatus(status):
    print(status[0])



def openQuoteFile(inputFile, fixedlst):
    lst = []
    f_read = open(inputFile, "r")
    for i in f_read:
        lst.append(i)
    for element in lst:
        fixedlst.append(element.strip())

    return fixedlst


notDoneTweeting = True
startTime = time.time()
quoteArray = []
openQuoteFile("quotes.txt", quoteArray)
mentions = api.mentions_timeline(count = 1)
buffer_size = 1024

sampledList = random.sample(quoteArray,len(quoteArray)) #randomizes the quoteArray each time the program is run

# main("https://www.pexels.com/search/dog/", "web-scraping")

for i in range(len(quoteArray)):
    randomNum = random.randint(0, len(quoteArray))
    newStatus = api.update_status(sampledList[i] + " " + "KaluBot") # prints status with a random number
    print(sampledList[i] + str(randomNum))                                             #This deals with twitter duplicate tweets/testing purposes only

    print(randomNum)
    sleep(10)       #Number of seconds of sleep till the for loop iterates

# for mention in mentions:
#     print(str(mention.id) + mention.text)
#



updateStatus = api.update_status(newStatus)

######Twitter Stream Initialization####################
myStreamListener = StdOutListener()

myStream = tweepy.Stream(auth = api.auth, listen = myStreamListener)


if __name__ == '__main__':
    s = []




