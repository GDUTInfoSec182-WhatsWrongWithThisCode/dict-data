import requests
from bs4 import BeautifulSoup
import pymysql
import re
 
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'
}
 
def get_urlhtml(url):#爬取主页
    try:
        html = requests.get(url,headers = header)#使用requests库爬取
        if html.status_code == 200:#如果状态码是200，则表示爬取成功
            print(url+'解析成功')
            return html.text#返回H5代码
        else:#否则返回空
            print('解析失败')
            return None
    except:#发生异常返回空
        print('解析失败')
        return None
 
def get_url(html):#解析首页得到所有的网址
    word_all = []#所有classid可能取值的列表
    mess = BeautifulSoup(html,'lxml')
    word_num = mess.select('.main_l li')
    for word in word_num:
        word_all.append(word.get('class_id'))
    return word_all
 
def paqu_wangye(reponse,name):#爬取所有的单词、发音、翻译
    word_mause={}
    mess = BeautifulSoup(reponse,'lxml')
    word = mess.find_all('div',class_="word_main_list_w")
    
    
    wordmp3= mess.find_all(class_="word_main_list_y")
    for i in range(1,len(word)):
        key = word[i].span.get('title')
        
        
        mp3=wordmp3[i].a.get('id')
        #if len(f) == 0:#因为某些发音不存在，我们直接放弃，不存入
            #continue
        word_mause[key]=[mp3]
    print('创建数据成功')
    return word_mause
  
def cucun(word_mause):#爬取数据到数据库
    db = pymysql.connect(host='localhost', user='root', password='yzh86831051', db='resource', port=3306)#打开数据库
    print('打开数据库成功')
    cursor = db.cursor()#创建一个游标
    for key in word_mause:#word_mause是一个字典，模型：{'comment': ['[ˈkɔment]', 'n. 评论，意见；体现，写照', '四级必备词汇']}
        sql = 'UPDATE dictory_02 SET pronunciation=%s WHERE word=%s'#构造sql语句
        try:
            cursor.execute(sql, (word_mause[key][0],key))
            db.commit()#插入数据
        except:
            db.rollback()#如果发生异常，则回滚（什么事情都没有发生）
    print('数据插入成功')
    db.close()#关闭数据库，记得一定要记得关闭数据库
    print('数据库成功关闭')
 
def main():
    url = 'http://word.iciba.com/'
    html = get_urlhtml(url)#得到首页的H5代码
    word_all = get_url(html)#得到所有classid可能取值的列表
    print('初始化成功开始爬取')
    for num in word_all:#word_all为classid所有可能的取值

        if num=='123':
            url_home = 'http://word.iciba.com/?action=courses&classid=' + str(num)#利用字符串拼接起来，得到URL网址
            html = get_urlhtml(url_home)
            mess = BeautifulSoup(html, 'lxml')
            li = mess.select('ul li')#解析得到所有的课时，其中li的长度就是课时的数量
            if len(li) <= 2:
                   continue
            name = mess.select('.word_h2')#得到词书名称
            name = name[0]
            r = re.compile(".*?</div>(.*?)</div>")
            name = re.findall(r,str(name))
            name  = name[0]#得到词书名称
            print('开始爬取'+name)
            for j in range(1,len(li)+1):#利用课时的数量就是course的取值的特性，得到course的取值
                url = 'http://word.iciba.com/?action=words&class='+str(num)+'&course='+str(j)#得到单词所在的URL网站
                reponse = get_urlhtml(url)
            # print('开始爬取音频')
            # paqumusci(reponse)
            # print('音频文件爬取完成')
                print('开始爬取数据')
                word_mause = paqu_wangye(reponse,name)#得到数据字典
                print('开始存储数据')
                cucun(word_mause)#存储数据
 
if __name__ == '__main__':
    main()