#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import MySQLdb
import datetime

#連接資料庫
db=MySQLdb.connect("localhost","root","ji3g4xu3wu/6p ","logic",charset='utf8')
cursor=db.cursor()

#今天的日期
now_date=int(datetime.datetime.now().strftime("%d"))

#取得新聞編號的最大號碼
pri_sql="SELECT (news_id) FROM news"
cursor.execute(pri_sql)
pri_result = cursor.fetchall()

for pri_num in pri_result:
        for primary_num in pri_num:
                primary_num

#將所有新聞的網址存到陣列中，用來檢查使否已經存在資料庫。重新執行一次程式，如果新聞連結已經在資料庫，就不更新
db_href=[]
cursor.execute("SELECT news_oriLink FROM news")
href_result=cursor.fetchall()
for db_href1 in href_result:
        for db_href2 in db_href1:
                db_href.append(re.sub("\W","",db_href2))


#因為當天的新聞大概都到26頁，不抓非當天的新聞
for page_num in range(1,26):

	#此連結為即時新聞頁面，上面有所有新聞標題，每則新聞依照發稿時間排序
	res_news_homepage =requests.get("http://www.appledaily.com.tw/realtimenews/section/new/"+repr(page_num))
	res_news_homepage.encoding = 'utf8'
	soup_news_homepage=BeautifulSoup(res_news_homepage.text)

	#依照網頁的標籤進行爬蟲，這裡抓到的是每一則新聞的連結
	for news_list in soup_news_homepage.findAll("li",{'class':'rtddt'}):

		href = "http://www.appledaily.com.tw"+news_list.a['href'].encode('utf8')

		if (re.sub("\W","",href) not in db_href):

			#開啟每一則新聞，抓取需要的新聞文字
			res_news_article=requests.get(href)
            res_news_article.encoding = 'utf8'
            soup_news_article=BeautifulSoup(res_news_article.text)

			#抓取新聞發布日期，判斷是否為當天新聞
			news_time = soup_news_article.findAll("div",{'class':'gggs'})[0].text.encode('utf8')
			re_time = re.sub("[年月日:]"," ",news_time).split()
			if (int(re_time[2])==now_date):

				#新聞編號+1
				primary_num=primary_num+1
                        	sql_num="INSERT INTO news (news_id) VALUES (%d)" %primary_num
                        	cursor.execute(sql_num)
                        	db.commit()
				#新聞連結
				sql_href="UPDATE news SET news_oriLink = '%s' WHERE news_id= (%d)" %(href,primary_num)
                       		cursor.execute(sql_href)
                        	db.commit()
							
				#新聞來源
				source="蘋果日報"
	                        sql_source="UPDATE news SET news_jour = '%s' WHERE news_id= (%d)" %(source,primary_num)
        	                cursor.execute(sql_source)
                	        db.commit()

				#新聞標題
				title = soup_news_article.findAll("h1",{'id':'h1'})[0].text.encode('utf8')
				sql_title="UPDATE news SET news_title = '%s' WHERE news_id= (%d)" %(title,primary_num)
                        	cursor.execute(sql_title)
                        	db.commit()

				#新聞時間，轉成datetime型態
				time = datetime.datetime(int(re_time[0]),int(re_time[1]),int(re_time[2]),int(re_time[3]),int(re_time[4]))
				sql_time="UPDATE news SET news_time = ('%s') WHERE news_id= (%d)" %(time,primary_num)
                        	cursor.execute(sql_time)
                        	db.commit()

				#新聞點閱率
				news_clicked = soup_news_article.findAll("a",{'class':'function_icon clicked'})[0].text.encode('utf8')
				CTR = int(re.sub("[人氣()]","",news_clicked))
				sql_CTR="UPDATE news SET news_oriClick = (%d) WHERE news_id= (%d)" %(int(CTR),primary_num)
                        	cursor.execute(sql_CTR)
                        	db.commit()

				#新聞文章內容
				news_article = soup_news_article.findAll("p",{'id':'summary'})[0]
                        	replace_article = news_article.encode('utf8').replace("<span style=\"height:30px;display:block;\">","\n")
                        	re_article=re.sub("\<.*?\>","",replace_article)
                        	sql_article="UPDATE news SET news_content = ('%s') WHERE news_id= (%d)" %(re_article.replace("'","’"),primary_num)
                        	cursor.execute(sql_article)
                        	db.commit()

			else:
				break

		else:
			break
db.close()
