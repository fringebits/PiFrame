# PiFrame
Photo slide show project intended to run on RaspberryPi

### Setup

pip -m venv env
env/Scripts/activate
pip install -r requirements.txt

### Execution

env/Scripts/activate

To rebuild the photo catalog instead of loading an existing `catalog.json`, run:

```bash
python main.py --refresh
```

To override the slideshow wait time (in milliseconds) from the command line:

```bash
python main.py --wait-time 5000
```

