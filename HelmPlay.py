from selenium import webdriver
from time import sleep
from threading import Thread
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


'''
play               x
pause              x
add yt             x
add search         x
add file
open folder
open recent
delete
save
download
replay on          x
replay off         x
replay toggle      x
shuffle off
shuffle on
shuffle toggle
skip
playfrom
#                  x
quit               x
'''
def  number(value):
    global playlist
    if value == "first":
        return 0
    elif value == "last":
        return len(playlist)-1
    elif value == "current":
        return current%len(playlist)
    elif value == "next":
        return (current+1)%len(playlist)
    elif value == "previous":
        return (current-1)%len(playlist)
    else:
        try:
            return int(value) - 1
        except:
            return None

def userinput():
    global replay
    global current
    global IO
    global playlist
    global userin
    while not userin == "quit":
        userin = input()
        if userin.startswith("add search "):
            add_search(userin[11:])
        elif userin == "play":
            print("playing...")
            IO = True
        elif userin == "pauze":
            print("pauzed")
            IO = False
        elif userin.startswith("add yt "):
            add_yt(userin[7:])
        elif userin == "replay on":
            print("replay is now turned on")
            replay = True
        elif userin == "replay off":
            print("replay is now turned off")
            replay == False
        elif userin == "replay toggle":
            replay = not replay
            print("replay is now turned " + replay*"on" + (not replay)*"off")
        elif userin.startswith("#"):
            if len(playlist) == 0:
                print("playlist doesn't contain any songs yet")
            else:
                if number(userin[1:]) is None:
                    print("Invalid number")
                else:
                    try:
                        print("song " + str(number(userin[1:]) + 1) + ") is called " + playlist[number(userin[1:])][1])
                    except:
                        print("Song index out of range")
        elif userin.startswith("playfrom #"):
            if number(userin[10:]) == None:
                print("Invalid number")
            else:
                IO = False
                sleep(2)
                current = number(userin[10:])%len(playlist)
                IO = True


def player():
    global userin
    global playlist
    global IO
    global replay
    global current
    global song
    while not userin == "quit":
        if song is None:
            if IO and current < len(playlist):
                song = Thread(target = play, args = (current,))
                song.start()
                if replay:
                    current = (current+1)%len(playlist)
                else:
                    current += 1
        else:
            if IO and current < len(playlist) and not song.is_alive():
                song = Thread(target = play, args = (current,))
                song.start()
                if replay:
                    current = (current+1)%len(playlist)
                else:
                    current += 1
                    
        
def add_yt(video):
    driver2.get("https://www.youtube.com/v/" + video)
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//embed'))
        WebDriverWait(driver2, 10).until(element_present)
    except TimeoutException:
        print("Internet connection timed out")
        return
    driver2.switch_to.frame(driver2.find_element_by_xpath('//embed'))
    title = driver2.find_element_by_xpath('//a[@data-sessionlink="feature=player-title"]').text
    global playlist
    playlist.append(("url", title, video))
    print("added " + title)

def add_search(search):
    driver2.get("https://www.youtube.com/results?search_query=" + search)
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, '.yt-lockup.yt-lockup-tile.yt-lockup-video'))
        WebDriverWait(driver2, 10).until(element_present)
    except TimeoutException:
        print("Internet connection timed out")
        return
    videos = driver2.find_elements_by_css_selector('.yt-lockup.yt-lockup-tile.yt-lockup-video')
    if len(videos) == 0:
        print("Search did not yield any results")
    else:
        link = videos[0].find_element_by_css_selector('.yt-uix-tile-link.yt-ui-ellipsis.yt-ui-ellipsis-2.yt-uix-sessionlink').get_attribute("href")[32:]
        add_yt(link)

def play_yt(video):
    global current
    global IO
    driver.get("https://www.youtube.com/watch?v=" + video)
    video_ended = False
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, "ytp-progress-bar"))
        WebDriverWait(driver, 10).until(element_present)
    except TimeoutException:
        print("Internet connection timed out")
        current -= 1
        return
    while not video_ended and IO:
        element = driver.find_element_by_class_name("ytp-progress-bar")
        video_ended = element.get_attribute("aria-valuenow") == element.get_attribute("aria-valuemax")
    sleep(1)
    driver.get("about:blank")

def play(item):
    global playlist
    print("now playing " + str(item+1) + ") " + playlist[item][1])
    if playlist[item][0] == "url":
        play_yt(playlist[item][2])
    else:
        pass
    if not IO:
        global current
        current -= 1
def __init__():
    global playlist
    global current
    global replay
    global IO
    global song
    global driver
    global driver2
    global userin
    userin = None
    driver = webdriver.Chrome()
    driver2 = webdriver.Chrome()
    print("You are using HelmPlay.\nCreated by Merlijn Zander van Helm")
    playlist = []
    current = 0
    replay = True
    IO = False
    song = None
    Thread(target = player).start()
    userinput()
    driver.quit()
    driver2.quit()
__init__()
