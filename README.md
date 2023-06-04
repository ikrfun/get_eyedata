# Get-eyedata

this library is an application that allows you to track objects in a video file and save the tracking data to a CSV file.

## Installation
---
you can use pip to install get-eyedata.
```bash
pip install get-eyedata
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

```python
from get_eyedata import valo

# valo_df is pandas dataframe
valo_df = valo.make_dataset('{video-file-path}')
```
---
## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
