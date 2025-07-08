import wmi
import math
import unicodedata
import re
import winreg
import traceback
from datetime import datetime

def remove_accents_and_special_chars(text):
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return ''.join(e for e in text if e.isalnum() or e.isspace())

def clean_string(text):
    return text.strip() if text else ""

def calculate_screen_size_mm(width_mm, height_mm):
    diagonal_mm = math.sqrt(width_mm**2 + height_mm**2)
    size_in_inches = diagonal_mm / 25.4
    return round(size_in_inches) if size_in_inches % 1 != 0 else int(size_in_inches)

def is_valid_name(name):
    if not name:
        return False
    n = name.lower()
    if n.startswith('@') or '%' in n:
        return False
    blacklist = [
        "touchpad", "intel", "standby", "function keys", "pm device", "miniport",
        "power and battery", "thermal solution", "driver da tecnologia",
        "wan miniport", "smart standby", "network", "audio", "bluetooth",
        "headset", "keyboard", "mouse", "volume", "controller", "device",
        "print", "firmware", "usb", "pci", "software", "system", "processor",
        "root hub", "storage", "platform", "enumerator", "driver", "radio",
        "audio", "capture", "hid", "bateria", "camera", "input", "compativel",
        "serial", "timer", "crowdstrike"
    ]
    if any(bad in n for bad in blacklist):
        return False
    whitelist = [
        "monitor", "display", "lcd", "led", "asus", "dell", "lenovo", "samsung",
        "acer", "lg", "viewsonic", "benq", "hp", "philips", "sony", "lf", "p",
        "ultrasharp", "xg", "predator", "odyssey", "curved"
    ]
    return any(good in n for good in whitelist)

def extract_size_from_name(name):
    try:
        sizes = re.findall(r'\b([1-9][0-9]?)\b', name)
        for s in sizes:
            size_int = int(s)
            if 15 <= size_int <= 100:
                return size_int
    except Exception as e:
        write_log("Erro ao extrair tamanho do nome: " + str(e), exc_info=True)
    return "Desconhecido"

def get_friendly_names_from_registry():
    friendly_names = {}
    try:
        base_path = r"SYSTEM\CurrentControlSet\Enum\DISPLAY"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base_path) as base_key:
            for i in range(winreg.QueryInfoKey(base_key)[0]):
                monitor_id = winreg.EnumKey(base_key, i)
                with winreg.OpenKey(base_key, monitor_id) as monitor_key:
                    for j in range(winreg.QueryInfoKey(monitor_key)[0]):
                        instance_id = winreg.EnumKey(monitor_key, j)
                        with winreg.OpenKey(monitor_key, instance_id) as instance_key:
                            try:
                                with winreg.OpenKey(instance_key, "Device Parameters") as dev_param_key:
                                    friendly_name, _ = winreg.QueryValueEx(dev_param_key, "FriendlyName")
                                    friendly_names[instance_id] = friendly_name.strip()
                            except FileNotFoundError:
                                continue
    except Exception as e:
        write_log("Erro ao ler friendly names do registro: " + str(e), exc_info=True)
    return friendly_names

def parse_edid(edid_bytes):
    if not edid_bytes or len(edid_bytes) < 128:
        return None

    try:
        manufacturer_id = edid_bytes[8:10]
        manufacturer_code = ""
        if len(manufacturer_id) == 2:
            val = (manufacturer_id[0] << 8) + manufacturer_id[1]
            for i in range(3):
                char_code = ((val >> (5 * (2 - i))) & 0x1F) + 64
                manufacturer_code += chr(char_code)

        product_code = edid_bytes[10] + (edid_bytes[11] << 8)
        serial_bytes = edid_bytes[12:16]
        serial_number = "".join(f"{b:02X}" for b in serial_bytes)
        horizontal_size_cm = edid_bytes[21]
        vertical_size_cm = edid_bytes[22]
        if horizontal_size_cm == 0 or vertical_size_cm == 0:
            size_inches = "Desconhecido"
        else:
            diagonal_cm = (horizontal_size_cm ** 2 + vertical_size_cm ** 2) ** 0.5
            size_inches = round(diagonal_cm / 2.54)

        return {
            "Fabricante": manufacturer_code,
            "Modelo": f"ProdCode_{product_code}",
            "Tamanho": size_inches,
            "Numero de Serie": serial_number
        }
    except Exception as e:
        write_log("Erro ao parsear EDID: " + str(e), exc_info=True)
        return None

def get_active_instance_ids_from_wmi():
    active_ids = set()
    try:
        c = wmi.WMI(namespace="root\\wmi")
        monitors = c.WmiMonitorID()
        if monitors:
            for mon in monitors:
                instance_name = getattr(mon, "InstanceName", None)
                if instance_name:
                    instance_id = instance_name.split("\\")[-1]
                    active_ids.add(instance_id)
    except Exception as e:
        write_log("Erro ao obter InstanceIDs ativos do WMI: " + str(e), exc_info=True)
    return active_ids

