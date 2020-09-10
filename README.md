邏輯客
==
邏輯客為一款線上新聞彙整暨公民討論平台的App。觀察人類會從不同角度切入同一事件的需求，打造一個彙整同一事件新聞且提供各種角度供使用者討論的平台。

__新聞分類__

利用爬蟲(Crawler)技術抓取五大新聞平台之即時新聞。將新聞以「議題」為主題分類，將講述同一主題的新聞整合一起，供使用者可以從不同新聞平台與不同角度追蹤同一事件。

例如:Apple發表新機，將五大新聞平台與Apple新機發表相關的新聞都彙整在一起。

__討論區__

設計分層式討論區供使用者討論。使用者可以針對同一事件從不同角度討論，可以建立類別表示要從哪個角度切入討論此事件。

例如:Apple新機可以從鏡頭、螢幕與價格等角度切入，就可以針對這些角度建立類別，從這些角度開設討論區。

負責項目
==
爬蟲抓取新聞(News_Crawler)
---
利用爬蟲抓取蘋果日報、自由時報、ETNEWS新聞、聯合新聞網及中時電子報五大新聞網站之即時新聞。不同的網站，網站架構不同，因此每個網站都有專門的爬蟲程式。利用Python中BeautifulSoup套件抓取每一篇新聞之連結、標題、發布時間、新聞點閱率及新聞文章內容。最後用MySQLdb套件將新聞存到MySQL資料庫當中。

將新聞以議題分類(News_Classify)
---
利用jieba中文斷詞套件中的關鍵字提取功能抓取該新聞的關鍵字，jieba關鍵字提取是以TF-IDF算法計算字詞之權重。再利用停用詞(Stop words)過濾掉累贅詞，剩餘的關鍵詞以餘弦相似度(cosine similarity)計算兩兩新聞的相似程度，將相似程度高的新聞歸類為同一類新聞。

UI
---
登入畫面
---
![image](https://github.com/tingnli6603/Logic/blob/master/Layout/2017-09-09%20(1).png)

首頁-四大新聞議題
---
![image](https://github.com/tingnli6603/Logic/blob/master/Layout/2017-09-09%20(2).png)

新聞區
---
![image](https://github.com/tingnli6603/Logic/blob/master/Layout/2017-09-09%20(3).png)

新聞內容
---
![image](https://github.com/tingnli6603/Logic/blob/master/Layout/2017-09-09%20(4).png)

討論區
---
![image](https://github.com/tingnli6603/Logic/blob/master/Layout/2017-09-09%20(5).png)

建議轉版介面
---
![image](https://github.com/tingnli6603/Logic/blob/master/Layout/2017-09-09%20(6).png)

留言回應區
---
![image](https://github.com/tingnli6603/Logic/blob/master/Layout/2017-09-09%20(7).png)

檢舉介面
---
![image](https://github.com/tingnli6603/Logic/blob/master/Layout/2017-09-09%20(8).png)
