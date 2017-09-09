#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import MySQLdb
import datetime

db=MySQLdb.connect("localhost","root","ji3g4xu3wu/6p ","logic",charset='utf8')              #資料庫連接
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


for page_num in range(1,30):
	res_newslist=requests.get("http://news.ltn.com.tw/list/BreakingNews?page="+repr(page_num))
	res_newslist.encoding = 'utf8'
	newslist_soup=BeautifulSoup(res_newslist.text)

	for newslist in newslist_soup.findAll("li",{'class':'lipic'}):

		news_time=newslist.span.text.encode('utf8')
		re_time=re.sub("[-:]"," ",news_time).split()

		if (int(re_time[2])==now_date):

			href=newslist.select('a')[1]['href']

			if (re.sub("\W","",href) not in db_href):

				primary_num=primary_num+1               #primary輸入資料庫
                        	sql_num="INSERT INTO news (news_id) VALUES (%d)" %primary_num
                        	cursor.execute(sql_num)
                        	db.commit()

				source="自由時報"
                                sql_source="UPDATE news SET news_jour = '%s' WHERE news_id= (%d)" %(source,primary_num)
                                cursor.execute(sql_source)
                                db.commit()

				title=newslist.select('a')[1].text.encode('utf8')
				sql_title="UPDATE news SET news_title = '%s' WHERE news_id= (%d)" %(title,primary_num)
                        	cursor.execute(sql_title)
                        	db.commit()

				time=datetime.datetime(int(re_time[0]),int(re_time[1]),int(re_time[2]),int(re_time[3]),int(re_time[4]))
				sql_time="UPDATE news SET news_time = ('%s') WHERE news_id= (%d)" %(time,primary_num) #datetime輸入資料庫
                        	cursor.execute(sql_time)
                        	db.commit()

				sql_href="UPDATE news SET news_oriLink = '%s' WHERE news_id= (%d)" %(href,primary_num)
                        	cursor.execute(sql_href)
                        	db.commit()

				tab=newslist.a['class'][0]
				if tab in ["tab1","tab2","tab3","tab4","tab5","tab7"]:

					res_newspage1=requests.get(href)
					res_newspage1.encoding = 'utf8'
					newspage1_soup = BeautifulSoup(res_newspage1.text)

					newstext=newspage1_soup.findAll("div",{'id':'newstext'})[0].encode('utf8')

					pic600=""
					if newspage1_soup.findAll("div",{'class':'pic600'}):
				        	pic600=pic600+newspage1_soup.findAll("div",{'class':'pic600'})[0].encode('utf8')

					newspic=""
					if newspage1_soup.findAll("div",{'id':'newspic'}):
				        	newspic=newspic+newspage1_soup.findAll("div",{'id':'newspic'})[0].encode('utf8')

					re_newstext=newstext.replace(pic600,"").replace(newspic,"")
					re_newstext_soup=BeautifulSoup(re_newstext)

					article1=""
					for content1 in re_newstext_soup.select('p'):
						article1=article1+content1.text.encode('utf8')+"\n"

					sql_article1="UPDATE news SET news_content = ('%s') WHERE news_id= (%d)" %(article1.replace("'","’"),primary_num)
                       			cursor.execute(sql_article1)
                        		db.commit()

				elif tab in ["tab8","tab10"]:

					res_newspage2=requests.get(href)
                                	res_newspage2.encoding = 'utf8'
                                	newspage2_soup = BeautifulSoup(res_newspage2.text)

					article2=""
					for content2 in newspage2_soup.select('p'):
				        	if content2.findAll("span",{'class':'ph_d1'}):
				                	continue
				        	if content2.select('strong'):
				                	continue
				        	article2=article2+content2.text.encode('utf8')+"\n"

					sql_article2="UPDATE news SET news_content = ('%s') WHERE news_id= (%d)" %(article2.replace("'","’"),primary_num)
                        		cursor.execute(sql_article2)
                        		db.commit()

			else:
				break

db.close()
