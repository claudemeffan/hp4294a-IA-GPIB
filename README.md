# HP4294a Impedance Analyser Python GPIB Data Retrieval

NOTE: The HP4294a does have a File Transfer Protocol (FTP) interface available through the LAN port. 
This is the best and easiest option by far to get files, I recommend you try this option first. However, I couldn't get the LAN port to function on our system, so I wrote this program to pull data off. 

Python GUI program to export saved data files from the internal memory of the HP4294A over a GPIB Interface.

## File support

The HP4294A impedance analyser can save ASCII (.TXT), Binary (.DAT), TIF Images, and touchstone files. 

Note that Binary data formats are not human-readable, ASCII, and touchstone files are human readable.

## Usage Instructions

Connect instrument to computer via a GPIB interface. Theoretically, other interfaces should work, but have not been tested.

Run the main.py file through the terminal line. ("python main.py")

## Requirements

Python 3.X, py-visa.

Needs VISA driver for your operating system (Choose the correct driver for your GPIB interface, National Intruments, Agilent, etc)



If it works for your system, please let me know!
