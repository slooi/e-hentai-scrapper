import threading
from bs4 import BeautifulSoup 
import requests
import re
import os
import time
import sys
import random

user_agent = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0"
}

def download_chapter(chap_url):
	# Downloads all the imgs of this chapter

	# get all page urls
	page_urls,chp_name = get_all_page_urls_and_chp_name(chap_url)
	print("Images to download: {}".format(len(page_urls)))

	# Create folder for images
	create_folder(chp_name)

	# download and save images
	t_list = []
	try:
		for page_url in page_urls:
			t = threading.Thread(target=h_download_imgs,args=(page_url,chp_name))
			t.start()
			print("started {}".format("*"*random.randint(1,5)))
			t_list.append(t)
			time.sleep(0.05)
	except Exception as err:
		print("Some thing went wrong while downloading and saving images!")
		print("Error:")
		print(err)
		print("Manged to download {} images".format(sum(t.is_alive() for t in t_list)))

	[t.join() for t in t_list]
	print("Downloaded everything!")

def h_download_imgs(page_url,chp_name):
	name = page_url_to_name(page_url)
	download_img_from_page(page_url,chp_name,name)

def create_folder(chp_name):
	if not os.path.exists("./{}".format(chp_name)):
		os.mkdir(chp_name)

def get_all_page_urls_and_chp_name(chap_url):
	# RETURN: [[PAGE_URLS],NAME_OF_CHAPTER]
	html = requests.get(chap_url,headers=user_agent).content
	soup = BeautifulSoup(html,"html.parser")

	# get link to img pages from images' parents
	img_ele_list_unfiltered = soup.findAll("img",{"alt":re.compile(r"\d*")})
	img_ele_list = [img for img in img_ele_list_unfiltered if re.match(r"\d*",img["alt"]).end()>0]
	page_urls = [img.parent["href"] for img in img_ele_list]

	# get chapter name
	name = soup.findAll("h1",{"id":"gn"})[0].text
	name = re.sub('[^\w\-_\. ]', '_', name)
 
	return [page_urls,name]

def page_url_to_name(page_url):
	return page_url.split("/")[-1]

def download_img_from_page(page_url,chp_name,name):
	# downloads one image from a page

	# Get info to download image
	img_url = img_url_from_page_url(page_url)
	ext = get_img_ext(img_url)

	# Download image
	download_img(img_url,chp_name,name,ext)


def img_url_from_page_url(page_url):
	html = requests.get(page_url,headers=user_agent).content
	soup = BeautifulSoup(html,"html.parser")
	ele_list = soup.findAll("img",{"id":"img"})
	return ele_list[0]["src"]


def get_img_ext(img_url):
	# RETURN: extension
	return img_url.split(".")[-1]


def download_img(img_url,chp_name,name,ext):
	img_file = open("{}/{}.{}".format(chp_name,name,ext),"wb")
	img_file.write(requests.get(img_url).content)
	img_file.close()
	print("{} saved".format(name))

# if re.match(r"^http(s?)://e-hentai.org/g/*","https://e-hentai.org/g/1846795/a8bca0e681/"):
# 	print("nice")
# os.mkdir("[Puchimaple (Hisagi)] Kouhai Danshi ni Netorare SEX 2 [Chinese] [禁漫天堂灰羽社汉化组] [Digital]")
# download_chapter("https://e-hentai.org/g/1846795/a8bca0e681/")

if __name__ == '__main__':
	try:
		usr_input = sys.argv[1]
		if not usr_input == str and not re.match(r"^http(s)?://e-hentai.org/g/*",usr_input):
			raise Exception()
	except Exception as err:
		print("Invalid inputs. Please include an vaild e-hentai.org url")
		print("Error:",err)
		if len(sys.argv)>1:
			print("{} is invalid".format(sys.argv))
	else:
		download_chapter(usr_input)
