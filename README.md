![Panopticon](./.github/Panopticon.jpg)

# Pynopticon

Pynopticon is a video recording utility that saves the last `n` frames before an interesting event to disk. This is an efficient way to monitor and record systems where you care only about certain moments, and only have information ex post facto (like a crash on a robotic system).

Using the [server](#http-api) you can always see a live video feed.

```python
import time
from pynopticon import Pynopticon

p = Pynopticon(
  record_frames=100,
  width=640,
  height=480,
  cam=0
)
p.start()
time.sleep(10)
p.save(
  outname="my_video.mp4",
  fps=30,
)
```

## Features

#### YouTube Upload

Optionally, you can _upload the video to YouTube_. This requires a `client_secrets.json` file, see instructions [here](https://developers.google.com/youtube/v3/guides/uploading_a_video#Requirements).

```python
import time
from pynopticon import Pynopticon, get_authenticated_service

youtube = get_authenticated_service(client_secrets_file="./client_secrets.json") # initialize youtube
p = Pynopticon(record_frames=100, youtube=youtube)
p.start()
time.sleep(10)
p.save(upload=True, title="My Video", description="My Description")
```

#### Email Notification

If uploading to YouTube, you can also _send an email_ when a video is saved.

```python
import time
from pynopticon import Pynopticon, get_authenticated_service
import sendgrid

sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key) # initialize sendgrid
youtube = get_authenticated_service(client_secrets_file="./client_secrets.json")

p = Pynopticon(record_frames=100, youtube=youtube, sg=sg)
p.start()
time.sleep(10)
p.save(
  upload=True,
  title="My Video", description="My Description",
  to_email=["me@example.com", "other@example.com"],from_email="you@sendgrid.com")
```

#### HTTP API

There is also a server that exposes an _http api_, in case if you want to run Pynopticon on an external device.

```bash
# without YouTube upload:
pynopticon-server

# with YouTube upload:
CLIENT_SECRETS_FILE="client_secrets.json" pynopticon-server
```

**api:**
- `/`: visit in browser for **live streaming**.
- `POST /start`: same as `p.start()` (after stop, server auto starts pynopticon instance).
- `POST /save`: same as `p.save()`.
  - Set `?upload=true` to upload to YouTube. Only works if `CLIENT_SECRETS_FILE` is set.
  - Set `?emails=one@example.com,two@example.com` to send an email to the given emails. Only works if `SENDGRID_API_KEY`, `SENDGRID_FROM` are set, and `upload=true`.
- `POST /stop`: same as `p.stop()`.

**config:**
- `RECORD_FRAMES`: number of frames to record before an event. Default: `100`
- `PORT`: port to run server on. Default: `4004`
- `HOST`: host to run server on. Default: `0.0.0.0`
- `CAM`: camera index. Default: `0`
- `WIDTH`: width of camera. Default: `640`
- `HEIGHT`: height of camera. Default: `480`

If you want to upload to YouTube, you should set the following environment variables:
- `CLIENT_SECRETS_FILE`: path to `client_secrets.json` file. Default: `None`

If all three of the following are set, the server will send an email when a video is uploaded to YT. If just some are set, an error will be raised.
- `SENDGRID_API_KEY`: sendgrid api key. Default: `None`
- `SENDGRID_FROM`: sendgrid from email. Default: `None`

##### Live Streaming

See [HTTP API](#http-api) section above.

## Installation

**Requires OpenCV!**

- from pip

```sh
pip install pynopticon            # basic
pip install 'pynopticon[all]'     # all
pip install 'pynopticon[mail]'    # mail
pip install 'pynopticon[yt]'      # yt
pip install 'pynopticon[server]'  # server
```

- from source

```sh
git clone https://github.com/rickwierenga/pynopticon
```

### Cameras

Plug in a webcam/camera to your computer. We use [this one ($50)](https://www.amazon.com/dp/B01BGBJ8Y0) in lab, but you should be able to use any USB webcam / camera.

Tip: You can use `v4l2-ctl --list-devices` on Linux to find the value you need to pass to `CAM`. This is particularly useful if you're going to be running multiple instances of the Pynopticon.

## Informative

![Schematic of Pynopticon](./.github/figure.png)

_Developed for the Sculpting Evolution Group at the MIT Media Lab_
