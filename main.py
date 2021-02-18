import threading
from bs4 import BeautifulSoup 
import requests
import re
import os
import time
import sys


# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.poolmanager import PoolManager
# import ssl

# class MyAdapter(HTTPAdapter):
#     def init_poolmanager(self, connections, maxsize, block=False):
#         self.poolmanager = PoolManager(num_pools=connections,
#                                        maxsize=maxsize,
#                                        block=block,
#                                        ssl_version=ssl.PROTOCOL_TLSv1)

s = requests.Session()
# s.mount('https://', MyAdapter())


user_agent = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0",
	# "Set-Cookie": "w:1"
}

unable_to_download = []

def download_chapter(chap_url):
	global unable_to_download 
	unable_to_download = []


	# Incase there's a offensive warning
	if(chap_url[-1]=="/"):
		chap_url+="?nw=session"
	else:
		chap_url+="/?nw=session"

	# Downloads all the imgs of this chapter

	# get all page urls
	page_urls,chp_name = get_all_page_urls_and_chp_name(chap_url)
	print("Beginning download of: {}".format(chp_name))
	print("Images to download: {}".format(len(page_urls)))

	# Create folder for images
	create_folder(chp_name)

	# download and save images
	t_list = []
	try:
		for i, page_url in enumerate(page_urls):
			t = threading.Thread(target=h_download_imgs,args=(page_url,chp_name))
			t.info = (page_url_to_name(page_url),page_url)
			t.start()
			print("Started download process for image {}".format(i))
			t_list.append(t)
			# time.sleep(0.05)
	except Exception as err:
		print("Some thing went wrong while downloading and saving images!")
		print("Error:")
		print(err)
		print("Manged to download {} image(s)".format(sum(t.is_alive() for t in t_list)))

	tm = thread_monitor(t_list)

	[t.join() for t in t_list]

	failed = True

	if len(unable_to_download) == 0:
		print("Successful download of '{}'!".format(chp_name))
		failed = False
	elif len(unable_to_download) < len(page_urls):
		print("PARTAL Successful download of '{}'!".format(chp_name))
		print("Missing page(s): {}".format(unable_to_download))
	else:
		print("Failed download of '{}'!".format(chp_name))

	if failed == True:
		# Second attempt at downloading images
		print("@"*30)
		print("ATTEMPT TO DOWNLOAD FAILED IMAGES")
		page_urls = unable_to_download
		unable_to_download = []
		for img_name, page_url in page_urls:
			t = threading.Thread(target=h_download_imgs,args=(page_url,chp_name))
			t.info = (page_url_to_name(page_url),page_url)
			t.start()
			print("Started download process for image {}".format(img_name))
			t_list.append(t)

		[t.join() for t in t_list]

		if len(unable_to_download) == 0:
			print("Successful download of '{}'!".format(chp_name))
		elif len(unable_to_download) < len(page_urls):
			print("PARTAL Successful download of '{}'!".format(chp_name))
			print("Missing page(s): {}".format(unable_to_download))
		else:
			print("Failed re-download of '{}'!".format(chp_name))
			print("Missing page(s): {}".format(unable_to_download))

		
	tm.do_run = False


def monitor(t_list):
	# Monitors the thread
	# Consoles progress occassionly
	t = threading.current_thread()
	while getattr(t,"do_run",True):
		print("#"*30)
		alive_threads =  [t.info[0] for t in t_list if t.is_alive()]
		print("Progress: {} out of {} images remaining. Number of skipped images: {}. {} ".format(len(t_list) - sum(t.is_alive() for t in t_list),len(t_list),len(unable_to_download),"Images remaining: {}".format(alive_threads,end="") if len(alive_threads)<10 else ""))
		time.sleep(10)


