from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from settings import *
import schedule
from multiprocessing.context import Process
import time

def main():
    setting = get_project_settings()
    # init settings
    initsettings(setting)
    process = CrawlerProcess(setting)
    didntWorkSpider = ['xiaoso',]
    for spider_name in process.spiders.list():
        if spider_name in didntWorkSpider :
            continue
        # print("Running spider %s" % (spider_name))
        process.crawl(spider_name)
    process.start()

def sub_process_start():
    process = Process(target=main)
    process.start() # 开始执行
    process.join()  # 阻塞等待进程执行完毕

def initsettings(setting):
    if DATABASE == 'leancloud':
        setting["ITEM_PIPELINES"]["hexo_circle_of_friends.pipelines.leancloud_pipe.LeancloudPipeline"] = 300
    elif DATABASE == 'mysql' or DATABASE== "sqlite":
        setting["ITEM_PIPELINES"]["hexo_circle_of_friends.pipelines.sql_pipe.SQLPipeline"] = 300

if __name__ == '__main__':
    if DEPLOY_TYPE == "docker" or DEPLOY_TYPE == "server":
        # server/docker部署
        schedule.every(6).hours.do(sub_process_start)
        schedule.run_all()
        while 1:
            n = schedule.idle_seconds()
            if n is None:
                # no more jobs
                break
            elif n > 0:
                # sleep exactly the right amount of time
                time.sleep(n)
            schedule.run_pending()
    else:
        main()