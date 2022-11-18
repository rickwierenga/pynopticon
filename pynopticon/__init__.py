import datetime
import queue
import threading

import cv2

from pynopticon.upload_video import initialize_upload, get_authenticated_service


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
  def __init__(self, record_frames=100, width=640, height=480, cam=0, new_frame_callback=None, youtube=None):
    self.record_frames = record_frames
    self.queue = ClearingQueue(maxsize=record_frames)
    self.stopped = False
    self.t = None
    self.cap = None

    self.width = width
    self.height = height
    self.cam = cam

    self.new_frame_callback = new_frame_callback
    self.youtube = youtube

  def start(self):
    """ Start the video capture. """
    self.cap = cv2.VideoCapture(self.cam)

    def _record():
      while not self.stopped:
        ret, frame = self.cap.read()
        if not ret:
          break

        frame = cv2.resize(frame, (self.width, self.height))
        self.queue.put(frame)
        if self.new_frame_callback is not None:
          self.new_frame_callback(frame)

    self.stopped = False
    self.t = threading.Thread(target=_record)
    self.t.start()

  def stop(self):
    """ Stop without saving. """
    self.stopped = True
    self.t.join()
    self.cap.release()

  def reset(self):
    """ Reset queue. """
    self.queue = ClearingQueue(maxsize=self.record_frames)

  def save(self, outname: str = "output.avi", fps: int = 15, upload=False, title=None, description=None):
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

    if upload:
      assert self.youtube is not None, "Youtube client not initialized"

      time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

      try:
        vidid = initialize_upload(self.youtube,
          title=title or f"Epic fail: {outname}",
          description=description or ("Pynopticon capture from " + time),
          category="22",
          tags=[],
          privacyStatus="private",
          file=outname)
        return vidid
      except HttpError as e: 
        return "An HTTP error %d occurred when uploading: %s" % (e.resp.status, e.content)
    
    return None
