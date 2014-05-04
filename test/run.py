from twitter_rec import crawler

c = crawler.Crawler('liaoyisheng89@sina.com', "bigdata", "./checkpt.txt")
c.crawl()
