#!/usr/bin/env python
# -*- coding: utf8 -*-

import numpy as np
import jieba
import jieba.analyse
import MySQLdb

#餘弦相似度
def get_cossimi(x,y):
        myx=np.array(x)
        myy=np.array(y)
        cos1=np.sum(myx*myy)
        cos21=np.sqrt(sum(myx*myx))
        cos22=np.sqrt(sum(myy*myy))
        return cos1/float(cos21*cos22)

#匯入中文辭庫
jieba.set_dictionary('dict.txt.big.txt')

#連接資料庫
db=MySQLdb.connect("localhost","root","ji3g4xu3wu/6p ","logic",charset='utf8')
cursor=db.cursor()


#尋找資料庫某一篇新聞當作樣本新聞
samplenews_num=input('Sample news:')
samplenews_sql="SELECT news_content,news_title FROM news WHERE news_id= %d " %samplenews_num
cursor.execute(samplenews_sql)
samplenews_result = cursor.fetchone()

#content1為樣本新聞的新聞內容
samplenews_content=samplenews_result[0] 
print "sample title:"+samplenews_result[1]


#找尋資料庫內所有新聞
allnews_sql="SELECT news_id,news_content,news_title,news_jour,news_oriClick FROM news"
cursor.execute(allnews_sql)
allnews_result = cursor.fetchall()

#停用詞
stopwords=open('stopwords.txt','rb').read()

#利用jieba的關鍵字提取，比較樣本新聞跟每一篇新聞的餘弦相似度
news_count=0
for allnews in allnews_result:
	
	#新聞內容有可能為空值
	if (allnews[1]==None):
		continue

	allnews_content = allnews[1]

	#jieba關鍵字提取
	samplenews_keywords = jieba.analyse.extract_tags(samplenews_content,withWeight=True, topK=30)
	allnews_keywords = jieba.analyse.extract_tags(allnews_content,withWeight=True, topK=30)

	#將兩篇新聞的關鍵字放到keyword_all內
	keyword_all=[]
	for samplenews_keyword in samplenews_keywords:
		if samplenews_keyword[0].encode('utf8') not in stopwords: #不在停用詞內
			keyword_all.append(samplenews_keyword[0])

	for allnews_keyword in allnews_keywords:
		if allnews_keyword[0].encode('utf8') not in stopwords:
			keyword_all.append(allnews_keyword[0])

	samplenews_dict={}
	allnews_dict={}
	
	#將兩篇新聞所有關鍵字存成一個dictionary，值為0
	for keyword in keyword_all:
		samplenews_dict[keyword]=0
	
	#如果新聞內有一樣的關鍵字，則該關鍵字值為1
	for samplenews_word in samplenews_keywords:
		if samplenews_dict.has_key(samplenews_word[0]):
			samplenews_dict[samplenews_word[0]]+=samplenews_word[1]

	for keyword in keyword_all:
        	allnews_dict[keyword]=0

	for allnews_word in allnews_keywords:
        	if allnews_dict.has_key(allnews_word[0]):
               		allnews_dict[allnews_word[0]]+=allnews_word[1]

	samplenews_data=[]
	allnews_data=[]

	#兩個dictionary內的分別存到陣列內，再以餘弦相似度計算
	for key in keyword_all:
        	samplenews_data.append(samplenews_dict[key])
        	allnews_data.append(allnews_dict[key])

	testsimi=get_cossimi(samplenews_data,allnews_dict)

	#如果相似度值大於0.2，則取該篇新聞為相似
	if (testsimi>=0.2):
		news_count+=1
		print allnews[0],
		print allnews[2],
		print allnews[3],
		print allnews[4],
		print "------",
		print testsimi

		sql_newsbel="INSERT INTO news_bel SET issue_id='%d' , news_id='%d' " %(1,allnews[0])
		cursor.execute(sql_newsbel)
		db.commit()
print "總數:"+str(news_count)
db.close()