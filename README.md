# Documentação do Script de Coleta de Informações de Monitores

Este script coleta informações sobre os monitores conectados ao sistema, incluindo nome, fabricante, tamanho da tela e número de série. Ele utiliza duas bibliotecas: **WMI** (Windows Management Instrumentation) e **screeninfo**. As informações coletadas são registradas em um arquivo de log no diretório `C:\Windows\Temp`.

## Funcionalidades

1. **Coleta de Informações de Monitores**:
   - Obtém o nome do monitor, fabricante, número de série e o tamanho da tela (em polegadas).
   - Usa **WMI** para acessar informações sobre os monitores conectados e **screeninfo** para obter as dimensões físicas dos monitores.
   - Calcula o tamanho da tela em polegadas com base nas dimensões físicas em milímetros.

2. **Registro de Dados em Arquivo de Log**:
   - Cria um arquivo de log (`Monitores_Dados.txt`) contendo as informações dos monitores, incluindo o nome, fabricante, tamanho e número de série.

3. **Exibição de Dados no Console**:
   - Imprime as informações dos monitores diretamente no console.

## Estrutura do Código

### 1. Importação de Bibliotecas

```python
import wmi
from screeninfo import get_monitors
```

Essas bibliotecas são usadas para acessar informações do sistema:
- **`wmi`**: Para interagir com o WMI (Windows Management Instrumentation) e obter informações sobre o hardware.
- **`screeninfo`**: Para obter as dimensões físicas dos monitores conectados ao sistema.

### 2. Função `get_monitor_info()`

```python
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
```

A função `get_monitor_info()` coleta as informações sobre os monitores conectados ao sistema:
1. Usa o **WMI** para obter as informações do monitor, como nome do modelo, número de série e fabricante.
2. Usa a **screeninfo** para obter as dimensões físicas do monitor.
3. Converte as dimensões de milímetros para polegadas para calcular o tamanho diagonal da tela.
4. Retorna uma lista de dicionários com as informações de cada monitor, contendo:
   - **Nome**: Nome do monitor.
   - **Fabricante**: Fabricante do monitor.
   - **Tamanho**: Tamanho diagonal da tela em polegadas.
   - **Número de Série**: Número de série do monitor.

### 3. Função `save_log_to_file()`

```python
def save_log_to_file(log):
    with open("C:\\Windows\\Temp\\Monitores_Dados.txt", "w") as file:
        file.write(log)
```

A função `save_log_to_file()` salva o log de informações dos monitores em um arquivo de texto:
- O arquivo é criado no diretório `C:\Windows\Temp` com o nome `Monitores_Dados.txt`.
- As informações dos monitores são escritas no arquivo, com cada monitor listado em uma linha.

### 4. Função Principal `main()`

```python
if __name__ == "__main__":
    info = get_monitor_info()
    log = ""
    for i, monitor in enumerate(info):
        log += f"Monitor {i+1}, Nome: {monitor['Nome']}, Fabricante: {monitor['Fabricante']}, Tamanho: {monitor['Tamanho']}, Numero de Serie: {monitor['Numero de Serie']}"
        if i < len(info) - 1:
            log += ", "
    print(log)
    save_log_to_file(log)
```

- **Chama a função `get_monitor_info()`** para obter as informações dos monitores.
- **Cria um log** com as informações de cada monitor, incluindo nome, fabricante, tamanho e número de série.
- **Imprime as informações no console**.
- **Chama a função `save_log_to_file()`** para salvar o log no arquivo `Monitores_Dados.txt`.

### 5. Execução do Script

```python
if __name__ == "__main__":
    main()
```

Esta linha garante que o código dentro da função `main()` será executado quando o script for chamado diretamente.

## Possíveis Melhorias

- **Detecção de Mais Monitores**: O script atualmente limita a coleta a 3 monitores. Isso pode ser modificado para coletar informações de todos os monitores conectados, se necessário.
- **Melhorias na Formatação do Log**: O log gerado pode ser formatado para facilitar a leitura, por exemplo, incluindo quebras de linha ou separadores mais visíveis.
- **Tratamento de Erros**: O código pode ser aprimorado para incluir melhor tratamento de erros, caso a obtenção das informações de algum monitor falhe.

## Uso

1. **Executar o script**: Para rodar o script, basta executá-lo em um ambiente Python. Ele coletará as informações dos monitores conectados e exibirá essas informações no console.
2. **Verificar o arquivo de log**: O arquivo de log `Monitores_Dados.txt` será criado em `C:\Windows\Temp\` com as informações detalhadas dos monitores.

## Conclusão

Este script fornece uma maneira eficaz de coletar e registrar informações sobre os monitores conectados ao sistema, incluindo nome, fabricante, número de série e tamanho da tela. Ele pode ser útil para administradores de sistemas ou em contextos onde a coleta de informações sobre o hardware de exibição é necessária.
