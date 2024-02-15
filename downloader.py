# Author: Kunal Kumar
# Buy Me a Coffee: https://www.buymeacoffee.com/l1v1n9h311
# Social: twitter.com/l1v1n9h311, instagram.com/prokunal
# Website: procoder.in
import requests
import json
from pytube import YouTube
from pytube import Playlist
import os
import threading
import re,sys


def download_video(lesson):
    #print(f"Downloading: {lesson['name']} - YouTube Id: {lesson['youtube_id']}")
    yt = YouTube("https://www.youtube.com/watch?v=" + str(lesson['youtube_id']))
    ys = yt.streams.get_highest_resolution()
    filename = ys.download()
    print(f"{filename} downloaded")
    regex = re.compile(r'[a-zA-Z0-9\s]+')
    os.rename(filename,''.join(regex.findall(lesson['name']))+"."+filename.split(".")[-1])

def download_unit(data):
    for unit in data["data"]["units"]:
        #print(f"Unit {unit['id']}: {unit['name']}")
        regex = re.compile(r'[a-zA-Z0-9\s]+')
        dir_name = ''.join(regex.findall(unit['name']))
        os.mkdir(dir_name)
        os.chdir(dir_name)
        threads = []

        for lesson in unit["lessons"]:
            thread = threading.Thread(target=download_video, args=(lesson,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        os.chdir("..\\")

if __name__ == "__main__":
    url = input("Enter course url: ").split("/")[-2]
    url="https://tools.nptel.ac.in/npteldata/course_outline1.php?id="+str(url)
    r = requests.get(url)
    data = json.loads(r.text)
    print("Title: "+data['data']['title']+"\nProfessor: " +data['data']['professor']+"\nInstitute: "+data['data']['institutename'])
    regex = re.compile(r'[a-zA-Z0-9\s]+')
    try:
        os.mkdir(''.join(regex.findall(data['data']['title'])))
        os.chdir(''.join(regex.findall(data['data']['title'])))
    except Exception as e:
        print("Error Found, Pleaes fix this issue: "+str(e))
        sys.exit()
    syllabus = data['data']['syllabus_url']
    open(syllabus.split("/")[-1],'wb').write(requests.get(syllabus).content)
    print("Syllabus Downloaded: " +syllabus.split("/")[-1])
    print()
    download_unit(data)
