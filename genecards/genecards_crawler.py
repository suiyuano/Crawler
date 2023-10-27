'''
Author: Yangsy
Date:   2023/10/27
Description:    This is a script to crawl the information of the website named "Genecards".
'''

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# 引入必要的库
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import openpyxl


# 全局变量


def read_file_lines(file_path):
    '''
    :param file_path:
    :return: 一个文件内容的生成器
    '''
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()


def get_driver():
    try:
        # 设置浏览器驱动路径（这里使用Chrome浏览器驱动作为示例）
        driver_path = 'G:\software\chrome_driver\chromedriver-win64\chromedriver.exe'

        # 选择谷歌浏览器
        s = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=s)
        return driver
    except Exception as e:
        print(f'获取浏览器实例失败！')
        print(e)
        return webdriver.Chrome()


def process_genelist(filepath: str) -> list:
    # 局部变量
    geneinfo = []  # 初始化

    file_path = filepath
    lines_generator = read_file_lines(file_path)
    # 使用 for 循环逐行迭代文件内容
    for line in lines_generator:
        print(line)
        geneinfo.append(line)

    # # 或者使用 next() 逐行获取文件内容
    # line1 = next(lines_generator)
    # print(line1)
    #
    # line2 = next(lines_generator)
    # print(line2)

    return geneinfo


def get_gene_web():
    pass


def export_info():
    # 创建输出表格Excel：创建工作表
    excel = openpyxl.Workbook()
    # 创建sheet页：以demo为名字创建一个sheet页
    sheet = excel.create_sheet('本科一批', 0)

    # 第一行第一列的单元格
    for i in range(len(school_info)):
        for k in range(len(school_info[i])):
            cell = sheet.cell(row=i + 1, column=k + 1)
            # 单元格赋值
            cell.value = school_info[i][k]

    # 保存excel文件
    excel.save('school_info.xlsx')


if __name__ == "__main__":
    # 设置你想要搜索的问题
    # web_url = 'https://www.genecards.org/'

    web_url = 'https://www.genecards.org/cgi-bin/carddisp.pl?gene=PCSK2&keywords=pcsk2'

    # login_cookie()
    driver = get_driver()

    driver.get(web_url)

    geneinfo = process_genelist('gene.txt')

    time.sleep(10)
    # login()

    # get_schools(web_url)
    # export_info()
    #
    # # 休息一分钟，检查信息
    # time.sleep(10)
    #
    # # 不关闭浏览器
    # ActionChains(driver).key_down(Keys.CONTROL).send_keys("t").key_up(Keys.CONTROL).perform()
