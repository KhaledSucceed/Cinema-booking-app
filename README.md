# Cinema Booking App

This repository contains a simple seat booking application built with **Tkinter**. The app allows selecting seats from a cinema layout and keeps track of the total price.

## Requirements

- Python 3.8+
- [Pillow](https://python-pillow.org/) – for image loading in the GUI
- [opencv-python](https://pypi.org/project/opencv-python/) – optional, used by `hsv_color_picker.py`

Install dependencies via:

```bash
pip install Pillow opencv-python
```

## Running the Application

Run the main program using:

```bash
python3 main.py
```

When launched, the app opens maximized for easier viewing. The GUI shows the seating chart; click seats to book or reset them. Bookings can be saved to and loaded from `bookings.json`.

## Additional Scripts

- `radar_system.py` – an example of using abstract base classes to model a vehicle radar system.
- `hsv_color_picker.py` – prints HSV values from the seating chart image using OpenCV.

## License

This project is released under the MIT License.

