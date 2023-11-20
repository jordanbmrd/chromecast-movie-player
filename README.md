# Chromecast Movie Streamer

Chromecast Movie Streamer is a simple web application that allows you to cast local movie files to your Google Chromecast device. Just drag and drop a movie file onto the web page, and it will be streamed to your Chromecast. The application supports various video formats and also provides basic playback controls.

## Features

- Drag and drop movie files
- Stream various video formats to Chromecast
- Basic playback controls (play, pause)

## Installation

1. Clone the repository:

```git clone https://github.com/jordanbmrd/chromecast-movie-player.git```

2. Change the directory:

```cd chromecast-movie-streamer```

3. Install the required dependencies:

```pip install -r requirements.txt```

## Usage

1. Run the application:

```python pyChromecast.py```

2. Open your web browser and navigate to:

```http://localhost:8000```


3. Drag and drop a movie file onto the web page.

4. The movie will start streaming on your Chromecast device.

## Supported Video Formats

Chromecast Movie Streamer supports various video formats, including:

- MP4
- WebM
- Ogg
- MOV
- AVI
- MKV
- And more

The list of supported formats depends on the installed version of FFmpeg.

## Dependencies

- [Flask](https://flask.palletsprojects.com/)
- [PyChromecast](https://github.com/home-assistant-libs/pychromecast)
- [FFmpeg](https://ffmpeg.org/)

## Contributing

If you'd like to contribute to the project, please create a fork and submit a pull request with your changes.
