import requests,re,threading,os
cert='YWsxM240YWprOHxhZ3RrZWRjaXdo'
quality=1080
class spider:
    def __init__(self,sp):
        self.sp=sp
    def page(self,flag):
        page_url='https://javhd.com/zh/japanese-porn-videos/justadded/all/'+str(flag)
        return page_url
    def req(self):
        req=requests.Session()
        response=req.get('https://secure.javhd.com/login/index/direct?credentials='+cert+'&back=javhd.com&lang=zh', allow_redirects=False)
        req.get(response.headers['location'])
        return req
    def find_info(self,page_url):
        req=requests.get(page_url)
        info=re.findall(r'clickitem="(.*?)".*?t ">\n(.*?)\n.*?</span>',str(req.text),re.M)
        return info
    def find_mp4(self,id,reqget):
        url='https://javhd.com/zh/player/'+str(id)+'?type=vjs'
        req=reqget.get(url)
        return req.json()
    def sources_mp4(self,dict,reqget):
        for i in dict['sources']:
            if int(i['res'])==self.sp:
                w=reqget.get(i['src'],allow_redirects=False)
                return w.headers['location']
def Handler(start, end, url, filename):
    headers = {'Range': 'bytes=%d-%d' % (start, end)}
    with requests.get(url, headers=headers,stream=True) as r:
        with open(filename+'.mp4', "r+b") as fp:
            fp.seek(start)
            var = fp.tell()
            fp.write(r.content)
def download(url,tittle, num_thread = 10):
    r = requests.head(url)
    try:
        file_name = tittle
        file_size = int(r.headers['content-length'])
    except:
        print("检查URL，或不支持对线程下载")
        return
    fp = open(file_name+'.mp4', "wb")
    fp.truncate(file_size)
    fp.close()
    part = file_size // num_thread
    for i in range(num_thread):
        start = part * i
        if i == num_thread - 1:
            end = file_size
        else:
            end = start + part
        t = threading.Thread(target=Handler, kwargs={'start': start, 'end': end, 'url': url, 'filename': file_name})
        t.setDaemon(True)
        t.start()
 
    # 等待所有线程下载完成
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()
    print('%s 下载完成' % file_name)
def run():
    s=spider(quality)
    reqget=s.req()
    flag=1
    while True:
        page=s.page(flag)
        info=s.find_info(page)
        for i in info:
            mp4_dict=s.find_mp4(i[0],reqget)
            tittle=i[1].strip()
            print(tittle)
            if os.path.exists(str(tittle)+'.mp4')==False:
                print(s.sources_mp4(mp4_dict,reqget))
                download(s.sources_mp4(mp4_dict,reqget),tittle)
            else:continue
        flag+=1
if __name__=='__main__':
    run()