def thread_monitor(t_list):
	tm = threading.Thread(target=monitor,args=(t_list,))
	tm.do_run = True
	tm.start()
	return tm


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
		html = s.get(hrefs[chap_pages_downloaded],headers=user_agent).content
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
	html = s.get(chap_url,headers=user_agent).content
	soup = BeautifulSoup(html,"html.parser")

	# THE LINE BELOW THROWS AND ERROR WHEN YOU'VE BEEN BANNED
	a_tags = soup.findAll("td",{"class":"ptdd"})[0].parent.findChildren("a") 
	all_page_ele = a_tags
	if not len(a_tags) == 1:
		all_page_ele = a_tags[0:-1]

		first_half_url, last_pg_str = all_page_ele[-1]["href"].split("=")
		first_half_url+="="
		all_page_href = generate_chap_pages(first_half_url,last_pg_str)

		print("Download from {} pages: {}".format(len(all_page_href),all_page_href))
		return [len(all_page_href),all_page_href]
	else:
		all_page_href = [ele["href"] for ele in all_page_ele]

		print("Download from {} pages: {}".format(len(all_page_href),all_page_href))
		return [len(all_page_href),all_page_href]

def generate_chap_pages(first_half_url,last_pg_str):
	# RETURNS string[] - urls of all the chap_pages
	return [first_half_url+str(i) for i in range(int(last_pg_str)+1)]

def page_url_to_name(page_url):
	return page_url.split("/")[-1]

def download_img_from_page(page_url,chp_name,name):
	# downloads one image from a page

	# Get info to download image
	img_url = img_url_from_page_url(page_url,True)
	ext = get_img_ext(img_url)

	# Download image
	download_img(img_url,chp_name,name,ext)


def img_url_from_page_url(page_url,get_loadfail = False):
	# Get img url
	html = s.get(page_url,headers=user_agent).content
	soup = BeautifulSoup(html,"html.parser")
	ele_list = soup.findAll("img",{"id":"img"})
	img_url = ele_list[0]["src"]

	if get_loadfail:
		# set loadfail url
		loadfail_url_section = soup.findAll("a",{"id":"loadfail"})[0]["onclick"]
		loadfail_url = loadfail_url_section.split("'")[1]
		threading.current_thread().loadfail = page_url+"?nl="+loadfail_url #!@#!@#!@#
	
	return img_url


def get_img_ext(img_url):
	# RETURN: extension
	return img_url.split(".")[-1]


def download_img(img_url,chp_name,name,ext):

	potential_file_bin = get_img_bin(img_url,0,name)

	if not potential_file_bin == 0:
		img_file = open("{}/{}.{}".format(chp_name,name,ext),"wb")
		img_file.write(potential_file_bin)
		img_file.close()
		print("{} saved".format(name))
	else:
		pass

def get_img_bin(img_url,num_of_tries,name):

	num_of_tries+=1
	try:
		return s.get(img_url,headers=user_agent,timeout=30).content
	except Exception as err:
		print("ERROR:",err)
		if num_of_tries >= 3:
			return get_img_bin_loadfail(img_url,num_of_tries,name)
			
		print("Trying to download {} again. Total Download Attempts: {}".format(name,num_of_tries))
		return get_img_bin(img_url,num_of_tries,name)

def get_img_bin_loadfail(img_url,num_of_tries,name):
	print("### Attempting to use loadfail for image {} link after {} attempts".format(name,num_of_tries))
	global unable_to_download


	# get loadfail page image src 
	try:
		img_url = img_url_from_page_url(threading.current_thread().loadfail)
	except:
		return 0

	# try to get loadfail page IMAGE data
	while num_of_tries < 5:
		num_of_tries+=1
		
		try:
			return s.get(img_url,headers=user_agent,timeout=30).content
		except Exception as err:
			print("ERROR:",err)
			print("Aborting image download for image '{}'. A max of {} attempts was reached".format(name,num_of_tries))
	
	unable_to_download.append((name,threading.current_thread().info[1]))
	return 0


# num_chap_pages_and_next_links("https://e-hentai.org/g/1846633/c6d614fbbf/")
# download_img("https://pejbhim.hwxbgtmqrlbd.hath.network:6568/h/5182868199a47d35caee2c39026cf67755889bf8-109630-584-1262-jpg/keystamp=1613198100-3870178735;fileindex=81079955;xres=2400/76008129_p1.jpg",".","tester","jpg")
# download_chapter("https://e-hentai.org/g/1809737/2db6b8f48e/")

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

