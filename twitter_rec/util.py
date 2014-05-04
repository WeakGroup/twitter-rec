import cPickle
import os
import sys
import threading
import time
import traceback

program_start = time.time()
log_mutex = threading.Lock()

class Logger(object):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    FATAL = 4

    level_to_char = { DEBUG : 'D',
                      INFO : 'I',
                      WARN : 'W',
                      ERROR : 'E',
                      FATAL : 'F', 
                      }

    def __init__(self, level = None):
        if level is None:
            self.level = Logger.INFO
        else:
            self.level = level
    def set_level(self, level):
        self.level = level

    def _log(self, msg, *args, **kw):
      level = kw.get('level', Logger.INFO)
      if level < self.level:
          return
      with log_mutex:
        caller = sys._getframe(kw.get('caller_frame', 2))
        filename = caller.f_code.co_filename
        lineno = caller.f_lineno
        now = time.time() - program_start
        if 'exc_info' in kw:
          exc = ''.join(traceback.format_exc())
        else:
          exc = None
        print >> sys.stderr, '[--%s-- %.3f|%s:%d] %s' % (Logger.level_to_char[level], now, os.path.basename(filename), lineno, msg % args)
        if exc:
          print >> sys.stderr, exc
        
        if level >= Logger.ERROR:
            sys.exit(-1)

    def log_debug(self, msg, *args, **kw): self._log(msg, *args, level=Logger.DEBUG, caller_frame=3)
    def log_info(self, msg, *args, **kw): self._log(msg, *args, level=Logger.INFO, caller_frame=3)
    def log_warn(self, msg, *args, **kw): self._log(msg, *args, level=Logger.WARN, caller_frame=3)
    def log_error(self, msg, *args, **kw): self._log(msg, *args, level=Logger.ERROR, caller_frame=3)
    def log_fatal(self, msg, *args, **kw): self._log(msg, *args, level=Logger.FATAL, caller_frame=3)

    def D(self, msg, *args, **kw): self._log(msg, *args, level=Logger.DEBUG, caller_frame=3)
    def I(self, msg, *args, **kw): self._log(msg, *args, level=Logger.INFO, caller_frame=3)
    def W(self, msg, *args, **kw): self._log(msg, *args, level=Logger.WARN, caller_frame=3)
    def E(self, msg, *args, **kw): self._log(msg, *args, level=Logger.ERROR, caller_frame=3)
    def F(self, msg, *args, **kw): self._log(msg, *args, level=Logger.FATAL, caller_frame=3)

logger = Logger(Logger.DEBUG)

def parse_credential_conf(filename):
    if not os.path.exists(filename):
        logger.F('configuration file not exists %s', filename) 
    
    dic = {}
    logger.D('Parsing credential file %s', filename)
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            else:
                key, value = [x.strip() for x in line.split('=')]
                dic[key] = value
                logger.D('Get key/value [%s|%s]', key, value)
    return dic

def unique_order(list):
  rst = []
  for x in list:
    if x not in rst:
      rst.append(x)
  return rst
