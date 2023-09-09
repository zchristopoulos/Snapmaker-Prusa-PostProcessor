# Snapmaker-Prusa-PostProcessor

This python script will add relevant GCode headers to PrusaSlicer's outputted GCode files. Absolutely still a work in progress, but it is a start. Only currently tested to work with Snapmaker 2.0 A350T with a Dual Extrusion module.

Loosly using Snapmaker's Cura plugin as inspiration/guidance. https://github.com/Snapmaker/SnapmakerCuraPlugin/blob/main/gcode_writer/SnapmakerGCodeWriter.py

## How To Use
1. Download/save the python file `snapmaker_gcode_processor.py`.
2. In your print settings, go to "Output options" and list the script under Post-processing scripts.

## Notes
- It is recommended to set the outputted G-code thumbnail to `600x600` and a PNG in your printer settings. The post processor will grab that and format it into a Snapmaker thumbnail header.

## ToDo's
- [ ] Figure out why the percentage is not going to 100% at the end of a print. (thinking it might be too many lines in `file_total_lines`)
- [ ] Add extruder info headers.
- [ ] Add retraction info headers.
- [ ] Add bounding box/work range headers. (min/max x, y, z)
- [ ] Add printer name header.
- [ ] Support for new Artisan/J1 headers.
