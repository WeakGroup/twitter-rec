import urllib2
import urllib
import re
import cookielib
import sqlite3
import sys

class Api(object):
    '''
    This Api needs a firefox local cookie to get cookie proteced content from twitter. So pass a
    cookie path as the parameter
    '''
    def __init__(self, cookie_path):
        self.host = 'twitter'
        self.header =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}  # fake a user agent, some websites (like google) don't like automated exploration
        self.cookies_db = self.cookie_path
        if not os.path.exists(filename):
            raise Exception, 'File %s Not Found' % (cookie_path)

        self.cookiejar = self._init_cookies(self.host)
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))

    def _init_cookies(self, host):
        cj = cookielib.LWPCookieJar()
        con = sqlite3.connect(self.cookie_path)
        cur = con.cursor()

        CONTENTS = "host, path, isSecure, expiry, name, value"
        sql = "SELECT {c} FROM moz_cookies WHERE host LIKE '%{h}%'".format(c=CONTENTS, h=host)
        cur.execute(sql)
        for item in cur.fetchall():
            c = cookielib.Cookie(0, item[4], item[5],
                None, False,
                item[0], item[0].startswith('.'), item[0].startswith('.'),
                item[1], False,
                item[2],
                item[3], item[3]=="",
                None, None, {})
            cj.set_cookie(c)
        return cj

    def _connection(url):
        try:
            request = urllib2.Request('https://' + self.host + '.com/' + url, headers = self.header)
            fd = self.opener.open(request)
            return fd.read()
        except urllib2.HTTPError, e:
            print e
            sys.exit(0)
    
    def _save_page(source, filename):
        with open(filaname, 'w') as f:
            print >> f, source

    def verifyCredentials():
        page_source = self._connection('')
        self._save_page(page_source, page)
