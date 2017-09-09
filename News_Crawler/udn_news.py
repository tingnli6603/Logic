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


for page_num in range(1,8):

        res_breaknews=requests.get("http://udn.com/news/breaknews/1/0/"+repr(page_num))
        res_breaknews.encoding='utf8'
        soup_breaknews=BeautifulSoup(res_breaknews.text)

	breaknews_body=soup_breaknews.findAll("div",{'id':'breaknews_body'})[0]

        for news_list in breaknews_body.select('dt'):

		news_time = news_list.findAll("div",{'class':'dt'})[0].text.encode('utf8')
                re_time=re.sub("[-:]"," ",news_time).split()

		if (int(re_time[1])==now_date):

			href = "http://udn.com"+news_list.a['href']

			if (re.sub("\W","",href) not in db_href):

				primary_num=primary_num+1
                                sql_num="INSERT INTO news (news_id) VALUES (%s)" %(primary_num)
                                cursor.execute(sql_num)
                                db.commit()

                                source="聯合新聞網"
                                sql_source="UPDATE news SET news_jour = '%s' WHERE news_id= (%d)" %(source,primary_num)
                                cursor.execute(sql_source)
                                db.commit()

				sql_href="UPDATE news SET news_oriLink = '%s' WHERE news_id= (%d)" %(href,primary_num)
                                cursor.execute(sql_href)
                                db.commit()

				title = news_list.select("h2")[0].contents[0].encode('utf8')
				sql_title="UPDATE news SET news_title = '%s' WHERE news_id= (%d)" %(title,primary_num)
                                cursor.execute(sql_title)
                                db.commit()

				CTR = news_list.findAll("div",{'class':'view'})[0].text.encode('utf8')
				sql_CTR="UPDATE news SET news_oriClick = (%d) WHERE news_id= (%d)" %(int(CTR),primary_num)
                                cursor.execute(sql_CTR)
                                db.commit()

				time=datetime.datetime(now_year,int(re_time[0]),int(re_time[1]),int(re_time[2]),int(re_time[3]))
				sql_time="UPDATE news SET news_time = ('%s') WHERE news_id= (%d)" %(time,primary_num)
                                cursor.execute(sql_time)
                                db.commit()


				res_article=requests.get(href)
                        	res_article.encoding = 'utf8'
	                        soup_article = BeautifulSoup(res_article.text)

        	                story_body_content=soup_article.findAll("div",{'id':'story_body_content'})[0]

	                        for script in story_body_content.select('script'):
        	                	re_script_article=story_body_content.encode('utf8').replace(script.encode('utf8'),"")

                	        re_p_article=re_script_article.replace("<!-- /.photo -->","<p>")
                        	article_soup=BeautifulSoup(re_p_article)

	                        article=""
        	                for word in article_soup.select('p'):
                	        	article=article+word.text.encode('utf8')+"\n"
				sql_article="UPDATE news SET news_content = ('%s') WHERE news_id= (%d)" %(article.replace("'","’").strip(),primary_num)
                                cursor.execute(sql_article)
                                db.commit()

			else:
				break
		else:
			break

db.close()
