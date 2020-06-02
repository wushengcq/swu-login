#! /usr/bin/env python3
# --*-- encoding=utf8 --*--

import requests
import getpass

class SwuLogin(object):
	
	def login(self):
		key = self.askForKey()

		if self.isOnline(key):
			print(' [INFO] - user "' + key['user'] + '" already login on this host')
			return

		session_id = self.getSessionId()
		query_string = self.getQueryString()

		url = 'http://222.198.127.170/eportal/InterFace.do?method=login'
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Origin': 'http://222.198.127.170',
			'Referer': 'http://222.198.127.170/eportal/index.jsp?' + query_string,
			'Accept-Encoding': 'deflate',
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
			'Cookie': 'JSESSIONID=' + session_id
		}

		payload = {
			'userId': key['user'],
			'password': key['password'],
			'service': '默认',
			'queryString': query_string,
			'operatorPwd':'',
			'operatorUserId':'',
			'validcode':''
		}

		r = requests.post(url, headers=headers, data=payload)
		r.encoding = 'utf-8'
		#print(r.headers)
		#print(r.text)
		if r.text.find('success') > -1:
			print(' [INFO] - login success')
		else:
			# 提取错误信息
			msg = r.text[r.text.find('"message":"') + len('"message":"') : r.text.find('","keepaliveInterval')]
			print(' [ERRO] - ' + msg)

	def getSessionId(self):
		url_login = 'http://222.198.127.170'

		headers = {
			'Host': '222.198.127.170',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'deflate',
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
			'Upgrade-Insecure-Requests': '1'
		}
		r = requests.get(url_login, headers=headers, allow_redirects=False)
		#print(r.headers)
		#print(r.text)
		set_cookie = r.headers['set-cookie']
		return set_cookie[set_cookie.find('=')+1:set_cookie.find(';')]
	
	def getQueryString(self):
		url_123 = 'http://123.123.123.123'
		headers = {
			'Host': '123.123.123.123',
			'Connection': 'keep-alive',		# 必须设置为keep-alive,不然接收不到服务器的返回结果,会一直阻塞不返回数据
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'deflate',	# 设置为deflate,如果按浏览器的设置"gzip, deflate",返回数据为压缩格式,不便于处理
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Upgrade-Insecure-Requests': '1'
		}
		r = requests.get(url_123, headers=headers, allow_redirects=False)
		#print(r.headers)
		#print(r.text)
		return r.text[r.text.find('index.jsp?')+10 : r.text.rfind('\'</script>')]

	def isOnline(self, key):
		url_logout = 'http://222.198.127.170/eportal/gologout.jsp'
		headers = {
			'Host': '222.198.127.170',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Upgrade-Insecure-Requests': '1',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'deflate',
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
			'Referer': 'http://www.swu.edu.cn/',
        }
		r = requests.get(url_logout, headers=headers, allow_redirects=False)
		#print(r.headers)
		#print(r.text)
		status = r.headers['location'] != None and r.headers['location'].find('success.jsp') > -1
		return status

	def askForKey(self):
		print('--------------------------------------------------------')
		print(' Another door into the network of Southwest University  ')
		print('          v1.0, author: ws1115@swu.edu.cn              ')
		print('--------------------------------------------------------')
		u = input(' Input UserName : ')
		p = getpass.getpass(prompt=' Input Password : ')
		return {'user':u, 'password':p}

if __name__ == '__main__':
	swulogin = SwuLogin()
	swulogin.login()

