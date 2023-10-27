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
# username:   yangsy@big.ac.cn
# password:   ysy17308104115


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


# 得到登录的cookie
def login_cookie():
    # driver = get_driver()
    # driver.set_page_load_timeout(20)
    # driver.set_script_timeout(20)
    # LOGIN_URL = 'https://www.genecards.org/Account/LogOn?moduleName=GC'
    # driver.get(LOGIN_URL)
    # time.sleep(10)
    input("请登录后按 Enter")
    cookies = driver.get_cookies()
    jsonCookies = json.dumps(cookies)
    # 下面的文件位置需要自己改
    with open('cookie.txt', 'w') as f:
        f.write(jsonCookies)
    # driver.quit()


# 再次登录
def login():
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    LOGIN_URL = 'https://www.genecards.org/'
    driver.get(LOGIN_URL)
    time.sleep(5)
    # 下面的文件位置需要自己改，与上面的改动一致
    f = open('cookie.txt')
    cookies = f.read()
    jsonCookies = json.loads(cookies)
    # print(jsonCookies)
    for co in jsonCookies:
        driver.add_cookie(co)
    # for co in cookie:
    #     driver.add_cookie(co)
    driver.refresh()
    # 打印网页title
    # print(driver.title)
    time.sleep(5)


def process_genelist(filepath: str) -> list:
    '''
    :param filepath: 文件名(文件格式：第一列-基因名；第二列-ensembl ID)
    :return: geneinfo 基因信息
    '''

    # 局部变量
    geneinfo = []  # 初始化

    file_path = filepath
    lines_generator = read_file_lines(file_path)
    # 使用 for 循环逐行迭代文件内容
    for line in lines_generator:
        each_gene = line.strip('\n').split('\t')
        geneinfo.append(each_gene)

    # # 或者使用 next() 逐行获取文件内容
    # line1 = next(lines_generator)
    # print(line1)
    #
    # line2 = next(lines_generator)
    # print(line2)

    return geneinfo


def get_gene_web(geneinfo: list) -> list:
    '''
    :param geneinfo: 基因名和ID
    :return: geneout: 爬取的基因信息
    '''

    # 局部变量
    geneinfo = geneinfo
    geneout = []

    # driver = get_driver()  # 获取浏览器实例

    for each_gene in geneinfo:
        gene_name_upper = each_gene[0].upper()
        gene_name_lower = each_gene[0].lower()
        ensembl_id = each_gene[1]
        current_info = []

        # web_url = 'https://www.genecards.org/'    #目标网址

        web_url = f'https://www.genecards.org/cgi-bin/carddisp.pl?gene={gene_name_upper}&keywords={gene_name_lower}'
        driver.get(web_url)  # 获取单个基因的页面
        input("按下回车键寻找该基因的调控元件：")  # 每次等待键盘输入再继续处理下一个基因

        # login_url = 'https://www.genecards.org/Account/LogOn?moduleName=GC'
        # driver.get(login_url)
        # time.sleep(5)

        # 获取页面对应基因的ensembl ID,这是基因的唯一标识，光查询genename容易出错！
        target_ensembl_id = driver.find_element(By.XPATH,
                                                '//*[@id="aliases_descriptions"]/div[1]/div[1]/div[2]/div/ul/li[3]/a').text
        if target_ensembl_id == ensembl_id:
            # 如果ensembl ID相同，说明是目标基因，放心进行信息的爬取
            # 我目前只关注该基因所对应的所有genehancer信息
            # show_all_elements = driver.find_element(By.XPATH,
            #                                         '//*[@id="enhancerControllerComponent"]/div/div[2]/div/div/div[1]/a[1]')
            # show_all_elements.click()

            tbody = driver.find_element(By.XPATH, '//*[@id="enhancerControllerComponent"]/div/div[2]/div/table/tbody')
            all_tr = tbody.find_element(By.TAG_NAME, 'tr')
            # 遍历每个<tr>元素并获取其内容
            count = 1
            for row in all_tr:
                if count % 2 == 1:
                    # 奇数，表示是主要信息行
                    cells = row.find_element(By.TAG_NAME, 'td')
                    for item in cells:
                        text = item.text
                        current_info.append(text)
                else:
                    # 偶数，表示是拓展行
                    # 使用XPath找到父标签下的所有子元素
                    child_elements = row.find_elements_by_xpath(".//*")

                    # 遍历每个子元素并获取其文本内容
                    for element in child_elements:
                        text = element.text
                        if text:
                            if '(GRCh37/hg19)' in text:
                                current_info.append(text)
                                geneout.append(current_info)
                                current_info = []   #再次初始化
                                break
                            else:
                                continue
                        else:
                            continue

                count += 1  # 移动到下一行

            time.sleep(5)

        else:
            print('Chech your gene plz! The ensembl ID is not match!')
            time.sleep(5)

        print(geneout)
        input("按下回车键继续处理下一个基因...")  # 每次等待键盘输入再继续处理下一个基因

    return geneout


def export_info():
    pass


if __name__ == "__main__":
    # 脚本入口

    driver = get_driver()
    # driver.set_page_load_timeout(20)
    # driver.set_script_timeout(20)
    # LOGIN_URL = 'https://www.genecards.org/Account/LogOn?moduleName=GC'
    # driver.get(LOGIN_URL)
    # time.sleep(10)
    # login_cookie()  # 登录，记录cookie

    # f = open('cookie.txt')
    # cookies = f.read()
    # jsonCookies = json.loads(cookies)
    # # print(jsonCookies)
    # for co in jsonCookies:
    #     driver.add_cookie(co)
    # # for co in cookie:
    # #     driver.add_cookie(co)
    # driver.refresh()

    # driver = get_driver()   # 获取浏览器实例
    # login() #再次登录，携带cookie

    geneinfo = process_genelist(filepath='gene.txt')
    print(geneinfo)

    geneinfo = get_gene_web(geneinfo=geneinfo)

    # get_schools(web_url)
    # export_info()

    # 休息一分钟，检查信息
    time.sleep(10)

    # 不关闭浏览器
    ActionChains(driver).key_down(Keys.CONTROL).send_keys("t").key_up(Keys.CONTROL).perform()
