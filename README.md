# Get-eyedata

this softwere is an application that allows you to track objects in a video file and save the tracking data to a CSV file.

## Installation

---

1. Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/ikrfun/get_eyedata.git
```

2. Install the required packages using the following command:

```bash
cd get_eyedata
pip install pipenv
pipenv sync
pipenv shell
```

---

## Usage

To use Aeye-Tracker, run the following command in your terminal

```bash
python main.py -f <video-file-path> -o <output-file-path>
```

`<video-file-path>`: The path to the video file that you want to track.

`<output-file-path>`: The path to the output file where you want to save the tracking data. Default value is `output.csv`.

## Examples

Track an object in a video file and save the tracking data to a CSV file:

```bash
python main.py -f videos/sample.mp4 -o output
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
