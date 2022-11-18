![Panopticon](./.github/Panopticon.jpg)

# Pynopticon

Pynopticon is a video recording utility that saves the last `n` frames before an interesting event to disk. This is useful if you just want to record the frames leading up to an interesting event.

```python
import time
from pynopticon import Pynopticon

p = Pynopticon(record_frames=100)
p.start()
time.sleep(10)
p.save()
```

Optionally, you can upload the video to YouTube. This requires a `client_secrets.json` file, see instructions [here](https://developers.google.com/youtube/v3/guides/uploading_a_video#Requirements).

```python
import time
from pynopticon import Pynopticon, get_authenticated_service

youtube = get_authenticated_service(client_secrets_file="./client_secrets.json")
p = Pynopticon(record_frames=100, youtube=youtube)
p.start()
time.sleep(10)
p.save(upload=True, title="My Video", description="My Description")
```

There is also a server that exposes an http api, in case if you want to run Pynopticon on an external device.

```bash
# without upload:
python -m pynopticon

# with upload:
CLIENT_SECRETS_FILE="client_secrets.json" python -m pynopticon
```

- `/`: visit in browser for live streaming
- `POST /start`: same as `p.start()` (after stop, server auto starts pynopticon instance)
- `POST /save`: same as `p.save()`. Set `?upload=true` to upload to YouTube. Only works if `CLIENT_SECRETS_FILE` is set.
- `POST /stop`: same as `p.stop()`

https://en.wikipedia.org/wiki/Panopticon

## Installation

**Requires OpenCV!**

- from pip

```sh
pip install pynopticon
```

- from source

```sh
git clone https://github.com/rickwierenga/pynopticon
```

_Developed for the Sculpting Evolution Group at the MIT Media Lab_

