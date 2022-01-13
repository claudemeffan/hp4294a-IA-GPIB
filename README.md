# HP4294a Impedance Analyser Python GPIB Data Retrieval

Python GUI program to export saved data files from the internal memory of the HP4294A over a GPIB Interface.

## File support

HP4294A can save ASCII (.TXT), Binary (.DAT), PNG, and touchstone files. The program currently only decodes files saved as .TXT (ASCII) to a csv file.

All other files are not decoded, and are dumped into a raw txt file as bytes. If it's requested I will add decoding support for other files.

## Requirements

Python 3.X, py-visa.

A binary installation is also available. 
