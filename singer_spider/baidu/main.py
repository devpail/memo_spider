# -*- coding:utf-8 -*-

# 爬虫总调main函数

import time
import urllib.parse
import db_helper
import html_ChromeDriver
import html_parser
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()


class SpiderMain(object):


    # 初始化方法
    def __init__(self):
        # 初始化下载器
        self.downloader = html_ChromeDriver.HtmlDownload()
        # 初始化解析器
        self.parser = html_parser.HtmlParser()
        # 初始化数据库存储
        self.dbHelper = db_helper.DbHelper()

    # 抓取百度音乐歌手名单页面
    def crawlSingerListPage(self, root_url):
        startTime = time.time()
        logger.info("百度音乐歌手列表页面抓取开始时间戳：" + str(startTime))
        # 下载url页面html
        soup = self.downloader.download(root_url)
        # print(htmlCode.decode('utf-8'))
        # 解析html代码
        datas = self.parser.parseSingerListPage(soup)
        # 存储到数据库中
        self.dbHelper.saveSinger(datas)
        endTime = time.time()
        logger.info("百度音乐歌手列表页面抓取结束时间戳：" + str(endTime))
        logger.info("用时：" + (endTime-startTime)/1000)

    # 抓取百度音乐歌手个人页面的百度百科URL
    def crawlSingerPage(self):
        startTime = time.time()
        logger.info("百度音乐歌手详情页面抓取开始时间戳：" + str(startTime))
        # 从数据库中取出所有的歌手
        singers = self.dbHelper.get10Singer()
        while singers != None:
            # 遍历歌手的信息取出百度音乐个人页面
            for singer in singers:
                # 抓取百科地址、贴吧地址、图片地址存储
                soup = self.downloader.download(singer[1])
                # 解析歌手详情页
                logger.info("解析网页信息:name=" + singer[2] + ",href=" + singer[1])
                data = self.parser.parserSingerPage(soup)
                if data is None:
                    self.dbHelper.updateSingerStatus(singer[0], 2)
                    continue
                data['baike_url'] = 'https://baike.baidu.com/item/' + urllib.parse.quote(singer[2])
                # 保存抓取的歌手详情信息
                self.dbHelper.saveSingerInfo(singer[0], data)
            singers = self.dbHelper.get10Singer()
        else:
            logger.info("百度音乐歌手信息页面已全部抓取完毕~\n\n\n")
        endTime = time.time()
        logger.info("百度音乐歌手详情页面抓取结束时间戳：" + str(endTime))
        logger.info("用时：" + (endTime - startTime) / 1000)

    # 抓取歌手百度百科页面信息
    def crawlBaike(self):
        startTime = time.time()
        logger.info("百度音乐歌手百科页面抓取开始时间戳：" + str(startTime))
        # 从数据库中取出所有的名字信息
        singers = self.dbHelper.get10SingerInfo()
        while singers != None:
            self.crawlSingerBaikePage(singers)
            singers = self.dbHelper.get10SingerInfo()
        else:
            logger.info("百度百科页面已全部抓取完毕~")
        endTime = time.time()
        logger.info("百度音乐歌手百科页面抓取结束时间戳：" + str(endTime))
        logger.info("用时：" + (endTime - startTime) / 1000)

    # 抓取歌手百度百科页面
    def crawlSingerBaikePage(self, singers): #singer_id,baike_url,id
        for singer in singers:
            if singer[1] is None:
                continue
            if self.dbHelper.getSingerBaike(singer[1]) != 0:
                logger.info(singer[1] + ' 的百科信息已经被抓取~')
                self.dbHelper.updateSingerInfoStatus(singer[2], 1)
                continue
            logger.info('开始抓取 ' + singer[1] + ' 的百科信息~')
            # 下载百度百科页面
            singer_baike_url = singer[1]
            soup = self.downloader.download(singer_baike_url)
            # 抓取百科页面信息
            itemDatas, relations = self.parser.parseSingerBaikePage(soup)
            if itemDatas is None and relations is None:
                self.dbHelper.updateSingerInfoStatus(singer[2], 2)
                logger.info(singer[1] + " 的百科页面-没有个人详情数据！")
            else:
                # 存储抓取的数据
                logger.info('保存 ' + singer[1] + " 的百科信息~")
                self.dbHelper.saveBaike(singer, itemDatas, relations)



if __name__ == "__main__":
    root_url = "http://music.baidu.com/artist"
    obj_spider = SpiderMain()
    # 抓取百度音乐歌手名单
    #obj_spider.crawlSingerListPage(root_url)
    # 抓取百度音乐歌手页面
    #obj_spider.crawlSingerPage()
    # 抓取歌手百度百科页面
    obj_spider.crawlBaike()
