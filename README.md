Here are the contents for your `README.md` and `requirements.txt` files for your **Image Watermark App** built with Python, Tkinter, and Pillow:

---

### ✅ `README.md`

````markdown
# Image Watermark App

This is a Tkinter-based GUI application that allows users to apply and customize watermarks on images. It supports text watermarks with customizable font, color, size, and opacity. Users can also save the watermarked image or reset the watermark settings.

## Features

- Load and preview images
- Add text watermarks
- Customize font, size, and color of the watermark
- Adjust watermark opacity
- Position watermark interactively
- Save watermarked image
- Reset watermark settings

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/ArjunPathania/imagewatermarker
cd imagewatermarker
````

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

## Usage

Run the application using:

```bash
python imagewatermarker.py
```

Follow the GUI to:

1. Load an image.
2. Enter and customize your watermark.
3. Position the watermark using the canvas.
4. Save the final image.

## Dependencies

* `Pillow`: For image processing
* `Matplotlib`: Handling fonts
* `Tkinter`: For the graphical user interface (included with Python)

## File Structure

```
image-watermark-app/
│
├── imagewatermarker.py   # Main Python script
├── requirements.txt         # Python package requirements
└── README.md                # Project documentation
```

## License

This project is open-source and available under the [MIT License](LICENSE).

## Author

Arjun Pathania - [@ArjunPathania](https://github.com/ArjunPathania)

````
