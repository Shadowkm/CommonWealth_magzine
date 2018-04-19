import asyncio
import uvloop
import aiohttp
import pandas as pd
import shutil
import re
from bs4 import BeautifulSoup as bsp
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

#headers放登入後的http header包括cookie
headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
"cache-control": "max-age=0",
"cookie": "_cb_ls=1; _ga=GA1.3.85884496.1523413943; SL_C_23361dd035530_VID=pvcB-w20xACu; SL_C_23361dd035530_KEY=19aaf69439071aa3dc932884420fe6abd553a411; _cb=ta7W-CgpDYsCW9TUx; _atrk_siteuid=rw7QzoQGcpLwtaYy; __gads=ID=e940936781a9d984:T=1523430931:S=ALNI_MaHlenLDI1JoJqTKqGg6pBi-pJWmQ; __eruid=521aa7b5-9f5d-07a6-322a-6a1e8bda8770; appier_uid_2=Srkj4D4VgAt2f1B9_iMRGL; SL_C_23361dd035530_SID=npzh7avIKAAu; _gac_UA-1198057-9=1.1523441716.Cj0KCQjw5LbWBRDCARIsALAbcOcx_QRTQt0x9riHF8PV3lL1qRd174OIuGnY-1g3oaAAQwuvEAOlHEcaAl6TEALw_wcB; _atrk_xuid=ea29e30bafe279206acbba7044b38046cef134f4f07c4df229ae5186acf9c71f; __erEvntUid=t1719482@gmail.com; user_ary=eyJpdiI6InhSNm1JdUZQc0RmeHZ3MlY5MXRudWc9PSIsInZhbHVlIjoiTE9MSEwxdGpOeHNMNTlMQytFQWIzSThFR0cyaTNzdmVXS2lmT28xU2R2UzVZTHRVT0NMVVN0aSt2TlVqa2xVY0F2SEJnc1BXd1F5K2FsRkplWUFxZVczSDJ1VmNBNkRzT256TngrTytuZFhPQ3czcGZlR2hKbm4wcUlRVnlVelIycVliRkxtbFNGSXJiKzhlUHZoNWpjUm1jaUUyM0F2dFdTMWhUZHhLbGN3NTlCRzJITndrMHFUaHZCMDY5cUFlNUliTEswbXJsaWFqNFFPUURnc2xaTktjcTF6RHhRVnZjVXRLMXIzQ2J5ajNiZnJYakQxY0lJMmxzMEQ5aHVkUmZVK0c4MmkzWHYwUU40SnEzUHdweTl3cDBTUlVMdDFlVDRSRk5WenFlNDJKWTFpXC9yaUo2SVdUOWFoV3JaYW5TTVY2aE5jcTlWYStUV0ZiVWpUcjlUN1lRT0kwaHVIS2xvazBScmJkY1VLVklBY3YrMVpqK2o3XC93bnZjNEpGXC9TS1dhUGc1eGpkNzVyQTRSMEVxdmtGbFMrK0xrNGFncU05Tm02VFJzb1FWQUoydXRwZFRcL2JKQ1JDTW9Fc1FmdUZxV2FtRWwxVHZTODEwN3AyNGJKQjRXaW50a20zd0ZKQ0J4d3VsSjB0YVNVOHRqTXN6aFd6S3doNTdiQ3VvYThqRFg1NDJGZ2w2dFRiYlBKM0RFNE81SDJ0XC9RWkF3RkZJbWNNVVc4VGJzc2ZJUFg1VHFzNWxuMGtYdzNzZU14N2FDWEJwcnhRc0NIV0Rqd2Jra0lNUUpmXC9Cb0cxRksxTkFnNTQ2OGl0Y0hqd0E5c3FaOWdFbHNLZ2dySkd1MVQ0ejVLdjdaaTVNWFNcL1wvUzF5RExSTUU0UERrR0Y2VklDU0RrcXkrM1B0dXYyeTZZSktScThOTWVKWDQwK1pcL0kyZlwvbEVHRUppWjVFWjMzNXV3WWVOSkkxUFwvaTJGNUQrVnIzclpORnc5R0tFZmRGZzM1N3RxK0N4TmZHTWVqNnNjK1JFOG16d1VTM0w5QzlkMXV3XC9IejczdGNnd2M3MWVqalZUclwvdURNRGV3UUJpaGxVZTRMRDlyMDA1NWd4SXZwbm8iLCJtYWMiOiJkMWFhZjYxYjU1ZGIwMzAzNWFiZjEwOGRkOGI2NDI2ODE1ZjJiZGFiNmIxMmJlOTM3YWIyMmExZTM5NDU0MjA4In0%3D; paywall_cookie_cw=eyJpdiI6ImhEVEtReVhybjFEbys4RkRVazdBTmc9PSIsInZhbHVlIjoibXZhNVRpcTZCclM5WGtoZ2pwaWhrUFI1ck9tTU9cLzhGcThiWDFkdGZOOVwvdEcwNnpYOXBFOXdLOGdNUVdSejNiR25mZkVDZXk1TTJGV1d5aVFvZ1BpTmt4K3Fyc1wvYjFHRnF5U3I2UTg2N0ZXWkdOeEdOaHhcL00zR29QaWtaUlZIQlh5a05OTURQT2dGbHIwN1FkdFhJejhlXC9wNldVdVo3VnNpVzJqdHNSK2hRbTRHaVk4V2ZObTRHODZZMDJXXC9TWU1FQVwvXC80dUJtXC9VaEFlOXhUVUZhdz09IiwibWFjIjoiYzk5OTc1ZjhkMGQ4ZWM3ZGQ0NmRlMmZjOTE1Nzk1ZWMxMDA0NDFhNjMyMjQzNWJlY2FhZmI0ZThlMGFjMzAxYiJ9; paywall_lightbox_new=eyJpdiI6IjVpc0RreDZ2Zit3dGROYmxFU1VmZ2c9PSIsInZhbHVlIjoieGVHMjMwWGlQWlZIV1hLbUhqZ1wvWlE9PSIsIm1hYyI6IjM2OTExZWI4ZTA0MmZkZGI4YjY3NTZmYjViYjBkYTJmMjU4YjI5ZGE2ZDVmOTBkYWUzNzRhM2VkYTA3ZWIyYWUifQ%3D%3D; _gid=GA1.3.2109598071.1523935998; _ceg.s=p7b8jk; _ceg.u=p7b8jk; appier_tp=; _cm_mmc=Facebook; _cm_cc=1; appier_utmz=%7B%22csr%22%3A%22Facebook%22%2C%22timestamp%22%3A1523936011%2C%22ccn%22%3A%22Daily%22%2C%22cmd%22%3A%22Social%22%7D; _atrk_ssid=klOgLGeUiTjW-NAI3v0c3e; _chartbeat2=.1523413946054.1523936011907.1101001.B1C4DkolRvyGAcxOwTDONS7q5L.1; _cb_svref=null; __lastv=5088277; XSRF-TOKEN=eyJpdiI6IjZQZTZ4eklOaFl5ZEtpYk5FWUNoYmc9PSIsInZhbHVlIjoiSjFXWW5jUUU5eFp5WUJSOVNKZGR3NjNibzVSNUpNQ2NWK2dYWHp2WmRXc05pUTJUZlwvSjRoT0c1SnRaNzFHWG01VU5vdHFMQWtJUGdHdWJVZXlzQnpBPT0iLCJtYWMiOiJjZDE3YWI2ZTIxMDA4ODVlMmYyMjc0NjgyNDczOWY4YzQ4MWU0ODI3MTZjODU3ZDMwNTIxZWFhZjA4YmJjNTc2In0%3D; laravel_session=eyJpdiI6ImRKeXZLK2hBUnY3Zyt6SitKYzkwV3c9PSIsInZhbHVlIjoiNEJaamtvdDZ4d0lmeTJxbENcLzZFR3BCTVlKRVBGUldObk9YempvMlVwNHZieWRcL2JVOEV4RXRDelpIOEZOMU02clhBWVNkeTRPV2Z1alczMEh1S0E5QT09IiwibWFjIjoiODZlODU0YzljNzhjYTUzNDM0YmU3MzgwZDE2Y2VlZWNlOTM2MTJkZjVjMzg0YjQyMDFkMTg3NTJiY2Y4MzQ5ZSJ9; _td=eecd899d-fa2b-4388-8acd-a2ecfacfec99; _atrk_sessidx=6",
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}
#output_dir放圖片輸出的位置
output_dir = 'image'
#data_dir放讀article_contents.csv的位置
data_dir =  'article_contents.csv'
pids = pd.read_csv(data_dir,lineterminator="\n").pid

async def extract_abstract(ix):
    url = 'https://www.cw.com.tw/article/articleLogin.action?id=%s'%ix
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url,headers=headers) as res:
            try:
                text = await res.text()
            except:
                print('%s failed'%ix)
                with open('failed.txt','a') as f:
                    f.write('%s\n'%ix)
                return
            soup = bsp(text,"lxml")
            try:
                img_url = soup.select('.main article .st_email_large')[0]['st_image']
                if len(img_url) == 0: return
                img_url = re.sub('\:\d+','',img_url)
                print(img_url)
                print('--------')
                async with session.get(img_url,headers=headers) as img_res:
                    img = await img_res.read()
                    with open('%s/%s.jpg'%(output_dir,ix),'wb') as out_file:
                        #shutil.copyfileobj(img, out_file)
                        out_file.write(img)
            except IndexError:
                return 

async def crawler(pids):
    sem = asyncio.Semaphore(10)
    for ix in pids:
        print(ix)
        async with sem:
            await extract_abstract(ix)

event_loop = asyncio.get_event_loop()
future = asyncio.ensure_future(crawler(pids))
results = event_loop.run_until_complete(future)
