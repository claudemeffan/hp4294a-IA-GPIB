# HP4294a Impedance Analyser Python GPIB Data Retrieval

NOTE: The HP4294a does have a File Transfer Protocol (FTP) interface available through the LAN port. This is the best and easiest option by far to get files, I reccomend you try this option first. However, I couldn't get the LAN port to function on our system, so I wrote this program to pull data off. 

Python GUI program to export saved data files from the internal memory of the HP4294A over a GPIB Interface.

## File support

The HP4294A impedance analyser can save ASCII (.TXT), Binary (.DAT), PNG, and touchstone files. This python interface currently only decodes files saved as .TXT (ASCII) to a csv file.

All other files save by the HP4294a IA are not decoded, and are dumped into a raw txt file as bytes. If it's requested I will add decoding support for other files.

## Requirements

Python 3.X, py-visa.

Needs OS VISA driver (National Instruments for example)