def get_edid_from_registry(active_instance_ids):
    monitors_edid = []
    base_path = r"SYSTEM\CurrentControlSet\Enum\DISPLAY"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base_path) as base_key:
            for i in range(winreg.QueryInfoKey(base_key)[0]):
                monitor_id = winreg.EnumKey(base_key, i)
                with winreg.OpenKey(base_key, monitor_id) as monitor_key:
                    for j in range(winreg.QueryInfoKey(monitor_key)[0]):
                        instance_id = winreg.EnumKey(monitor_key, j)
                        if instance_id not in active_instance_ids:
                            continue
                        with winreg.OpenKey(monitor_key, instance_id) as instance_key:
                            try:
                                with winreg.OpenKey(instance_key, "Device Parameters") as dev_param_key:
                                    edid_raw, _ = winreg.QueryValueEx(dev_param_key, "EDID")
                                    edid_info = parse_edid(edid_raw)
                                    if edid_info:
                                        edid_info["InstanceID"] = instance_id
                                        monitors_edid.append(edid_info)
                            except FileNotFoundError:
                                continue
    except Exception as e:
        write_log("Erro ao ler EDID do registro: " + str(e), exc_info=True)

    return monitors_edid

def write_log(message, exc_info=False):
    log_path = r"C:\Windows\Temp\Monitor_Log.txt"
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")
            if exc_info:
                f.write(traceback.format_exc() + "\n")
    except Exception:
        pass

def get_monitors_data():
    c = wmi.WMI(namespace="root\\wmi")
    friendly_names_registry = get_friendly_names_from_registry()
    active_instance_ids = get_active_instance_ids_from_wmi()
    edid_monitors = get_edid_from_registry(active_instance_ids)
    monitor_data = []
    try:
        monitors = c.WmiMonitorID()
        params = c.WmiMonitorBasicDisplayParams()
    except Exception as e:
        write_log("Erro ao acessar WMI para monitores: " + str(e), exc_info=True)
        monitors = None
        params = None

    if monitors and params and len(monitors) == len(params):
        for i in range(len(monitors)):
            mon = monitors[i]
            par = params[i]
            try:
                manufacturer = ''.join(chr(c) for c in mon.ManufacturerName if c != 0)
                model = ''.join(chr(c) for c in mon.UserFriendlyName if c != 0)
                serial = ''.join(chr(c) for c in mon.SerialNumberID if c != 0)
                manufacturer = clean_string(remove_accents_and_special_chars(manufacturer))
                model = clean_string(remove_accents_and_special_chars(model))
                serial = clean_string(remove_accents_and_special_chars(serial))
            except Exception as e:
                write_log("Erro ao ler dados do monitor WMI: " + str(e), exc_info=True)
                manufacturer = model = serial = ""

            if not is_valid_name(model):
                instance_name = getattr(mon, "InstanceName", None)
                if instance_name:
                    instance_id = instance_name.split("\\")[-1]
                    if instance_id in friendly_names_registry:
                        model = friendly_names_registry[instance_id]

            size = "Desconhecido"
            try:
                if hasattr(par, 'MaxHorizontalImageSize') and hasattr(par, 'MaxVerticalImageSize'):
                    width_mm = par.MaxHorizontalImageSize * 10
                    height_mm = par.MaxVerticalImageSize * 10
                    size = calculate_screen_size_mm(width_mm, height_mm)
            except Exception as e:
                write_log("Erro ao calcular tamanho do monitor: " + str(e), exc_info=True)

            if size == "Desconhecido":
                size = extract_size_from_name(model)

            if model and manufacturer and is_valid_name(model):
                monitor_data.append({
                    "InstanceID": getattr(mon, "InstanceName", "").split("\\")[-1] if hasattr(mon, "InstanceName") else "",
                    "Fabricante": manufacturer,
                    "Modelo": model,
                    "Tamanho": size,
                    "Numero de Serie": serial if serial else "Desconhecido"
                })

    if edid_monitors:
        for edid_mon in edid_monitors:
            if any(m.get("InstanceID", "") == edid_mon.get("InstanceID", "") for m in monitor_data):
                continue
            monitor_data.append({
                "Fabricante": edid_mon.get("Fabricante", "Desconhecido"),
                "Modelo": edid_mon.get("Modelo", "Desconhecido"),
                "Tamanho": edid_mon.get("Tamanho", "Desconhecido"),
                "Numero de Serie": edid_mon.get("Numero de Serie", "Desconhecido")
            })

    if not monitor_data:
        write_log("Sem monitor conectado no momento.")
        monitor_data.append({
            "Fabricante": "Sem monitor conectado no momento",
            "Modelo": "",
            "Tamanho": "",
            "Numero de Serie": ""
        })
    else:
        valid = any(is_valid_name(m.get("Modelo", "")) and m.get("Fabricante", "") for m in monitor_data)
        if not valid:
            write_log("Sem informacoes suficientes para identificar os monitores.")
            monitor_data = [{
                "Fabricante": "Sem informacoes suficientes.",
                "Modelo": "",
                "Tamanho": "",
                "Numero de Serie": ""
            }]

    return monitor_data

def save_monitor_data_to_file(monitor_data, filepath):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            for m in monitor_data:
                line = f"{m['Fabricante']};{m['Modelo']};{m['Tamanho']};{m['Numero de Serie']}\n"
                f.write(line)
        return True
    except Exception as e:
        write_log("Erro ao salvar arquivo de dados do monitor: " + str(e), exc_info=True)
        return False

def main():
    path = r"C:\Windows\Temp\Monitores_Dados.txt"
    data = get_monitors_data()
    save_monitor_data_to_file(data, path)

if __name__ == "__main__":
    main()
