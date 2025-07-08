# 🖥️ DetectaMonitores - WMI + EDID (Python)

## Este script Python identifica os monitores conectados ao computador utilizando diversas fontes confiáveis do Windows, como **WMI**, **registro do sistema (EDID)** e heurísticas inteligentes. Ele é capaz de recuperar:

- Fabricante  
- Modelo  
- Tamanho (em polegadas)  
- Número de série  

## Os dados são exportados automaticamente para um arquivo `.txt` em:

```
C:\Windows\Temp\Monitores\_Dados.txt
```

Além disso, um log técnico é salvo para registrar falhas silenciosas:

```
C:\Windows\Temp\Monitor\_Log.txt
```

---

## 🚀 Funcionalidades

- Detecção de monitores via `WmiMonitorID` e `WmiMonitorBasicDisplayParams`  
- Leitura direta do EDID via registro do Windows  
- Fallback com heurísticas para extrair nome/tamanho de modelos incompletos  
- Filtragem de dispositivos irrelevantes (áudio, bluetooth, etc.)  
- Log detalhado com data e stack trace para diagnóstico  
- Funciona com mais de um monitor conectado  
- Permite compilação em `.exe` para execução remota ou distribuída  

---

## 📋 Estrutura do Arquivo Gerado

O arquivo `Monitores_Dados.txt` contém os dados em formato:

```
Fabricante;Modelo;Tamanho;Numero de Serie
```

Exemplo:

```
SAM;LF24T35;24;HX5X113520
LEN;ProdCode_16550;14;00000000
```

---

## ⚙️ Requisitos

- Python 3.8+  
- Sistema Operacional: Windows  
- Permissões de leitura no Registro e gravação em `C:\Windows\Temp`  

Instale as dependências com:

```bash
pip install wmi
```

---

## 🛠️ Compilação para .EXE

Se quiser gerar um `.exe` standalone:

### 1. Instale o PyInstaller

```bash
pip install pyinstaller
```

### 2. Compile:

```bash
pyinstaller --onefile --noconsole monitor_detect.py
```

O `.exe` será gerado na pasta `dist\`.

> ⚠️ O modo `--noconsole` evita abrir janela preta. Ideal para execução silenciosa.

---

## 🧪 Exemplos de uso

### Execução direta no Python:

```bash
python monitor_detect.py
```

### Execução do `.exe`:

```bash
C:\caminho\para\monitor_detect.exe
```

---

## 📄 Log de alterações

* **v2.0**:
  * Inclusão de fallback com leitura direta do EDID
  * Verificação apenas dos monitores atualmente conectados (ativos)
  * Registro de exceções detalhadas com stack trace
  * Reformulação completa do código para modularidade e robustez

* **v1.0**:
  * Detecção básica via WMI

---

## 🧠 Autor

**Anderson Moegel**  
🔗 [LinkedIn](https://www.linkedin.com/in/andersonmoegel/)  
💻 Desenvolvedor e profissional de Governança de TI

---

## ✅ Licença

Uso interno e educacional. Adaptável conforme política da empresa.
