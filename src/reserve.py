# -*- coding: UTF-8 -*-
import mechanize  
import cookielib  
import urllib
import json

# Encode the ' ' with '#'
USER_NAME = 'denis+wu'
  
br = mechanize.Browser()  
cj = cookielib.LWPCookieJar()  
br.set_cookiejar(cj)##关联cookies  
  
###设置一些参数，因为是模拟客户端请求，所以要支持客户端的一些常用功能，比如gzip,referer等  
br.set_handle_equiv(True)  
br.set_handle_gzip(True)  
br.set_handle_redirect(True)  
br.set_handle_referer(True)  
br.set_handle_robots(False)  
  
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)  
  
###这个是degbug##你可以看到他中间的执行过程，对你调试代码有帮助  
br.set_debug_http(True)  
#br.set_debug_redirects(True)  
#br.set_debug_responses(True)  
  
##模拟浏览器头
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.11) Gecko/20100701 Firefox/3.5.11')]

## 登录URL
br.open('http://cdcfan/api/user-search?identity={}&_=1505786191038'.format(USER_NAME))

assert(br.response().code == 200)

response = json.loads(br.response().read())

PSID = response['psid']
DEPARTMENT = response['depcode']


###个人信息，修改psid和depcode
params = {u'order': u'e-1', u'psid': PSID, u'depcode': DEPARTMENT}

data = urllib.urlencode(params)

# 订餐
br.open('http://cdcfan/api/order-new', data)

# 查看订餐状态
br.open('http://cdcfan/api/my-orders?psid={}'.format(PSID))

response = json.loads(br.response().read())

response = response[0] if response else None

if response:
	print 'Order success!'
else:
	print 'Order failed!'
