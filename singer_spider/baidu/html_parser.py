# -*- coding:utf-8 -*-

import re
import uuid
import time
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('main')
class HtmlParser(object):
    def parseSingerListPage(self, soup):
        reDatas = []
        ul_tag = soup.find("ul", class_="container")
        a_tags = ul_tag.find_all("a", href=re.compile(r"/artist/"))
        # print(a_tags)
        for a_tag in a_tags:
            if a_tag.has_attr('title'):
                reData = {}
                reData['id'] = uuid.uuid1()
                reData['time'] = time.time()
                reData['href'] = 'http://music.baidu.com' + a_tag['href']
                reData['name'] = a_tag['title']
                reDatas.append(reData)
                # print(reData)
        return reDatas

    def parserSingerPage(self, soup):
        reData = {}
        if soup is None:
            return None
        #歌手类型
        div_music_body = soup.find("div", class_="music-body")
        if div_music_body is None:
            return None

        reData['type'] = ''
        div_artist_info = div_music_body.find("div", class_="artist-info")
        if div_artist_info is None:
            return None
        div_artist_img_box = div_artist_info.find("div", class_="artist-img-box")
        reData["img"] = div_artist_img_box.img["src"]

        div_artist_detail_box = div_artist_info.find('div', class_="artist-detail-box")
        span_hot = div_artist_detail_box.find("span", class_="hot-nums-detail")
        reData['hot'] = span_hot.get_text()

        div_pop_introduce = div_artist_info.find('div', class_='pop-introduce')
        if div_pop_introduce is not None:
            reData['introduce'] = str(div_pop_introduce)
        else:
            reData['introduce'] = ''

        return reData

    def parseSingerBaikePage(self, soup):
        relations = []
        reDatas = []
        if soup is None:
            return None, None
        div_baseinfo = soup.find("div", class_="basic-info")
        if div_baseinfo is None:
            reDatas = None
        else:
            dt_names = div_baseinfo.find_all("dt", class_="basicInfo-item name")
            for index, dt_name in enumerate(dt_names):
                rsData={}
                rsData['order'] = index
                rsData['name'] = dt_name.get_text().replace('\xa0', '').strip('\n')
                dd_value = dt_name.find_next()
                rsData['value'] = dd_value.get_text().replace('\xa0', '').strip('\n')
                reDatas.append(rsData)
            #dd_values = dt_names.find_next()
            print(reDatas)

        div_relations = soup.find("div", class_="relations")
        if div_relations is None:
            relations = None
        else:
            div_slider_relations = div_relations.find("div", id="slider_relations")
            lis = div_slider_relations.find_all("li")
            for index, li in enumerate(lis):
                relation = {}
                relation["baike_url"] = li.a["href"]
                relation["name"] = li.a.div["title"]
                relation["relations"] = li.a.div.get_text()
                relations.append(relation)
            print(relations)

        return reDatas, relations
