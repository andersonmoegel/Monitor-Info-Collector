# Monitor Information Collection Script

This Python script collects detailed information about monitors connected to a Windows system, including manufacturer, model, serial number, and physical screen size. The collected data is stored in a text file located at `C:\Windows\Temp\Monitores_Dados.txt`.

## Features

- Retrieves detailed monitor information via the WMI interface.
- Processes data to remove accents and special characters.
- Calculates the physical screen size in inches based on system-provided dimensions.
- Saves the information in the `Monitores_Dados.txt` file.
- Automatically deletes the output file if no monitor information is found.

## Requirements

- Windows operating system.
- Python 3.x installed.
- `wmi` library installed.

Install the required library with:

```sh
pip install wmi
```

## Installation

1. Make sure Python is installed on your system.
2. Install the `wmi` library using the command above.
3. Save the script to a file named `monitor_info.py`.

## Usage

Run the script using the Windows terminal or command prompt:

```sh
python monitor_info.py
```

The script will generate the file `Monitores_Dados.txt` in `C:\Windows\Temp\` containing information about the connected monitors.

## Output File Structure

The file `Monitores_Dados.txt` will contain data in the following format:

```
Monitor1; Manufacturer: Dell; Model: P2419H; Size: 24; Serial Number: ABC12345;
Monitor2; Manufacturer: Lenovo; Model: L24q-30; Size: 23; Serial Number: XYZ67890;
```

If no monitor information is found, the file will be automatically deleted.

## Possible Errors and Solutions

- **Permission denied when creating the file:** Run the script as administrator.
- **No monitor detected:** Check if monitor drivers are up to date.
- **Error importing `wmi`:** Install the library using `pip install wmi`.

## Author

Developed by **Anderson** for monitor data collection in Windows environments.
