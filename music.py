import  requests
import  re
import  random

def donwload_voice(word):
    uapools = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"
        "Mozilla/5.0 (Windstows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"
    ]  # 浏览器伪装
    headers = {"User-Agent": random.choice(uapools)}
    r = requests.get('http://www.iciba.com/word?w='+word,headers = headers)
    # pattern = re.compile(r'<i class="new-speak-step" ms-on-mouseover="sound\(\'(.*?)\'\)"></i>',re.S)  #语音文件地址正则
    print(r.url)
    # "ph_en_mp3": "http://res.iciba.com/resource/amp3/oxford/0/07/a4/07a464945dda3d310b26995258d9a88a.mp3"
    # "ph_en_mp3": "http://res.iciba.com/resource/amp3/oxford/0/1c/f3/1cf3980c4529878b690ded143c409664.mp3"
    # "ph_am_mp3": "http://res.iciba.com/resource/amp3/1/0/76/80/7680edae4d6618e8fe00990c9f628966.mp3"

donwload_voice('path')     #开始愉快地玩耍吧