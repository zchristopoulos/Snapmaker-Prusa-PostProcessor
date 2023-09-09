import sys
import os
import re

def extract_print_time_from_filename(filename):
    # Assuming the format is something like "modelname_1h23m.gcode"
    match = re.search(r'(\d+h)?(\d+m)?.gcode', filename)
    if match:
        hours = int(match.group(1)[:-1]) if match.group(1) else 0
        minutes = int(match.group(2)[:-1]) if match.group(2) else 0
        return hours * 3600 + minutes * 60
    return 0

def extract_estimated_time(gcode_lines):
    # Regular expression to match the estimated printing time line
    pattern = r"; estimated printing time \(normal mode\) = (\d+d)? ?(\d+h)? ?(\d+m)? ?(\d+s)?"

    for line in gcode_lines:
        match = re.search(pattern, line)
        if match:
            days = int(match.group(1)[:-1]) if match.group(1) else 0
            hours = int(match.group(2)[:-1]) if match.group(2) else 0
            minutes = int(match.group(3)[:-1]) if match.group(3) else 0
            seconds = int(match.group(4)[:-1]) if match.group(4) else 0
            total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
            return total_seconds
    return 0

def extract_thumbnail_base64(gcode_lines):
    # Find the start and end of the thumbnail section
    thumbnail_start = None
    thumbnail_end = None
    for idx, line in enumerate(gcode_lines):
        if "thumbnail begin" in line:
            thumbnail_start = idx
        if "thumbnail end" in line:
            thumbnail_end = idx
            break

    # If both start and end are found, extract the base64 code
    if thumbnail_start is not None and thumbnail_end is not None:
        thumbnail_lines = gcode_lines[thumbnail_start + 1:thumbnail_end]
        # Remove the semicolon prefix and concatenate the lines
        base64_code = "".join([line.strip("; ").strip() for line in thumbnail_lines])
        return base64_code
    return None

def process_gcode(file_path):
    # Extract estimated time from the output name
    # output_name = str(os.getenv('SLIC3R_PP_OUTPUT_NAME', ''))
    # estimated_time = extract_print_time_from_filename(output_name)

    # Read the G-code file
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Extract the thumbnail base64 code
    thumbnail_base64 = extract_thumbnail_base64(lines)

    # Extract the estimated time
    estimated_time = extract_estimated_time(lines)

    # Extract necessary information
    total_lines = len(lines)
    nozzle_temp = os.environ.get('SLIC3R_TEMPERATURE', 'Unknown').split(',')[0]  # Adjusted the environment variable
    bed_temp = os.environ.get('SLIC3R_BED_TEMPERATURE', 'Unknown').split(',')[0]  # Get the first temperature value

    # Create the custom header
    header = "\n".join([
        ";Header Start",
        ";header_type: 3dp",
        # f";output_name: {output_name}",
        f";file_total_lines: {total_lines}",
        f";estimated_time(s): {estimated_time}",
        f";nozzle_temperature(°C): {nozzle_temp}",
        f";build_plate_temperature(°C): {bed_temp}",
        f";thumbnail: data:image/png;base64,{thumbnail_base64}",
        ";Header End",
        ""
    ])

    # Insert the custom header at the beginning of the G-code
    modified_gcode = header + "".join(lines)

    # Write the modified G-code back to the file
    with open(file_path, 'w') as f:
        f.write(modified_gcode)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No G-code file provided!")
        sys.exit(1)

    gcode_file_path = sys.argv[1]
    process_gcode(gcode_file_path)
