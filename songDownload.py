"""
download songs from djpunjab.is
works most of the time
"""

# from selenium import webdriver as wd
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# from string import capwords
import os, glob
# # from bs4 import BeautifulSoup
#
# # def remove_ads(driver, html):
# #     soup = BeautifulSoup(html, "html.parser")
# #
# #     # Remove the elements containing ads
# #     for ad in soup.select(".ad"):
# #         ad.decompose()
# #
# #     # Save the modified HTML
# #     modified_html = str(soup)
# #
# #     # Overwrite the HTML of the web page with the modified HTML
# #     driver.execute_script(f"document.documentElement.innerHTML = {modified_html!r}")
#
# def latest_download_file():
#     path = fr"C:\Users\{os.getenv('username')}\Downloads"
#     os.chdir(path)
#     files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
#     newest = files[-1]
#
#     return newest
#
# def check_download_complete():
#     fileends = "crdownload"
#     while "crdownload" == fileends:
#         time.sleep(1)
#         newest_file = latest_download_file()
#         if "crdownload" in newest_file:
#             fileends = "crdownload"
#         else:
#             fileends = "none"
#
#
# def songDownload(song_name, singer):
#     """
#     takes the song name and the name of the singer.
#     if name of singer is not known, False is sent as argument to songDownload()
#     uses selenium to download songs from "https://djpunjab.is"
#     """
#
#     browser = wd.Chrome()
#     browser.get("https://djpunjab.is")
#     browser.minimize_window()
#     # time.sleep(2)
#
#     # remove_ads(browser, browser.page_source)
#     browser.implicitly_wait(10)
#     search = browser.find_element(By.NAME, "search")
#     search.send_keys(f"{song_name} {singer if singer else ''}")
#     search.send_keys(Keys.RETURN)
#
#     # wait for site to load
#     time.sleep(3)
#     # remove_ads(browser, browser.page_source)
#
#     wait = WebDriverWait(browser, 7)
#     try:
#         try:
#             link_click = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, f"{capwords(song_name)}")))
#         except:
#             if singer:
#                 link_click = browser.find_element(By.PARTIAL_LINK_TEXT, f"{capwords(singer)}")
#             else: pass
#     except:
#         try:
#             link_click = browser.find_element(By.PARTIAL_LINK_TEXT, "song download")
#         except:
#             return False
#     # browser.find_element(By.PARTIAL_LINK_TEXT, f"{capwords(song_name)}")
#     link_click.click()
#     window_handles = browser.window_handles
#
#     browser.switch_to.window(window_handles[1])
#     try:
#         download_link = browser.find_element(By.PARTIAL_LINK_TEXT, "Download In 320 Kbps")
#     except:
#         try:
#             try:
#                 download_link = browser.find_element(By.PARTIAL_LINK_TEXT, "Get In 320 Kbps")
#             except:
#                 try:
#                     download_link = browser.find_element(By.PARTIAL_LINK_TEXT, "320 Kbps")
#                 except:
#                     download_link = browser.find_element(By.PARTIAL_LINK_TEXT, "128 Kbps")
#         except:
#             return False
#     try:
#         download_link.click()
#     except:
#         return False
#     check_download_complete()
#     return True

# super sexy method
# works 99.9% times if song name is genuine
def ultimateSongDownload(song_name):
    """
    downloads songs using spotdl
    if song name is genuine, downloads the song
    if song name is not available or fake, does not throw an error but displays so
    """
    # location to the Music directory. This is where all the songs will be downloaded
    loc = fr"C:\Users\{os.getlogin()}\Music"
    os.chdir(loc)
    os.system(fr'spotdl "{song_name}"')

    # finding the latest file, which will be the music file we downloaded (if it downloads, hopefully)
    list_of_files = glob.glob(loc + '/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file