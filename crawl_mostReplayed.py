import warnings
warnings.filterwarnings('ignore')
from selenium import webdriver
from bs4 import BeautifulSoup
import sys
import os
from pathlib import Path
import pdb
import subprocess
import argparse
from ast import literal_eval

def crawl_mostreplayed(chrome_options, youtube_id, chdv_loc="./chromedriver"):
    chromeDriver = webdriver.Chrome(chdv_loc, chrome_options=chrome_options)
    chromeDriver.get(f"https://yt.lemnoslife.com/videos?part=mostReplayed&id={youtube_id}")
    html = chromeDriver.page_source
    html_page = BeautifulSoup(html, 'html.parser')
    body = html_page.select_one('body')
    bodydict = literal_eval(body.get_text())
    mostReplayed_list = bodydict['items'][0]["mostReplayed"]['heatMarkers']
    return mostReplayed_list

def get_time(mostReplayed_list):
    score_list = []
    for idx, data in enumerate(mostReplayed_list):
        data_real = data['heatMarkerRenderer']
        if data_real['timeRangeStartMillis'] == 0:
            # ignore the start poinit
            continue
        heat_score = data_real['heatMarkerIntensityScoreNormalized']
        score_list.append(heat_score)
    tmp = max(score_list)
    max_index = score_list.index(tmp)
    target_data = mostReplayed_list[max_index+1]['heatMarkerRenderer']

    start_time = target_data['timeRangeStartMillis']
    start_time_sec = start_time / 1000
    duration = target_data['markerDurationMillis']
    duration_sec = duration / 1000    
    return start_time_sec, duration_sec

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--youtube_id', type=str, help='id from Youtube address') 
    parser.add_argument('-c', '--chromedv_loc', type=str, default='./chromedriver', help='location of chromedriver')

    args= parser.parse_args()

    youtube_id = args.youtube_id
    chdv_loc = args.chromedv_loc

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless') # 웹 브라우저를 띄우지 않는 headless 
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    try:
        mostReplayed_list = crawl_mostreplayed(chrome_options, youtube_id, chdv_loc)
        start_time, duration = get_time(mostReplayed_list)
        end_time = start_time + duration
        youtube_address = "https://youtu.be/" + youtube_id
        print(f"Youtube address: {youtube_address}")
        print(f"Most Replayed Scene: {start_time}sec ~ {end_time}sec")
    except:
        print(f"There is no 'Most replayed' scene")