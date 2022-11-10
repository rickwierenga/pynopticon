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

