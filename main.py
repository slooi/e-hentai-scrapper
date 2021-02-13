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


	# Incase there's a offensive warning
	if(chap_url[-1]=="/"):
		chap_url+="?nw=session"
	else:
		chap_url+="/?nw=session"

	# Downloads all the imgs of this chapter

	# get all page urls
	page_urls,chp_name = get_all_page_urls_and_chp_name(chap_url)
	print("Images to download: {}".format(len(page_urls)))

	# Create folder for images
	create_folder(chp_name)

	# download and save images
	t_list = []
	try:
		for i, page_url in enumerate(page_urls):
			t = threading.Thread(target=h_download_imgs,args=(page_url,chp_name))
			t.start()
			print("Started download process for image {}".format(i))
			t_list.append(t)
			time.sleep(0.05)
	except Exception as err:
		print("Some thing went wrong while downloading and saving images!")
		print("Error:")
		print(err)
		print("Manged to download {} images".format(sum(t.is_alive() for t in t_list)))

	[t.join() for t in t_list]
	print("Everything downloaded from '{}'!".format(chp_name))

def h_download_imgs(page_url,chp_name):
	name = page_url_to_name(page_url)
	download_img_from_page(page_url,chp_name,name)

def create_folder(chp_name):
	if not os.path.exists("./{}".format(chp_name)):
		os.mkdir(chp_name)

def get_all_page_urls_and_chp_name(chap_url):
	# RETURN: [[PAGE_URLS],NAME_OF_CHAPTER]

	# find number of chap_page need to download
	num_to_download, hrefs = num_chap_pages_and_next_links(chap_url)

	# keep iterating to the next page until all chap_pages are looked at
	chap_pages_downloaded = 0
	page_urls = []
	while not chap_pages_downloaded == num_to_download:
		# get page content
		html = requests.get(hrefs[chap_pages_downloaded],headers=user_agent).content
		soup = BeautifulSoup(html,"html.parser")

		# get link to img pages from images' parents
		img_ele_list_unfiltered = soup.findAll("img",{"alt":re.compile(r"\d*")})
		img_ele_list = [img for img in img_ele_list_unfiltered if re.match(r"\d*",img["alt"]).end()>0]
		[page_urls.append(img.parent["href"]) for img in img_ele_list]

		chap_pages_downloaded+=1

	# get chapter name
	name = soup.findAll("h1",{"id":"gn"})[0].text
	name = re.sub('[^\w\-_\. ]', '_', name)
 
	return [page_urls,name]

def num_chap_pages_and_next_links(chap_url):
	# RETURNS: number of chapter pages AND next links

	# get page content
	html = requests.get(chap_url,headers=user_agent).content
	soup = BeautifulSoup(html,"html.parser")

	# 
	all_page_ele = soup.findAll("td",{"class":"ptdd"})[0].parent.findChildren("a")[0:-1]
	all_page_href = [ele["href"] for ele in all_page_ele]

	print(len(all_page_href),all_page_href)
	return [len(all_page_href),all_page_href]


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

# num_chap_pages_and_next_links("https://e-hentai.org/g/1846633/c6d614fbbf/")
download_img("https://pejbhim.hwxbgtmqrlbd.hath.network:6568/h/5182868199a47d35caee2c39026cf67755889bf8-109630-584-1262-jpg/keystamp=1613198100-3870178735;fileindex=81079955;xres=2400/76008129_p1.jpg",".","tester","jpg")

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
