import threading 
import time

class Strategy(object):
  def __init__(self, exchange, interval=60, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.args = args
    self.kwargs = kwargs
    self.exchange = exchange
    self.is_running = False
    self.next_call = time.time()

  def _run(self):
    self.is_running = False
    self.start()
    self.run(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False
