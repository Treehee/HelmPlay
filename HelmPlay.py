from selenium import webdriver
from time import sleep
driver = webdriver.Chrome()

playlist = []
'''
play
pause
add yt
add search
add file
open folder
open recent
delete first
delete current
delete last
delete #
save
install
replay on
replay off
replay toggle
shuffle off
shuffle on
shuffle toggle
skip
playfrom
#
'''
count = 0
def add_yt(video):
    global count
    driver.execute_script("window.open('about:blank', 'tab" + str(count) + "');")
    count += 1
    driver.switch_to_window(driver.window_handles[1])
    driver.get("https://www.youtube.com/v/" + video)
    driver.switch_to.frame(driver.find_element_by_xpath('//embed'))
    title = driver.find_element_by_xpath('//a[@data-sessionlink="feature=player-title"]').text
    global playlist
    playlist.append((title, video))
    driver.close()
    driver.switch_to_window(driver.window_handles[0])

def add_search(search):
    global count
    driver.execute_script("window.open('about:blank', 'tab" + str(count) + "');")
    count += 1
    driver.switch_to_window(driver.window_handles[1])
    driver.get("https://www.youtube.com/results?search_query=" + search)
    link = driver.find_elements_by_css_selector('.yt-uix-tile-link.yt-ui-ellipsis.yt-ui-ellipsis-2.yt-uix-sessionlink')[0].get_attribute("href")[32:]
    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    add_yt(link)

def play(item):
    global playlist
    print("Now playing " + str(item + 1) + ") " + playlist[item][0])
    driver.switch_to_window(driver.window_handles[0])
    driver.get("https://www.youtube.com/watch?v=" + playlist[item][1])
    video_ended = False
    while not video_ended:
        element = driver.find_element_by_class_name("ytp-progress-bar")
        video_ended = element.get_attribute("aria-valuenow") == element.get_attribute("aria-valuemax") and element.get_attribute("aria-valuemax") != None
    sleep(1)
    driver.get("about:blank")

add_search("mooi")
add_search("katy perry roar")
print(playlist)
play(0)
play(1)
driver.quit()
