# Author
# Praneet Kumar, B.Tech CSE
# NIT Silchar, Class of 2019

from pytube import YouTube
from selenium import webdriver
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.youtube.com/watch?v=4FB1nO6ckZI&index=1&list=PLKQEL9j11yiUQ5SWdkc6ZT6A1NRoaskst"  # Enter video URL.
count = 1
''' 
In case the download fails in between due to connectivity issues, update the url with the next file to be downloaded,
and modify the name variable according to the name of the last downloaded file.
Eg. If your download fails for the 21st video in a 50 video playlist, update the url with the 21st video's link and
change the name variable to '21' from '1'.
'''
name = 1
SAVE_PATH = "E:/YouTube/Spanish Lessons"                # The path where the videos are to be saved.

driver = webdriver.Chrome('E:\Python\chromedriver.exe')        # Initialize chromedriver.
# driver.set_window_position(-10000, 0)
driver.get(url)

while count >= 1:

    try:                                                       # Establish connection.
        yt = YouTube(url)
    except:
        print("Connection error!")

    mp4files = yt.filter('mp4')                                # Target the best available mp4 quality.
    yt.set_filename(str(name))
    d_video = yt.get(mp4files[-1].extension, mp4files[-1].resolution)

    try:                                                       # Download and save the video in the desired path.
        d_video.download(SAVE_PATH)
    except:
        print("Connection error!")

    # print("Video " + str(name) + " downloaded.")
    try:
        WebDriverWait(driver, 15).until(               # Explicit wait to ensure that page has fully loaded
            EC.presence_of_element_located((By.LINK_TEXT, "dummy text"))
        )
    except:
        pass

    for i in driver.find_elements_by_css_selector('.index-message.style-scope.ytd-playlist-panel-renderer'):
        status = i.text + " downloaded." + "\n"
        print(status)                                     # Print the download status.

        a = re.findall(r'\d+', status)                    # Check if the entire playlist has been downloaded.
        if a[0] == a[1]:
            print("Task completed!!")
            driver.quit()
            exit()

    for i in driver.find_elements_by_css_selector('.ytp-next-button.ytp-button'):       # Get the link of next video
        url = i.get_attribute('href')                                                   # in playlist.
        name += 1
        try:
            time.sleep(5)
            i.click()
        except:
            time.sleep(10)
            i.click()
        break