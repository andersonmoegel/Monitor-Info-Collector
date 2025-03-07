import wmi
from screeninfo import get_monitors

def get_monitor_info():
    c = wmi.WMI(namespace='root\\wmi')
    monitors = c.WmiMonitorID()
    screen_monitors = get_monitors()
    monitor_info = []

    for i, monitor in enumerate(monitors):
        if i >= 3:
            break
        name = ''.join([chr(char) for char in monitor.UserFriendlyName if char != 0])
        serial_number = ''.join([chr(char) for char in monitor.SerialNumberID if char != 0])
        model = ''.join([chr(char) for char in monitor.ManufacturerName if char != 0])
        
        if i < len(screen_monitors):
            screen_monitor = screen_monitors[i]
            width_mm = screen_monitor.width_mm
            height_mm = screen_monitor.height_mm

            # Convertendo o tamanho de milimetros para polegadas
            width_inches = width_mm / 25.4
            height_inches = height_mm / 25.4
            diagonal_inches = (width_inches**2 + height_inches**2) ** 0.5

            monitor_info.append({
                'Nome': name,
                'Fabricante': model,
                'Tamanho': round(diagonal_inches),
                'Numero de Serie': serial_number
            })

    return monitor_info

def save_log_to_file(log):
    with open("C:\\Windows\\Temp\\Monitores_Dados.txt", "w") as file:
        file.write(log)

if __name__ == "__main__":
    info = get_monitor_info()
    log = ""
    for i, monitor in enumerate(info):
        log += f"Monitor {i+1}, Nome: {monitor['Nome']}, Fabricante: {monitor['Fabricante']}, Tamanho: {monitor['Tamanho']}, Numero de Serie: {monitor['Numero de Serie']}"
        if i < len(info) - 1:
            log += ", "
    print(log)
    save_log_to_file(log)
