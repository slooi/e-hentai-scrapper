import threading
from bs4 import BeautifulSoup 
import requests

import re


# scrape webpage for all image page urls

# navigate to each page urls and get image url

# download all images


text = """
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"><head>
<title>[Pixiv] J9歌劇団 (J9)</title>
<link rel="stylesheet" type="text/css" href="https://e-hentai.org/z/0348/g.css">
</head>
<body>
<script type="text/javascript">
function popUp(URL,w,h) {
	window.open(URL,"_pu"+(Math.random()+"").replace(/0\./,""),"toolbar=0,scrollbars=0,location=0,statusbar=0,menubar=0,resizable=0,width="+w+",height="+h+",left="+((screen.width-w)/2)+",top="+((screen.height-h)/2));
	return false;
}
</script>
<div id="i1" class="sni" style="width: 1300px; max-width: 1137px;"><h1>[Pixiv] J9歌劇団 (J9)</h1><div id="i2"><div class="sn"><a onclick="return load_image(1, 'f12bbdcbeb')" href="https://e-hentai.org/s/f12bbdcbeb/1846305-1"><img src="https://ehgt.org/g/f.png"></a><a id="prev" onclick="return load_image(1, 'f12bbdcbeb')" href="https://e-hentai.org/s/f12bbdcbeb/1846305-1"><img src="https://ehgt.org/g/p.png"></a><div><span>1</span> / <span>31</span></div><a id="next" onclick="return load_image(2, '15d8ae7252')" href="https://e-hentai.org/s/15d8ae7252/1846305-2"><img src="https://ehgt.org/g/n.png"></a><a onclick="return load_image(31, '70e7bbad02')" href="https://e-hentai.org/s/70e7bbad02/1846305-31"><img src="https://ehgt.org/g/l.png"></a></div><div>1.jpg :: 1280 x 1808 :: 424.3 KB</div></div><script async="" src="//adserver.juicyads.com/js/jads.js"></script><ins id="265909" data-width="728" data-height="90"></ins><script>(adsbyjuicy = window.adsbyjuicy || []).push({'adzone':265909});</script><div id="i3"><a onclick="return load_image(2, '15d8ae7252')" href="https://e-hentai.org/s/15d8ae7252/1846305-2"><img id="img" src="https://vrhhaik.dnhrkwvhhewd.hath.network/h/f796a7782ba62b748611b37ab2993638d99ae113-434478-1280-1808-jpg/keystamp=1613140800-168f191d25;fileindex=89651824;xres=1280/1.jpg" style="height: 1808px; width: 1280px; max-width: 1117px; max-height: 1578px;" onerror="this.onerror=null; nl('33130-448094')"></a></div><script async="" src="//adserver.juicyads.com/js/jads.js"></script><ins id="249007" data-width="728" data-height="90"></ins><script>(adsbyjuicy = window.adsbyjuicy || []).push({'adzone':249007});</script><div id="i4"><div>1.jpg :: 1280 x 1808 :: 424.3 KB</div><div class="sn"><a onclick="return load_image(1, 'f12bbdcbeb')" href="https://e-hentai.org/s/f12bbdcbeb/1846305-1"><img src="https://ehgt.org/g/f.png"></a><a id="prev" onclick="return load_image(1, 'f12bbdcbeb')" href="https://e-hentai.org/s/f12bbdcbeb/1846305-1"><img src="https://ehgt.org/g/p.png"></a><div><span>1</span> / <span>31</span></div><a id="next" onclick="return load_image(2, '15d8ae7252')" href="https://e-hentai.org/s/15d8ae7252/1846305-2"><img src="https://ehgt.org/g/n.png"></a><a onclick="return load_image(31, '70e7bbad02')" href="https://e-hentai.org/s/70e7bbad02/1846305-31"><img src="https://ehgt.org/g/l.png"></a></div></div><div id="i5"><div class="sb"><a href="https://e-hentai.org/g/1846305/3b40753564/"><img src="https://ehgt.org/g/b.png" referrerpolicy="no-referrer"></a></div></div><div id="i6" class="if"> &nbsp; <img src="https://ehgt.org/g/mr.gif" class="mr"> <a href="https://e-hentai.org/?f_shash=f12bbdcbeb6032b571fa8fadf785deb392f0756b&amp;fs_from=1.jpg+from+%5BPixiv%5D+J9%E6%AD%8C%E5%8A%87%E5%9B%A3+%28J9%29">Show all galleries with this file</a>  &nbsp; <img src="https://ehgt.org/g/mr.gif" class="mr"> <a href="#" onclick="prompt('Copy the URL below.', 'https://e-hentai.org/r/f796a7782ba62b748611b37ab2993638d99ae113-434478-1280-1808-jpg/forumtoken/1846305-1/1.jpg'); return false">Generate a static forum image link</a>  &nbsp; <img src="https://ehgt.org/g/mr.gif" class="mr"> <a href="#" id="loadfail" onclick="return nl('33130-448094')">Click here if the image fails loading</a> </div><div id="i7" class="if"> &nbsp; <img src="https://ehgt.org/g/mr.gif" class="mr"> <a href="https://e-hentai.org/fullimg.php?gid=1846305&amp;page=1&amp;key=osf9g3c9lr2">Download original 1494 x 2110 894.6 KB source</a></div></div><script type="text/javascript">var gid=1846305;var startpage=1;var startkey="f12bbdcbeb";var showkey="bjzyggm9lr2";var base_url="https://e-hentai.org/";var api_url = "https://api.e-hentai.org/api.php";var prl=0;var si="33130";var xres = 1280;var yres = 1808;</script><script type="text/javascript" src="https://e-hentai.org/z/0348/ehg_show.c.js"></script><div class="dp" style="margin:-5px auto 5px"><a href="https://e-hentai.org/">Front Page</a> &nbsp; <a href="https://e-hentai.org/tos.php">Terms of Service</a> &nbsp; <a href="mailto:luke@juicyads.com">Advertise</a></div>


</body></html>
"""


