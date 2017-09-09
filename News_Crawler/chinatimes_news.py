#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import MySQLdb
import datetime

db=MySQLdb.connect("localhost","root","ji3g4xu3wu/6p ","logic",charset='utf8')          #資料庫連接
cursor=db.cursor()


now_date=int(datetime.datetime.now().strftime("%d"))


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


for page_num in range(1,55):

	res_news_list = requests.get("http://www.chinatimes.com/realtimenews/?page="+repr(page_num))
	res_news_list.encodeing = 'utf8'
	soup_news_list = BeautifulSoup(res_news_list.text)
	
	news_listRight = soup_news_list.findAll("div",{'class':'listRight'})[0]
	for news_list in news_listRight.findAll("li",{'class':'clear-fix'}):
		
		news_time = news_list.time['datetime']
                re_time = re.sub("[/:]"," ",news_time).split()

		if (int(re_time[2])==now_date):

			news_list_h2 = news_list.select('h2')[0]
			href = "http://www.chinatimes.com/"+news_list_h2.a['href']

			if (re.sub("\W","",href) not in db_href):

				primary_num=primary_num+1
	                        sql_num="INSERT INTO news (news_id) VALUES (%d)" %primary_num
        	                cursor.execute(sql_num)
                	        db.commit()

                        	source="中時電子報"
	                        sql_source="UPDATE news SET news_jour = '%s' WHERE news_id= (%d)" %(source,primary_num)
        	                cursor.execute(sql_source)
                	        db.commit()

				sql_href="UPDATE news SET news_oriLink = '%s' WHERE news_id= (%d)" %(href,primary_num)
	                        cursor.execute(sql_href)
        	                db.commit()

				title = news_list_h2.text.strip().encode('utf8')
				sql_title="UPDATE news SET news_title = '%s' WHERE news_id= (%d)" %(title,primary_num)
	                        cursor.execute(sql_title)
        	                db.commit()

				time = datetime.datetime(int(re_time[0]),int(re_time[1]),int(re_time[2]),int(re_time[3]),int(re_time[4]))
				sql_time="UPDATE news SET news_time = ('%s') WHERE news_id= (%d)" %(time,primary_num)
	                        cursor.execute(sql_time)
        	                db.commit()

				res_news_article = requests.get(href)
				res_news_article.encoding = 'utf8'
                        	soup_news_article=BeautifulSoup(res_news_article.text)

				news_click = soup_news_article.findAll("div",{'class':'art_click clear-fix'})[0]
				if (news_click.findAll("span",{'class':'num'})):
					CTR = news_click.findAll("span",{'class':'num'})[0].text
					sql_CTR="UPDATE news SET news_oriClick = (%d) WHERE news_id= (%d)" %(int(CTR),primary_num)
	        	                cursor.execute(sql_CTR)
        	        	        db.commit()

				article=""
                        	html_news_article = soup_news_article.findAll("article",{'class':'clear-fix'})[0]
                        	for news_article in html_news_article.select('p'):
                                	re_article=re.sub("\<.*?\>","",news_article.encode('utf8'))
                                	article=article+re_article+"\n"

                        	sql_article="UPDATE news SET news_content = ('%s') WHERE news_id= (%d)" %(article.replace("'","’"),primary_num)
                        	cursor.execute(sql_article)
				db.commit()
			else:
				break
		else:
			break

db.close()
