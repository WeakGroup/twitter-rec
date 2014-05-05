from twitter_rec import crawler

checkpoint_path = './data/checkpt'
cp = crawler.Checkpointer(checkpoint_path)
c = crawler.Crawler('liaoyisheng89@sina.com', "bigdata", cp)
c.crawl()
