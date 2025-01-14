import ctypes
import wmi
from ctypes import wintypes
import unicodedata
import subprocess
import sys

# Constantes
MAX_DISPLAYS = 10
LOG_FILE_PATH = r"C:\Windows\Temp\Monitor_Log.txt"
ENUM_CURRENT_SETTINGS = -1  # Para obter a resolução ativa

# Função para verificar se o script está sendo executado com privilégios de administrador
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

# Função para reiniciar o script com privilégios de administrador, de forma silenciosa
def run_as_admin():
    if not is_admin():
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 0)
            sys.exit(0)
        except Exception as e:
            print(f"Erro ao solicitar privilégios de administrador: {e}")

# Função para tentar ativar o WMI caso ele esteja desativado
def ativar_wmi():
    try:
        resultado = subprocess.run(["sc", "query", "winmgmt"], capture_output=True, text=True)
        if "RUNNING" not in resultado.stdout:
            subprocess.run(["sc", "start", "winmgmt"], capture_output=True, text=True)
    except Exception as e:
        print(f"Erro ao ativar WMI: {e}")

# Definição da estrutura DEVMODE para pegar informações do monitor com ctypes
class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", wintypes.WCHAR * 32),
        ("dmSpecVersion", wintypes.WORD),
        ("dmDriverVersion", wintypes.WORD),
        ("dmSize", wintypes.WORD),
        ("dmDriverExtra", wintypes.WORD),
        ("dmFields", wintypes.DWORD),
        ("dmPositionX", ctypes.c_long),
        ("dmPositionY", ctypes.c_long),
        ("dmDisplayOrientation", wintypes.DWORD),
        ("dmDisplayFixedOutput", wintypes.DWORD),
        ("dmColor", wintypes.WORD),
        ("dmDuplex", wintypes.WORD),
        ("dmYResolution", wintypes.WORD),
        ("dmTTOption", wintypes.WORD),
        ("dmCollate", wintypes.WORD),
        ("dmFormName", wintypes.WCHAR * 32),
        ("dmLogPixels", wintypes.WORD),
        ("dmBitsPerPel", wintypes.DWORD),
        ("dmPelsWidth", wintypes.DWORD),
        ("dmPelsHeight", wintypes.DWORD),
        ("dmDisplayFlags", wintypes.DWORD),
        ("dmDisplayFrequency", wintypes.DWORD),
        ("dmICMMethod", wintypes.DWORD),
        ("dmICMIntent", wintypes.DWORD),
        ("dmMediaType", wintypes.DWORD),
        ("dmDitherType", wintypes.DWORD),
        ("dmReserved1", wintypes.DWORD),
        ("dmReserved2", wintypes.DWORD),
        ("dmPanningWidth", wintypes.DWORD),
        ("dmPanningHeight", wintypes.DWORD),
    ]

# Função para remover caracteres especiais, como acentos e cedilhas
def remover_caracteres_especiais(texto):
    texto = unicodedata.normalize("NFKD", texto)
    return "".join([c for c in texto if unicodedata.category(c) != "Mn" and c != 'Ç' and c != 'ç'])

# Função auxiliar para extrair strings de arrays de inteiros
def extrair_string(array):
    return ''.join(chr(char) for char in array if char != 0).strip()

# Função para obter as informações dos monitores com WMI
def obter_monitores_wmi():
    try:
        c = wmi.WMI(namespace="root\\WMI")
        monitores = c.WmiMonitorID()
        monitor_data = []

        for monitor in monitores:
            nome = extrair_string(monitor.UserFriendlyName)
            modelo = extrair_string(monitor.ProductCodeID)
            fabricante = extrair_string(monitor.ManufacturerName)

            monitor_data.append({
                "nome": nome or "Desconhecido",
                "modelo": modelo or "Desconhecido",
                "fabricante": fabricante or "Desconhecido"
            })

        return monitor_data
    except Exception as e:
        return [{"erro": str(e)}]

# Função para obter a resolução de todos os monitores
def obter_resolucoes():
    try:
        user32 = ctypes.windll.user32
        user32.EnumDisplaySettingsW.restype = wintypes.BOOL
        user32.EnumDisplaySettingsW.argtypes = [wintypes.LPWSTR, wintypes.DWORD, ctypes.POINTER(DEVMODE)]

        resolucoes = []

        for i in range(MAX_DISPLAYS):
            devmode = DEVMODE()
            if user32.EnumDisplaySettingsW(f"\\\\.\\DISPLAY{i+1}", ENUM_CURRENT_SETTINGS, ctypes.byref(devmode)):
                resolucoes.append({
                    "nome": f"\\\\.\\DISPLAY{i+1}",
                    "resolucao": f"{devmode.dmPelsWidth}x{devmode.dmPelsHeight}",
                    "largura": devmode.dmPelsWidth,
                    "altura": devmode.dmPelsHeight
                })
            else:
                resolucoes.append({
                    "nome": f"\\\\.\\DISPLAY{i+1}",
                    "resolucao": "Indisponível"
                })

        return resolucoes
    except Exception as e:
        return [{"erro": str(e)}]

# Função para exibir as informações dos monitores, incluindo resolução e nome/modelo
def contar_monitores():
    try:
        ativar_wmi()
        monitores_wmi = obter_monitores_wmi()
        resolucoes = obter_resolucoes()

        informacoes_monitores = []

        for i, monitor in enumerate(monitores_wmi):
            nome = remover_caracteres_especiais(monitor.get("nome", "Desconhecido"))
            modelo = remover_caracteres_especiais(monitor.get("modelo", "Desconhecido"))
            fabricante = remover_caracteres_especiais(monitor.get("fabricante", "Desconhecido"))
            resolucao = resolucoes[i]["resolucao"]

            informacoes_monitores.append(
                f"Monitor {i + 1}: Nome: {nome}, Modelo: {modelo}, Resolucao: {resolucao}"
            )

        salvar_log(informacoes_monitores)
    except Exception as e:
        salvar_log([f"Erro: {str(e)}"])

# Função para salvar as informações em um arquivo de log, com tudo em uma linha
def salvar_log(informacoes):
    try:
        with open(LOG_FILE_PATH, "w", encoding="utf-8") as arquivo:
            for info in informacoes:
                arquivo.write(f"{info}\n")
    except Exception as e:
        print(f"Erro ao salvar o log: {e}")

# Função principal
def main():
    run_as_admin()
    contar_monitores()

if __name__ == "__main__":
    main()
