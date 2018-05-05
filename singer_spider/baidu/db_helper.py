# -*- coding:utf-8 -*-
import uuid
import time
import pymysql as pymysql
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()
class DbHelper(object):
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'db': 'memo_spider',
        'charset': 'utf8'
    }
    def saveSinger(self, datas):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                for data in datas:
                    if self.getSingerByHref(data['href']) != 0:
                        logger.info(data['name']+'的url已经被抓取~')
                        continue
                    sql = 'insert into `bd_singer`(`id`,`href`,`name`,`time`,status) values(%s,%s,%s,%s,%s)'
                    cursor.execute(sql, (str(data['id']), data['href'], data['name'], str(data['time']), 0))
                    connection.commit()
                    logger.info(data['name']+":"+data['href'] + "    -保存成功~")
        finally:
            connection.close()

    # 检查是否已经抓取
    def getSingerByHref(self, href):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "select `id`, `name`, `href`, `time`, `status` from `bd_singer` where href = %s limit 1"
                cursor.execute(sql, (str(href)))
                return cursor.rowcount
        finally:
            connection.close()

    #获取10条未抓取成功的歌手
    def get10Singer(self):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "select `id`,`href`,`name`,`time` from bd_singer where status = 0 limit 10"
                logger.info(sql + ":" + sql)
                cursor.execute(sql)
                if cursor.rowcount == 0:
                    return None
                else:
                    return cursor.fetchall()
        finally:
            connection.close()

    def listSinger(self):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "select `id`,`href`,`name`,`time` from `bd_singer`"
                logger.info(sql+":"+sql)
                cursor.execute(sql)
                datas = cursor.fetchmany(size=6000)
            connection.commit()
            return datas
        finally:
            connection.close()

    def updateSingerStatus(self, singerId, status):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "update bd_singer set status = %s where id = %s"
                logger.info("更新id是" + str(singerId) + "的页面url抓取状态为" + str(status))
                cursor.execute(sql, (status, str(singerId)))
                connection.commit()
                logger.info(singerId + "--抓取状态更新~")
        finally:
            connection.close()

    def saveSingerInfo(self, singer_id, data):
        connection = pymysql.connect(**self.config)
        if data is None:
            return
        try:
            with connection.cursor() as cursor:
                info_id = str(uuid.uuid1())
                sql = "insert into `bd_singer_info`(`id`, `singer_id`, `img`, `hot`, `introduce`, baike_url, `time`, `status`) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (info_id, singer_id,  str(data['img']), str(data['hot']),  str(data['introduce']), str(data['baike_url']), str(time.time()), 0))
                connection.commit()
                self.updateSingerStatus(singer_id, 1)
        except Exception as err:
            logger.info(err.__str__())
            self.updateSingerStatus(singer_id, -1)
        finally:
            connection.close()


    # 获取10条未抓取百科信息的歌手
    def get10SingerInfo(self):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "select  singer_id,baike_url,id from bd_singer_info where status = 0 limit 10"
                cursor.execute(sql)
                if cursor.rowcount == 0:
                    return None
                else:
                    return cursor.fetchall()
        finally:
            connection.close()

    # 验证singer百科页面是否被抓取
    def getSingerBaike(self, href):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "select id FROM bd_baike where href = %s "
                cursor.execute(sql, (str(href)))
                return cursor.rowcount
        finally:
            connection.close()

    def saveBaike(self, singer, itemDatas, relations):
        singerId = singer[0]
        singerBaikeUrl = singer[1]
        singerInfoId = singer[2]
        connection = pymysql.connect(**self.config)

        try:
            with connection.cursor() as cursor:
                baike_id = str(uuid.uuid1())
                sql = "insert into `bd_baike`(`id`, `singer_id`, `time`, `href`) values(%s,%s,%s,%s)"
                cursor.execute(sql, (baike_id, singerId, str(time.time()), singerBaikeUrl))
                connection.commit()
                if itemDatas is not None:
                    for item in itemDatas:
                        sql = "insert into `bd_baike_item`(`id`,`baike_id`,`order`,`name`,`value`) values(%s,%s,%s,%s,%s)"
                        cursor.execute(sql, (str(uuid.uuid1()), baike_id, item['order'], item['name'], item['value']))
                        connection.commit()
                if relations is not None:
                    for item in relations:
                        sql = "insert into `bd_baike_relations`(`id`,`baike_id`,`relations`,`name`,`baike_url`,status) values(%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sql, (str(uuid.uuid1()), baike_id, item['relations'], item['name'], item['baike_url'], 0))
                        connection.commit()
                self.updateSingerInfoStatus(singerInfoId, 1)
        except Exception as err:
            logger.info(err.__str__())
            self.updateSingerInfoStatus(singerInfoId, -1)
        finally:
            connection.close()

    def saveRelations(self, singer, relations):
        singerId = singer[0]
        singerBaikeUrl = singer[1]
        singerInfoId = singer[2]
        connection = pymysql.connect(**self.config)
        if relations is None:
            return
        try:
            with connection.cursor() as cursor:
                baike_id = str(uuid.uuid1())
                sql = "insert into `bd_baike`(`id`, `singer_id`, `time`, `href`) values(%s,%s,%s,%s)"
                cursor.execute(sql, (baike_id, singerId, str(time.time()), singerBaikeUrl))
                connection.commit()
                for item in itemDatas:
                    sql = "insert into `bd_baike_item`(`id`,`baike_id`,`order`,`name`,`value`) values(%s,%s,%s,%s,%s)"
                    cursor.execute(sql, (str(uuid.uuid1()), baike_id, item['order'], item['name'], item['value']))
                    connection.commit()
                self.updateSingerInfoStatus(singerInfoId, 1)
        except Exception as err:
            logger.info(err.__str__())
            self.updateSingerInfoStatus(singerInfoId, -1)
        finally:
            connection.close()

    def updateSingerInfoStatus(self, singerInfoId, status):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "update bd_singer_info set status = %s where id = %s"
                logger.info("更新id是" + str(singerInfoId) + "的页面url抓取状态为" + str(status))
                logger.info("sql:" + sql)
                cursor.execute(sql, (status, str(singerInfoId)))
                connection.commit()
                logger.info(singerInfoId + "--抓取状态更新~")
        finally:
            connection.close()