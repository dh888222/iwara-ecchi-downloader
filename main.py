import requests,os,time,math
from bs4 import BeautifulSoup
from contextlib import closing

def unit_conversion(num):
	if num < 1024:
		unit_num = str(round(num,2)) + 'B'
	elif num < 1024 ** 2:
		unit_num = str(round(num / 1024,2)) + 'KB'
	elif num < 1024 ** 3:
		unit_num = str(round(num / 1024 ** 2,2)) + 'MB'
	else:
		unit_num = str(round(num / 1024 ** 2,2)) + 'GB'
	return unit_num

def download_video(name,url,path):
	while True:
		if download_video_son(name,url,path):
			print('\n此文件下载失败，3s后开始重新下载')
			time.sleep(3)
		else:
			break


def download_video_son(name,url,path):
	print("downloadinging%s…………" % name)
	real_url = "https:" + str(url)
	with closing(requests.get(real_url,headers = headers,stream = True)) as response:
		chunk_size = 1024 #单次请求最大值
		content_size = int(response.headers['content-length']) #总体积大小
		data_count = 0
		last_count = 0
		dl_speed = ''
		file_path = path + '\\' + name + ".mp4"
		last_time = time.time()
		with open(file_path,'wb') as file:
			for data in response.iter_content(chunk_size = chunk_size):
				file.write(data)
				data_count = data_count + len(data)
				now_jd = (data_count / content_size) * 100
				now_time = time.time()
				time_distance = now_time - last_time
				if time_distance >= 1:
					dl_speed_num = (data_count - last_count) / time_distance
					dl_speed = unit_conversion(dl_speed_num)
					last_time = now_time
					last_count = data_count
				print("文件下载进度: %d%%(%s/%s)%s/s - %s" % (now_jd,unit_conversion(data_count),unit_conversion(content_size),dl_speed,name),end = '\r')
		if now_jd <= 98:
			return True


keywords = input('输入关键字，不输入即为下载最新发布的n个:')
while True:
	try:
		video_input = input('请输入下载的个数(输入[all]下载全部):')
		break
	except:
		print('请输入整数或all')

url = 'https://ecchi.iwara.tv/search?query={}&f%5B0%5D=type%3Avideo'.format(keywords)
headers = {
	'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
try:
	res = requests.get(url,headers = headers, timeout=(10, 10))
except:
	print("未能成功连接iwara，请检查网络状况")
	exit(0)
soup = BeautifulSoup(res.text,'html.parser')
try:
	last_page = int(soup.find(class_ = 'pager-last last').find('a')['href'].split('=')[-1])
except AttributeError:
	last_page = 1
if video_input == 'all':
	page = last_page
	video_num = 10000000
else:
	video_num = int(video_input) / 40
	page = math.ceil(video_num)
	if page > last_page:
		page = last_page
path_name = os.getcwd() + '\\video'
if not os.path.exists(path_name):
	os.makedirs(path_name)
	print('检测到无video文件夹，自动创建')
else:
	pass
videos_urls = []
have_dl_num = 0
for x in range(page):
	if have_dl_num >= int(video_input):
		break
	page_url = url + '&page=' + str(x)
	res = requests.get(url,headers = headers)
	soup = BeautifulSoup(res.text,'html.parser')
	items = soup.find_all('div',class_ = 'node node-video node-wide_teaser clearfix')
	for item in items:
		item_a = item.find('h3',class_ = 'title').find('a')
		video_url = 'https://ecchi.iwara.tv/api/video' + item_a['href'][7:]
		video_name = item_a.text
		try:
			video_res = requests.get(video_url,headers = headers)
			video_json = video_res.json()
			dl_uri = video_json[0]['uri']
			print(dl_uri)
			download_video(video_name, str(dl_uri),path_name)
			have_dl_num += 1
		except:
			print('\nNo video in this page.')
	




input('\n下载完成，成功下载%d个视频，回车键退出' % have_dl_num)
