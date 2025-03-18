import wmi
import math
import unicodedata
import os

def remove_accents_and_special_chars(text):
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return ''.join(e for e in text if e.isalnum() or e.isspace())

def clean_string(text):
    return text.strip()

def calculate_screen_size_mm(width_mm, height_mm):
    diagonal_mm = math.sqrt(width_mm**2 + height_mm**2)
    size_in_inches = diagonal_mm / 25.4
    return round(size_in_inches) if size_in_inches % 1 != 0 else int(size_in_inches)

try:
    c = wmi.WMI(namespace="root\\wmi")

    def get_friendly_monitor_info():
        monitors = c.WmiMonitorID()
        if monitors is None:
            return []
        monitor_info_list = []
        for monitor in monitors:
            manufacturer = ''.join(chr(c) for c in monitor.ManufacturerName if c != 0)
            model = ''.join(chr(c) for c in monitor.UserFriendlyName if c != 0)
            serial_number = ''.join(chr(c) for c in monitor.SerialNumberID if c != 0)
            manufacturer = clean_string(remove_accents_and_special_chars(manufacturer))
            model = clean_string(remove_accents_and_special_chars(model))
            serial_number = clean_string(remove_accents_and_special_chars(serial_number))
            monitor_info_list.append({
                "Fabricante": manufacturer,
                "Modelo": model,
                "Numero de Serie": serial_number
            })
        return monitor_info_list

    def get_monitor_physical_size():
        monitors = c.WmiMonitorBasicDisplayParams()
        if monitors is None:
            return []
        monitor_sizes = []
        for monitor in monitors:
            if hasattr(monitor, 'MaxHorizontalImageSize') and hasattr(monitor, 'MaxVerticalImageSize'):
                width_mm = monitor.MaxHorizontalImageSize * 10
                height_mm = monitor.MaxVerticalImageSize * 10
                size_in_inches = calculate_screen_size_mm(width_mm, height_mm)
                monitor_sizes.append(size_in_inches)
        return monitor_sizes

    monitor_info_list = get_friendly_monitor_info()
    monitor_sizes = get_monitor_physical_size()

    if monitor_info_list and monitor_sizes:
        with open(r"C:\Windows\Temp\Monitores_Dados.txt", "w", encoding="utf-8") as file:
            for i, info in enumerate(monitor_info_list, start=1):
                size_in_inches = monitor_sizes[i-1] if i-1 < len(monitor_sizes) else "Desconhecido"
                file.write(f"Monitor{i}; Fabricante: {info['Fabricante']}; Modelo: {info['Modelo']}; Tamanho: {size_in_inches}; N de serie: {info['Numero de Serie']};\n")
    else:
        if os.path.exists(r"C:\Windows\Temp\Monitores_Dados.txt"):
            os.remove(r"C:\Windows\Temp\Monitores_Dados.txt")

except Exception:
    pass
