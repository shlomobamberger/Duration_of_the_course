import datetime
import pafy
from selenium import webdriver

driver = webdriver.Chrome(r"C:\projects\Eclipse\chromedriver.exe")

# using pafy to get duration of youtube video
# return int - seconds of youtube video duration
def get_duration(url):
    video = pafy.new(url)
    with open("result.txt", 'a', encoding='utf-8') as f:
        f.write("VideoId: " + str(video.videoid) + " Duration " + str(video.duration) + '\n')
    duration_list = str(video.duration).split(":")
    hours = int(duration_list[0])
    minutes = int(duration_list[1])
    seconds = int(duration_list[1])
    final_time = seconds + (minutes * 60) + (hours * 60 * 60)
    return final_time

# get all links and write them to file
def get_links():
    driver.get("https://atidcollege.co.il/digital/qa/ch06-part03-password.html")
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@src='../menus/menu-software-testing.html']"))
    text_list = driver.find_elements_by_xpath("//li[@class='list-group-item']")
    for i in range(len(text_list)):
        try:
            link = text_list[i].find_element_by_tag_name('a').get_attribute("href")
            with open("links.txt", 'a', encoding='utf-8')as f:
                f.write(link + '\n')
        except:
            pass


# use selenium to open page and locate youtube video link
# return boolean - if is youtube or not , and link from youtube or the source link
def get_youtube_link(link):
    driver.get(link)
    frames = driver.find_elements_by_tag_name('iframe')
    is_youtube = False
    for i in frames:
        if "youtube" in i.get_attribute("src"):
            link = i.get_attribute("src")
            link = link.split("/")[-1]
            is_youtube = True
    return is_youtube, link


def main():
    # open file with all links to open
    with open("links.txt", 'r') as links:
        final_duration_in_seconds = 0
        for line in links:
            line = line.replace("\n", "")
            is_youtube_link = get_youtube_link(line)
            # pafy works for youtube only, if video storage in google drive we need to manual calculate
            if is_youtube_link[0]:
                final_duration_in_seconds += get_duration(is_youtube_link[1])
            else:
                print("drive?   " + line)
            # convert seconds to format "HH:MM:SS"
            duration = str(datetime.timedelta(seconds=final_duration_in_seconds))
            print("duration of all youtube videos:  " + duration)


if __name__ == '__main__':
    main()
