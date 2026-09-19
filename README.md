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

### Setup from a Raspberry PI
* Install desktop os, 64-bit
* Update / upgrade
    * sudo apt update
    * sudo apt upgrade
* Install nfs if needed
    * sudo apt install nfs-common -y
* Create a mount point
    * sudo mkdir -p /mnt/photos
* Mount to that end point
    * sudo mount -t nfs 192.168.1.7:/volume1/photo /mnt/photos
* Verify the connection
    * df -h 


* git clone https://github.com/fringebits/PiFrame.git
* python3 -m venv venv
* source venv/bin/activate
* pip install -r requirements.txt
