import queue
import threading

import cv2


class ClearingQueue(queue.Queue):
  def put(self, item):
    while True:
      try:
        super().put(item, block=False)
      except queue.Full:
        _ = self.get_nowait()
      else:
        break


class Pynopticon:
  def __init__(self, record_frames=100, width=640, height=480):
    self.record_frames = record_frames
    self.queue = ClearingQueue(maxsize=record_frames)
    self.stopped = False
    self.t = None

    self.width = width
    self.height = height

  def start(self):
    """ Start the video capture. """
    cap = cv2.VideoCapture(0)

    def _record():
      while not self.stopped:
        ret, frame = cap.read()
        if not ret:
          break

        frame = cv2.resize(frame, (self.width, self.height))
        self.queue.put(frame)

    self.stopped = False
    self.t = threading.Thread(target=_record)
    self.t.start()

  def stop(self):
    """ Stop without saving. """
    self.stopped = True
    self.t.join()

  def reset(self):
    """ Reset queue. """
    self.queue = ClearingQueue(maxsize=record_frames)

  def save(self, outname: str = "output.avi", fps: int = 15):
    """ Stop and save. """
    self.stop()

    out = cv2.VideoWriter(outname, cv2.VideoWriter_fourcc(*"DIVX"), fps, (self.width, self.height))

    while True:
      try:
        frame = self.queue.get_nowait()
        out.write(frame)
      except queue.Empty:
        break

    out.release()