user_agent = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0"
}
def download_chapter(chap_url):
	# Downloads all the imgs of this chapter

	# get all page urls
	page_urls = get_all_page_urls(chap_url)

	for page_url in page_urls:
		name = page_url_to_name(page_url)
		download_img_from_page(page_url,name)


def get_all_page_urls(chap_url):
	# RETURN: 
	html = requests.get(chap_url,headers=user_agent).content
	soup = BeautifulSoup(html,"html.parser")

	# get link to img pages from images' parents
	img_ele_list_unfiltered = soup.findAll("img",{"alt":re.compile(r"\d*")})
	img_ele_list = [img for img in img_ele_list_unfiltered if re.match(r"\d*",img["alt"]).end()>0]
	page_urls = [img.parent["href"] for img in img_ele_list]

	return page_urls

def page_url_to_name(page_url):
	return page_url.split("/")[-1]

def download_img_from_page(page_url,name):
	# downloads one image from a page

	# Get info to download image
	img_url = img_url_from_page_url(page_url)
	ext = get_img_ext(img_url)

	# Download image
	download_img(img_url,name,ext)


def img_url_from_page_url(page_url):
	html = requests.get(page_url,headers=user_agent).content
	print("html",html)
	soup = BeautifulSoup(html,"html.parser")
	ele_list = soup.findAll("img",{"id":"img"})
	print("ele_list:",ele_list)
	print("img_url:",ele_list[0]["src"])
	return ele_list[0]["src"]


def get_img_ext(img_url):
	# RETURN: extension
	return img_url.split(".")[-1]


def download_img(img_url,name,ext):
	img_file = open("{}.{}".format(name,ext),"wb")
	img_file.write(requests.get(img_url).content)
	img_file.close()

download_chapter("https://e-hentai.org/g/1846305/3b40753564/")
# download_img_from_page("https://e-hentai.org/s/f12bbdcbeb/1846305-1")
# download_img("https://vrhhaik.dnhrkwvhhewd.hath.network/h/f796a7782ba62b748611b37ab2993638d99ae113-434478-1280-1808-jpg/keystamp=1613139300-525a4ae9be;fileindex=89651824;xres=1280/1.jpg")