# Time Tracker

## Description

This is a simple time tracker that allows you to track your time spent on different tasks.

## Pre-requisites

- Python 3.6 or higher
- xdotool: `sudo apt install xdotool`

## Installation

1. Clone the repository
2. Install the requirements: `pip install -r requirements.txt`
3. Run the application setup: `python3 time_tracker.py setup`

## Usage

Start the service

```bash
python3 time_tracker.py start
```

with a 10 seconds interval and in the background

```bash
python3 time_tracker.py start -i 10 &
```

Stop the service running in the background

```bash
python3 time_tracker.py stop
```