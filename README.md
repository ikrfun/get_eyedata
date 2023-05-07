# Get-eyedata

this softwere is an application that allows you to track objects in a video file and save the tracking data to a CSV file.

## Installation

---

1. Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/ikrfun/get_eyedata.git
cd get_eyedata
```

2. Install the required packages using the following command:

```bash
pip install -r requirements.txt
```

---

## Usage

### Preparing Recorded Data

you need video file which is recorded by OBS with original setting

show details ->　https://github.com/ikrfun/get_eyedata/wiki/usage-en

get OBS -> https://obsproject.com/ja/download

---

### When creating a dataset of actual facial images and their corresponding gaze coordinates 

To use mekeing eye dataset, run the following command in your terminal

```bash
python make_eyedataset.py -f <video-file-path> 
```

`<video-file-path>`: The path to the video file 
then you can find dataset on 'data' dir

---

###  When creating a dataset consisting of Valorant screen data and corresponding gaze information

```bash
python make_valodataset.py -f <video-file-path> 
```

`<video-file-path>`: The path to the video file 
then you can find dataset on 'data' dir

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
