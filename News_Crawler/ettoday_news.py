#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import MySQLdb
import datetime

db=MySQLdb.connect("localhost","root","ji3g4xu3wu/6p ","logic",charset='utf8')
cursor=db.cursor()

now_date=int(datetime.datetime.now().strftime("%d"))
now_month=int(datetime.datetime.now().strftime("%m"))
now_year=int(datetime.datetime.now().strftime("%Y"))

db_href=[]
cursor.execute("SELECT news_oriLink FROM news")
href_result=cursor.fetchall()
for db_href1 in href_result:
        for db_href2 in db_href1:
                db_href.append(re.sub("\W","",db_href2))

pri_sql="SELECT (news_id) FROM news"
cursor.execute(pri_sql)
pri_result = cursor.fetchall()

for pri_num in pri_result:
        for primary_num in pri_num:
                primary_num


for page_num in range(1,21):
	res_news_list=requests.get("http://www.ettoday.net/news/news-list-2016-"+str(now_month)+"-"+str(now_date)+"-0-"+repr(page_num)+".htm")
	res_news_list.encoding='utf8'
	soup_news_list=BeautifulSoup(res_news_list.text)

	all_news_list=soup_news_list.findAll("div",{'id':'all-news-list'})[0]

	for news_line in all_news_list.select('h3'):
		news_time=news_line.select('span')[0].text

		re_time=re.sub("[\[\]/:]"," ",news_time).split()

		if (int(re_time[1])==now_date):

			href=news_line.a['href']
			if (re.sub("\W","",href) not in db_href):

				primary_num=primary_num+1
	                	sql_num="INSERT INTO news (news_id) VALUES (%d)" %(primary_num)
        	        	cursor.execute(sql_num)
                		db.commit()

				source="ETtoday東森新聞雲"
                                sql_source="UPDATE news SET news_jour = '%s' WHERE news_id= (%d)" %(source,primary_num)
                                cursor.execute(sql_source)
                                db.commit()

				title=news_line.select('a')[0].text.encode('utf8')
				sql_title="UPDATE news SET news_title = '%s' WHERE news_id= (%d)" %(title,primary_num)
				cursor.execute(sql_title)
				db.commit()

				time=datetime.datetime(now_year,int(re_time[0]),int(re_time[1]),int(re_time[2]),int(re_time[3]))
				sql_time="UPDATE news SET news_time = ('%s') WHERE news_id= (%d)" %(time,primary_num)
				cursor.execute(sql_time)
				db.commit()

				sql_href="UPDATE news SET news_oriLink = '%s' WHERE news_id= (%d)" %(href,primary_num)
        	                cursor.execute(sql_href)
                	        db.commit()

				res_article=requests.get(href)
				res_article.encoding='utf8'
				soup_article=BeautifulSoup(res_article.text)

				news= soup_article.findAll("div",{'class':'story'})[0]

				article=""
				for news_article in news.select('p'):

					if re.findall("^[▲]",news_article.text.encode('utf8')):
						continue
					if news_article.select('a'):
						continue

					article=article+news_article.text.encode('utf8')+"\n"

				sql_article="UPDATE news SET news_content = ('%s') WHERE news_id= (%d)" %(article.replace("'","’").strip(),primary_num)
				cursor.execute(sql_article)
				db.commit()
			else:
				break

		else:
			break
db.close()
