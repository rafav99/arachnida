import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import argparse

img_number = 0

parser = argparse.ArgumentParser(description='Get images from URL')
parser.add_argument('url')
parser.add_argument('-r', '--isrec', action='store_true')
parser.add_argument('-l', '--recnum', type=int)
parser.add_argument('-p', '--path', type=str)
args = parser.parse_args()	
url = args.url
if not args.isrec:
	depth = 1
	if args.recnum:
		print("Error: -l needs -r first")
		exit()
else:
	if not args.recnum:
		depth = 5
	else:
		depth = args.recnum
if not args.path:
	path = "data"
else:
	path = args.path

def download_img(image_url_list):
	global img_number
	if not os.path.exists(path):
		os.mkdir(path)
	for url in image_url_list:
		img_number += 1
		img_type = url.split(".")[-1]
		try:
			img_get = requests.get(url, timeout=5)
		except:
			pass
		filename = os.path.join(path, f"image_{img_number}.{img_type}")
		with open(filename, "wb") as f:
			for chunk in img_get.iter_content(1024):
				f.write(chunk)
		print(f"Image {img_number} downloaded and saved as {filename}")

def get_images(url, soup, depth):
	global absol_img_list
	image_url_list = []
	img_tags = soup.find_all("img")
	image_tags = soup.find_all("image")
	for img in img_tags:
		src = img.get("src")
		src = urllib.parse.urljoin(url, src)
		if src and src not in absol_img_list and src.endswith(tuple(img_extensions)):			
				image_url_list.append(src)
				absol_img_list.append(src)
	for img in image_tags:
		src = img.get("href")
		src = urllib.parse.urljoin(url, src)
		if src and src not in absol_img_list and src.endswith(tuple(img_extensions)):			
				image_url_list.append(src)
				absol_img_list.append(src)
	download_img(image_url_list)
   
def get_links(url, depth):
	depth -= 1
	try:
		response = requests.get(url, timeout=5)
		soup = BeautifulSoup(response.content, "html.parser")
		a_item  = soup.find_all("a")
		link_url_list = []
		for a in a_item:
			if "href" in a.attrs:
				link_url = a["href"]
				link_url = urllib.parse.urljoin(url, link_url)
				if web_name in link_url and link_url not in absol_list:
					if link_url.split(".")[-1] not in unwanted_extensions:
						link_url_list.append(link_url)
						absol_list.append(link_url)
		if depth > 0:
			for link in link_url_list:
				get_links(link, depth)
		get_images(url, soup, depth)
	except:
		print("could not enter link")

img_extensions = [".jpg", ".png", ".bmp", ".gif", ".jpeg"]
unwanted_extensions = ["pdf", "zip", "doc", "xls", "png", "jpg", "jpeg", "gif", "mp3", "mp4", "avi", "csv", "exe", "rar", "tar", "gz", "ppt", "pptx", "xlsx", "docx"]
try:
	web_name = url.split("/")[2]
except:
	print("Wrong format")
absol_list = [url]
absol_img_list = []
get_links(url, depth)
