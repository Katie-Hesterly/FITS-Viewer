# 🌌 FITS-Viewer

A lightweight interactive viewer for astronomical **FITS** images, built in Python.  
It provides fast zooming, panning, and brightness control for quick data inspection — ideal for astronomers, students, or anyone working with FITS files.

---

## 🧭 Overview

`FITSViewerZoom.py` allows you to open and explore FITS files interactively using a simple Matplotlib interface.  
You can zoom with the scroll wheel, pan by dragging, and adjust the image display dynamically — no external GUI toolkit required.

**Key features**
- 🔍 Mouse-wheel zoom and click-drag pan  
- 🌗 Adjustable contrast and brightness scaling  
- 💾 Supports standard 2D FITS images (e.g. Stokes I maps)  
- ⚙️ Pure-Python implementation using Astropy and Matplotlib  
- 🪶 Runs as a standalone script — no dependencies beyond common scientific packages

---

## ⚙️ Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/<your-username>/FITSViewerZoom.git
cd FITSViewerZoom
pip install -r requirements.txt

or install manually:
pip install astropy matplotlib numpy


## 🚀 Usage

Run the viewer directly from the command line:

python3 FITSViewerZoom.py <path_to_fits_file> [options]


For example:

python3 FITSViewerZoom.py example_image.fits --stretch log --cmap inferno


## 🧰 Options

FITSViewerZoom.py supports several optional arguments to customize how images are displayed:

filename — (Required) Path to the FITS file to open.

--ext <index> — Specify which FITS extension (HDU) to open (default: 0).

--cmap <name> — Choose a Matplotlib colourmap (default: gray).
Common choices: viridis, plasma, inferno, coolwarm.

--stretch <mode> — Set intensity scaling. Options:

linear (default)

log for logarithmic display

sqrt for square-root scaling

--contrast <factor> — Multiply image contrast by a scaling factor (default: 1.0).

--vmin <value> / --vmax <value> — Manually define lower and upper display limits.

--invert — Invert the colour scale (useful for displaying bright sources on a dark background).

--title <text> — Add a custom plot window title.

Example with several options:

python3 FITSViewerZoom.py data/my_image.fits \
  --ext 0 \
  --stretch log \
  --cmap plasma \
  --contrast 1.2 \
  --title "Galaxy Field"

## 🖱️ Interactive Controls

Once the viewer is open:

Control	Action
🖱️ Scroll	Zoom in or out around the cursor
🖱️ Click + Drag	Pan the image
⌨️ r	Reset zoom and scaling
⌨️ q	Quit the viewer window

##  Author 
Developed by Katie Hesterly
Part of open-source tools for astronomical data visualization

## Contributing

