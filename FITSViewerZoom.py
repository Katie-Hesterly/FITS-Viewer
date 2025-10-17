import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
from astropy.visualization import (ImageNormalize, LinearStretch, 
                                   LogStretch, AsinhStretch, ManualInterval)
import numpy as np
import argparse

def view_fits(filename, zoom_region=None, output=None, stretch='linear', 
              title=None, cmap='viridis', vmin=None, vmax=None, 
              plot_type='image-contours', contour_color='white', contour_levels=None):
    """
    View a FITS file with options to plot image alone, contours alone, or both.
    
    Parameters:
    -----------
    filename : str
        Path to the FITS file
    zoom_region : tuple, optional
        Region to zoom in on (x_min, x_max, y_min, y_max) in pixel coordinates
    output : str, optional
        Path to save the output image
    stretch : str, optional
        Type of stretch to apply ('linear', 'log', 'asinh')
    title : str, optional
        Title for the plot
    cmap : str, optional
        Colormap to use
    vmin : float, optional
        Minimum value for color scaling
    vmax : float, optional
        Maximum value for color scaling
    plot_type : str, optional
        'image', 'contours', or 'image-contours'
    contour_color : str, optional
        Color of the contours
    contour_levels : list, optional
        List of contour levels
    """
    # Open the FITS file
    hdul = fits.open(filename)
    
    # Determine which HDU contains the image data
    image_hdu = None
    for i, hdu in enumerate(hdul):
        if hdu.data is not None and len(hdu.data.shape) >= 2:
            image_hdu = i
            break
    
    if image_hdu is None:
        print("No image data found in the FITS file.")
        return
    
    # Get the data and header
    data = hdul[image_hdu].data
    header = hdul[image_hdu].header
    
    # If data has more than 2 dimensions, take the first 2D slice
    if len(data.shape) > 2:
        data = data[0, 0] if len(data.shape) == 4 else data[0]
    
    # Create WCS object for coordinate handling
    wcs = WCS(header, naxis=2)
    
    # If vmin or vmax are not provided, use data min/max
    if vmin is None:
        vmin = np.nanmin(data)
    if vmax is None:
        vmax = np.nanmax(data)
    
    # Set up the normalization based on the stretch type and color scale range
    interval = ManualInterval(vmin=vmin, vmax=vmax)
    
    if stretch == 'log':
        norm = ImageNormalize(data, interval=interval, stretch=LogStretch())
    elif stretch == 'asinh':
        norm = ImageNormalize(data, interval=interval, stretch=AsinhStretch())
    else:  # default to linear
        norm = ImageNormalize(data, interval=interval, stretch=LinearStretch())
    
    # Create the figure and axes
    plt.figure(figsize=(10, 8))
    ax = plt.subplot(projection=wcs)
    
    # Display the image if the plot type is 'image' or 'image-contours'
    if plot_type in ['image', 'image-contours']:
        im = ax.imshow(data, origin='lower', cmap=cmap, norm=norm)
        cbar = plt.colorbar(im, ax=ax, label='Flux')  # Add colorbar for image
    
    # Plot contours if the plot type is 'contours' or 'image-contours'
    if plot_type in ['contours', 'image-contours']:
        if contour_levels is None:
            contour_levels = np.linspace(vmin, vmax, 10)  # Default to 10 levels from vmin to vmax
        contour = ax.contour(data, levels=contour_levels, colors=contour_color, linewidths=1)
        ax.clabel(contour, inline=True, fontsize=8)  # Add labels to the contours
    
    # Set coordinate format to J2000 in hours, minutes, seconds
    ax.coords[0].set_format_unit('hour', decimal=False)
    ax.coords[1].set_format_unit('deg', decimal=False)
    
    # Set axis labels
    ax.coords[0].set_axislabel('Right Ascension (J2000)')
    ax.coords[1].set_axislabel('Declination (J2000)')
    
    # Hide grid lines
    ax.grid(False)
    
    # Set title
    if title:
        plt.title(title)
    else:
        plt.title(f"FITS Image: {filename}")
    
    # Apply zoom if specified
    if zoom_region:
        x_min, x_max, y_min, y_max = zoom_region
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
    
    # Save the figure if output is specified
    if output:
        plt.savefig(output, dpi=300, bbox_inches='tight')
        print(f"Image saved to {output}")
    
    # Show the plot
    plt.tight_layout()
    plt.show()
    
    # Close the FITS file
    hdul.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='View a FITS file with options for image, contours, or both.')
    parser.add_argument('filename', help='Path to the FITS file')
    parser.add_argument('--zoom', nargs=4, type=int, metavar=('XMIN', 'XMAX', 'YMIN', 'YMAX'),
                        help='Region to zoom in on (pixel coordinates)')
    parser.add_argument('--output', help='Path to save the output image')
    parser.add_argument('--stretch', choices=['linear', 'log', 'asinh'], default='linear',
                        help='Type of stretch to apply')
    parser.add_argument('--title', help='Title for the plot')
    parser.add_argument('--cmap', default='viridis', help='Colormap to use')
    parser.add_argument('--vmin', type=float, help='Minimum value for color scaling')
    parser.add_argument('--vmax', type=float, help='Maximum value for color scaling')
    parser.add_argument('--plot-type', choices=['image', 'contours', 'image-contours'], default='image-contours',
                        help='Plot type: "image" (image alone), "contours" (contours alone), or "image-contours" (both)')
    parser.add_argument('--contour-color', default='white', help='Color of the contours')
    parser.add_argument('--contour-levels', type=float, nargs='*', help='List of contour levels')
    
    args = parser.parse_args()
    
    view_fits(args.filename, args.zoom, args.output, args.stretch, 
              args.title, args.cmap, args.vmin, args.vmax, 
              args.plot_type, args.contour_color, args.contour_levels)




