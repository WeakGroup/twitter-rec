# These classes are used for debug purpose only.
import httplib
import urllib2
import StringIO

class VerboseHTTPResponse(httplib.HTTPResponse):
  def _read_status(self):
    s = self.fp.read()
    print '-' * 20, 'Response', '-' * 20
    print s.split('\r\n\r\n')[0]
    self.fp = StringIO.StringIO(s)
    return httplib.HTTPResponse._read_status(self)

class VerboseHTTPSConnection(httplib.HTTPSConnection):
  response_class = VerboseHTTPResponse

  def send(self, s):
    print '-' * 20, 'Request', '-' * 20
    print s.strip()
    print ""
    httplib.HTTPSConnection.send(self, s)


class VerboseHTTPHandler(urllib2.HTTPSHandler):
  def https_open(self, req):
    return self.do_open(VerboseHTTPSConnection, req)
