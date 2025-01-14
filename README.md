# Script de Detecção de Monitores README

## Visão Geral
Este script detecta e registra informações sobre os monitores conectados em sistemas Windows, incluindo sua resolução, nome, modelo e fabricante. Ele utiliza a interface Windows Management Instrumentation (WMI) e a biblioteca `ctypes` para interagir com o sistema operacional. A saída é salva em um arquivo de log localizado em `C:\Windows\Temp\Monitor_Log.txt`.

---

## Funcionalidades
- Detecta até **10 monitores conectados**.
- Obtém informações do monitor, incluindo:
  - **Nome Amigável**: Nome do monitor exibido ao usuário.
  - **Modelo**: Código do produto do monitor.
  - **Fabricante**: Nome do fabricante do monitor.
- Recupera a **resolução de exibição atual** de cada monitor.
- **Elevação automática de privilégios** para executar com direitos administrativos.
- Salva todos os resultados em um **arquivo de log** para revisão posterior.

---

## Pré-requisitos
- **Python 3.x**
- **Módulos necessários**:
  - `wmi`: Instale com `pip install WMI`

---

## Uso
### Compilando para um Executável
Para criar um executável independente:
```bash
python -m PyInstaller --onefile -w Monitores.py
```
A flag `-w` suprime a exibição da janela do terminal ao executar o executável.

---

## Localização dos Arquivos
- **Arquivo de Log**: `C:\Windows\Temp\Monitor_Log.txt`

---

## Estrutura do Código
### 1. Constantes
```python
MAX_DISPLAYS = 10
LOG_FILE_PATH = r"C:\Windows\Temp\Monitor_Log.txt"
ENUM_CURRENT_SETTINGS = -1
```
Define o número máximo de monitores a serem detectados e o caminho para o arquivo de log.

### 2. Funções

#### `is_admin()`
Verifica se o script está sendo executado com privilégios administrativos.

#### `run_as_admin()`
Eleva os privilégios, se necessário, usando uma solicitação silenciosa para evitar interrupções ao usuário.

#### `ativar_wmi()`
Garante que o serviço Windows Management Instrumentation (WMI) esteja em execução.

#### `DEVMODE`
Uma estrutura que contém configurações de exibição, usada para obter resoluções de tela.

#### `remover_caracteres_especiais(texto)`
Remove caracteres especiais, como acentos e cedilhas, de strings.

#### `extrair_string(array)`
Converte um array de inteiros representando caracteres em uma string legível.

#### `obter_monitores_wmi()`
Recupera o nome, modelo e fabricante dos monitores usando a interface WMI.

#### `obter_resolucoes()`
Obtém a resolução atual de cada monitor conectado.

#### `contar_monitores()`
Combina as informações dos monitores e as resoluções em uma lista de strings formatadas.

#### `salvar_log(informacoes)`
Salva as informações formatadas dos monitores no arquivo de log especificado.

### 3. Ponto de Entrada Principal
```python
def main():
    run_as_admin()
    contar_monitores()

if __name__ == "__main__":
    main()
```
Executa a lógica do script, garantindo que ele funcione com os privilégios necessários.

---

## Tratamento de Erros
- Verifica o status do serviço WMI e tenta iniciá-lo se não estiver em execução.
- Registra quaisquer exceções encontradas durante a execução.

---

## Exemplo de Saída
```
Monitor 1: Nome: Dell U2719D, Modelo: ABC123, Resolucao: 2560x1440
Monitor 2: Nome: Desconhecido, Modelo: XYZ456, Resolucao: 1920x1080
```

---

## Limitações Conhecidas
- Pode não detectar corretamente todos os monitores em versões antigas do Windows ou em configurações de hardware não suportadas.
- Depende de chamadas específicas de `wmi` e `ctypes`, limitando a compatibilidade com outras plataformas.

---

## Considerações de Segurança
- Requer privilégios administrativos para funcionalidade completa, incluindo a detecção de resoluções.
- Escreve logs em um diretório do sistema; certifique-se de que as permissões apropriadas estejam configuradas para evitar acesso não autorizado.

---

## Licença
Este software é disponibilizado sob a licença MIT. Isso permite o uso livre, modificação e distribuição, desde que os devidos créditos sejam mantidos. Para mais detalhes, consulte o texto completo da licença MIT abaixo:

---

## Contato
Para problemas ou melhorias, entre em contato comigo.

