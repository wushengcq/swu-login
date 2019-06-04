#! /usr/bin/env python3
# --*-- encoding=utf8 --*--
# TODO: A Class of SwuNet

# Requests HTTP library
import requests
# Utilities to get a password and/or the current user name.
import getpass
# from getpass import *
import re


class SwuNet(object):

	def login(self, key, session_id):

		if self.is_online():
			print(' [INFO] - user ' + key['user'] + ' already login on this host!')
			return

		query_string = self.get_query_string()

		# 登录校园网时的Request URL和请求包结构
		url_lgoin = 'http://222.198.127.170/eportal/InterFace.do?method=login'
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Accept-Encoding': 'deflate',
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Origin': 'http://222.198.127.170',
			'Referer': 'http://222.198.127.170/eportal/index.jsp?' + query_string,
			'Cookie': 'JSESSIONID=' + session_id
		}
		payload = {
			'userId': key['user'],
			'password': key['password'],
			'service': '%E9%BB%98%E8%AE%A4',
			'queryString': query_string,
			'operatorPwd': '',
			'operatorUserId': '',
			'validcode': ''
		}

		# Requests HTTP library's post function Sends a POST request.
		# Return a requests.Response object.
		resp = requests.post(url_lgoin, headers=headers, data=payload)
		resp.encoding = 'utf-8'
		# find method returns the lowest index of 'success' in text.
		if resp.text.find('success') != -1:  # Return -1 on failure.
			# ps: resp.json()是字典对象，resp.text是类似字典的字符串对象
			# 两者包含的内容相同，但实际上却是不同类型的对象
			# print(resp.json())  # resp.text
			print(' [INFO] - login success')
		else:
			# 通过对字符串切片提取错误信息
			# print(resp.json())
			msg = resp.text[resp.text.find('"message":"') + len('"message":"'): resp.text.find('","keepaliveInterval')]
			print(' [ERRO] - ' + msg)

	def logout(self, key, session_id):

		if self.is_online() is False:
			print(' [INFO] - user ' + key['user'] + ' is offline.')
			return

		user_index = self.get_user_index()

		# 退出校园网时的Request URL和请求包结构
		url_logout = 'http://222.198.127.170/eportal/InterFace.do?method=logout'
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Accept': '*/*',
			'Accept-Encoding': 'deflate',
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Connection': 'keep-alive',
			'Origin': 'http://222.198.127.170',
			'Referer': 'http://222.198.127.170/eportal/success.jsp' + user_index,
			'Cookie': 'JSESSIONID=' + session_id
		}
		payload = {
			'userIndex': user_index,
		}

		resp = requests.post(url_logout, headers=headers, data=payload)
		resp.encoding = 'utf-8'
		# find method returns the lowest index of 'success' in text.
		if resp.text.find('success') != -1:  # Return -1 on failure.
			# print(resp.json())  # resp.text
			msg = resp.text[resp.text.find('"message":"') + len('"message":"'): -2]
			print(' [INFO] - ' + msg)
		else:
			# print(resp.json())
			msg = resp.text[resp.text.find('"message":"') + len('"message":"'): -2]
			print(' [ERRO] - ' + msg)

	def exit(self, key):

		params = self.get_online_device(key=key)
		session_id = params[0]
		ip = params[1]

		cookie = 'JSESSIONID=' + session_id + '; ' + 'oldpassWord=' + key['password'] + '; rmbUser=true; ' + \
		         'userName=' + key['user'] + '; ' + 'passWord=' + key['password']

		# 退出校园网时的Request URL和请求包结构
		url_exit = 'http://service2.swu.edu.cn/selfservice/module/userself/web/userself_ajax.jsf?methodName=indexBean.kickUserBySelfForAjax'
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Accept': 'text/plain, */*; q=0.01',
			'Accept-Encoding': 'deflate',
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Connection': 'keep-alive',
			'Cookie': cookie,
			'Host': 'service2.swu.edu.cn',
			'Origin': 'http://service2.swu.edu.cn',
			'Referer': 'http://service2.swu.edu.cn/selfservice/module/webcontent/web/onlinedevice_list.jsf',
			'X-Requested-With': 'XMLHttpRequest'
		}
		payload = {
			'key': key['user'] + ':' + ip
		}

		resp = requests.post(url_exit, headers=headers, data=payload)
		resp.encoding = 'gbk'
		# print(resp.headers)
		# print(resp.text)
		if resp.text.find('true') != -1:  # Return -1 on failure.
			msg = resp.text[resp.text.find('下线成功'): resp.text.find('下线成功') + len('下线成功')]
			print(' [INFO] - ' + msg)
		else:
			# 通过对字符串切片提取错误信息
			msg = resp.text[resp.text.find('false:null'): resp.text.find('false:null') + len('false:null')]
			print(' [ERRO] - ' + msg)

	def ask_for_key(self):
		print('--------------------------------------------------------')
		print(' Another door into the network of Southwest University  ')
		print('          v1.0, author: ws1115@swu.edu.cn              ')
		print('--------------------------------------------------------')
		user = input('UserName: ')
		# 在控制台环境下无回显输入密码
		password = getpass.getpass()  # 注意: 在IDE中直接Run无法执行此语句，只有在控制台下运行时才能输入密码
		return {'user': user, 'password': password}

	def is_online(self):
		# gologout.jsp -> index.jsp(offline) || success.jsp(online)
		url_logout = 'http://222.198.127.170/eportal/gologout.jsp'
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'deflate',
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Host': '222.198.127.170',
			'Referer': 'http://www.swu.edu.cn/',
			'Upgrade-Insecure-Requests': '1',
		}
		resp = requests.get(url_logout, headers=headers, allow_redirects=False)
		status = resp.headers['location'] != None and resp.headers['location'].find('success.jsp') != -1
		return status

	def get_session_id(self):
		url_login = 'http://222.198.127.170'
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'deflate',
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
			'Host': '222.198.127.170',
			'Upgrade-Insecure-Requests': '1'
		}
		resp = requests.get(url_login, headers=headers, allow_redirects=False)
		# print(resp.headers)
		set_cookie = resp.headers['set-cookie']
		return set_cookie[set_cookie.find('=') + 1: set_cookie.find(';')]

	def get_query_string(self):
		url_123 = 'http://123.123.123.123'
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'deflate',  # 设置为deflate,如果按浏览器的设置"gzip, deflate",返回数据为压缩格式,不便于处理
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Host': '123.123.123.123',
			'Connection': 'keep-alive',  # 必须设置为keep-alive,不然接收不到服务器的返回结果,会一直阻塞不返回数据
			'Upgrade-Insecure-Requests': '1'
		}
		resp = requests.get(url_123, headers=headers, allow_redirects=False)
		return resp.text[resp.text.find('index.jsp?') + 10: resp.text.rfind('\'</script>')]

	def get_user_index(self):
		url_index = 'http://222.198.127.170/eportal/InterFace.do?method=getOnlineUserInfo'
		session_id = self.get_session_id()
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Accept': '*/*',
			'Accept-Encoding': 'deflate',  # 设置为deflate,如果按浏览器的设置"gzip, deflate",返回数据为压缩格式,不便于处理
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Host': '222.198.127.170',
			'Origin': 'http://222.198.127.170',
			'Referer': 'http://222.198.127.170/eportal/success.jsp',
			'Connection': 'keep-alive',  # 必须设置为keep-alive,不然接收不到服务器的返回结果,会一直阻塞不返回数据
			'Cookie': 'JSESSIONID=' + session_id
		}
		resp = requests.get(url_index, headers=headers, allow_redirects=False)
		dict_resp = resp.json()
		return dict_resp['userIndex']

	def get_online_device(self, key):
		params = list()
		# 查询显示'我的设备'，需先登录'校园网自助服务系统'获取会话ID
		session_id = self.login_selfservice(key=key)
		params.append(session_id)

		cookie = 'JSESSIONID=' + session_id + '; ' + 'oldpassWord=' + key['password'] + '; rmbUser=true; ' + \
		         'userName=' + key['user'] + '; ' + 'passWord=' + key['password']

		url_device = 'http://service2.swu.edu.cn/selfservice/module/webcontent/web/onlinedevice_list.jsf'
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding': 'deflate',
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
			'Connection': 'keep-alive',
			'Host': 'service2.swu.edu.cn',
			'Referer': 'http://service2.swu.edu.cn/selfservice/module/webcontent/web/index_self.jsf?',
			'Cookie': cookie,
			'Upgrade-Insecure-Requests': '1'
		}

		reps = requests.get(url_device, headers=headers, allow_redirects=False)
		reps.encoding = 'gbk'
		# print(reps.text)
		if reps.text.find('我的电脑') != -1:  # Return -1 on failure.
			pattern_time = '..-.....:..:..'
			pattern_mac = 'MAC.*>............<'
			pattern_ip = 'IP.*<'
			msg_time = re.compile(pattern_time).findall(reps.text)
			msg_mac = re.compile(pattern_mac).findall(reps.text)
			msg_ip = re.compile(pattern_ip).findall(reps.text)
			print(' [INFO] - 我的电脑 ')
			print(' 上线时间: ', msg_time[0])
			print(' MAC : ', msg_mac[0].split('>')[1].strip('<'))
			print(' IP : ', msg_ip[0].strip('<')[5:])
			params.append(msg_ip[0].strip('<')[5:])
			return params
		else:
			print(' [INFO] - Not Device Online')
			exit(1)

	def login_selfservice(self, key):

		# rmbUser?
		cookie_get = 'rmbUser=true; ' + 'userName=' + key['user'] + '; ' + \
		         'oldpassWord=' + key['password'] + '; ' + 'passWord=' + key['password']
		url_service = 'http://service2.swu.edu.cn/selfservice/module/scgroup/web/login_judge.jsf'
		headers_get = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'deflate',
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
			'Connection': 'keep-alive',
			'Cookie': cookie_get,
			'Host': 'service2.swu.edu.cn',
			'Upgrade-Insecure-Requests': '1'
		}
		# 发送get请求获取会话ID
		resp_get = requests.get(url_service, headers=headers_get, allow_redirects=False)
		resp_get.encoding = 'gbk'
		set_cookie = resp_get.headers['Set-Cookie']
		session_id = set_cookie[set_cookie.find('=') + 1: set_cookie.find(';')]
		cookie_post = 'JSESSIONID=' + session_id + '; ' + 'oldpassWord=' + key['password'] + '; rmbUser=true; ' + \
		              'userName=' + key['user'] + '; ' + 'passWord=' + key['password']
		headers_post = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'deflate',
			'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Cookie': cookie_post,
			'Host': 'service2.swu.edu.cn',
			'Origin': 'http://service2.swu.edu.cn',
			'Referer': 'http://service2.swu.edu.cn/selfservice/module/scgroup/web/login_self.jsf',
			'Upgrade-Insecure-Requests': '1'
		}
		payload = {
			'name': key['user'],
			'password': key['password'],
		}
		# 发送post请求登录'校园网自助服务系统'
		resp_post = requests.post(url_service, headers=headers_post, data=payload)
		resp_post.encoding = 'gbk'
		# print(resp.text)
		if resp_post.text.find('errorMsg') != -1:
			msg = resp_post.text[resp_post.text.find('errorMsg=') + len('errorMsg='): resp_post.text.find('&name=')]
			print(' [ERRO] - ' + msg)
			exit(1)
		else:
			print(' [INFO] - SelfService System Login Success')

		return session_id

