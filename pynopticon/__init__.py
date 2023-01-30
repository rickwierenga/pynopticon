import datetime
import queue
import time
import threading

from apiclient.errors import HttpError
import cv2

from pynopticon.upload_video import initialize_upload, get_authenticated_service
from pynopticon.mailer import send_email


MAX_RETRIES = 5
FPS = 10


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
  def __init__(self, record_frames=100, width=640, height=480, cam=0, new_frame_callback=None, youtube=None, sg=None):
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
    self.sg = sg

  def start(self):
    """ Start the video capture. """

    if self.t is not None:
      raise RuntimeError("already started, call stop first")

    def _record():
      print("opening camera", self.cam)
      self.cap = cv2.VideoCapture(f"/dev/video{self.cam}", cv2.CAP_V4L2)
      self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
      print("opened camera")
      retries = 0
      while not self.stopped:
        ret, frame = self.cap.read()
        time.sleep(1 / FPS)
        if not ret or not self.cap.isOpened():
          if retries < MAX_RETRIES:
            self.cap.release()
            self.cap = cv2.VideoCapture(self.cam)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
            retries += 1
            continue
          else:
            break

        frame = cv2.resize(frame, (self.width, self.height))
        self.queue.put(frame)
        if self.new_frame_callback is not None:
          self.new_frame_callback(frame)
      print("! cam exit: ", self.cam)
      self.cap.release()

    self.stopped = False
    self.t = threading.Thread(target=_record, daemon=True)
    self.t.start()

  def stop(self):
    """ Stop without saving. """
    print("stopping")
    self.stopped = True
    self.t.join()
    self.t = None

  def reset(self):
    """ Reset queue. """
    self.queue = ClearingQueue(maxsize=self.record_frames)

  def save(self, outname: str = "output.avi", fps: int = 15, upload=False, title=None, description=None, mail_to:list=None, mail_from=None):
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
      except HttpError as e: 
        return f"An HTTP error {e.resp.status} occurred when uploading: {e.content}"
      
      if vidid is None:
        return None
      
      if mail_to is not None:
        assert self.sg is not None, "Sendgrid client not initialized"
        assert mail_from is not None, "Mail from not specified"

        send_email(
          self.sg,
          to_emails=mail_to,
          from_email=mail_from,
          subject="Pynopticon recorded something!",
          text=f"Video uploaded to https://youtu.be/{vidid}")

      return vidid
    
    return None
