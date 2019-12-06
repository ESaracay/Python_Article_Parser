import urllib.request
from urllib.parse import urlparse
import sys

def opensite(site):
    '''
    This is the heart of the application which takes writes
    a file with your news inside
    '''
    site_info = urlparse(site)
    # check if our site is fake news
    if FakeNews(site_info[1]):
        return print("Warning this is a fake News Website")
    # if clear then create a new file with website name as title
    f = open(site_info[1]+'.txt', "w+")
    raw_text = urllib.request.urlopen(site)
    text = raw_text.read().decode('utf-8')
    # we only want to look at the body
    begin = text.find('<body')
    end = text.find('</body', begin)
    text = text[begin:end]
    maintext = filter(text)
    secondtext = filter2(text)
    # going off the assumption that the more text the better
    if len(maintext) > len(secondtext):
        maintext = imgfilter(maintext)
        [f.write(line+'\n') for line in maintext]
    else:
        secondtext = imgfilter(secondtext)
        [f.write(line+'\n') for line in secondtext]
def FakeNews(netloc):
    """
    Based of Wikipedia(https://en.wikipedia.org/wiki/List_of_fake_news_websites)
     page that gives a list of known Fake
    news sites, check if our netloc is in this list
    """
    # This is just part of the list
    fake =["70News.com", "americannews.com", "beforeitsnews.com", "ABCnews.com.co","bizstandardnews.com","bients.com"]
    if netloc in fake:
        return True
    return False


def imgfilter(lines):
    '''
    This gets rid of imgages and information that
    often comes along with the body of news articles
    '''
    newlist =[]
    for line in lines:
        if 'href' not in line and 'src=' not in line and 'd=' not in line:
            newlist.append(line)
    return newlist

def filter(string):
    # do more filtering by getting rid of any <anything thats not <p in string
    """
    This filter is used when paragraph tag has additional information
    """
    search = 0
    site_text = []
    while True:
        begin = string.find('<p ', search)
        if begin == -1:
            break
        start = string.find('>', begin)
        # must find the beginning of paragraph from end
        end = string.find('</p', begin)
        real_text = string[start + 1: end]
        site_text.append(real_text)
        search = end
    return site_text

def filter2(string):
    """
    This filter is used in the case where <p> is your tag with no additional
    information within tag
    """
    search = 0
    site_text = []
    while True:
        begin = string.find('<p>', search)
        if begin == -1:
            break
        # must find the beginning of paragraph from end
        end = string.find('</p', begin)
        # while begin > search and string[begin] != '>':
        # begin = begin - 1
        real_text = string[begin + 3: end]
        site_text.append(real_text)
        search = end
    return site_text


def main():
    #  use terminal and simply add URL link as a parameter
    #args = sys.argv[1:]
    #if len(args)==1:
        #opensite(args[0])
    site = input(" Enter the URL of your News Article")
    opensite(site)


if __name__ =="__main__":
    main()