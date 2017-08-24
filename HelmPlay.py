from selenium import webdriver
from time import sleep
from threading import Thread


'''
play               x
pause              x
add yt             x
add search         x
add file
open folder
open recent
delete first
delete current
delete last
delete #
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
#
quit
'''

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
    driver2.switch_to.frame(driver2.find_element_by_xpath('//embed'))
    title = driver2.find_element_by_xpath('//a[@data-sessionlink="feature=player-title"]').text
    global playlist
    playlist.append(("url", title, video))
    print("added " + title)

def add_search(search):
    driver2.get("https://www.youtube.com/results?search_query=" + search)
    link = driver2.find_elements_by_css_selector('.yt-uix-tile-link.yt-ui-ellipsis.yt-ui-ellipsis-2.yt-uix-sessionlink')[0].get_attribute("href")[32:]
    add_yt(link)

def play_yt(video):
    global IO
    driver.get("https://www.youtube.com/watch?v=" + video)
    video_ended = False
    sleep(1)
    while not video_ended or not IO:
        element = driver.find_element_by_class_name("ytp-progress-bar")
        video_ended = element.get_attribute("aria-valuenow") == element.get_attribute("aria-valuemax")
    sleep(1)
    driver.get("about:blank")
    return

def play(item):
    global playlist
    print("now playing " + str(item) + ") " + playlist[item][1])
    if playlist[item][0] == "url":
        play_yt(playlist[item][2])
    else:
        pass
    return
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
