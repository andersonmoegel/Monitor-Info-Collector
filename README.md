# Documentação do Script de Coleta de Informações de Monitores

Este script em Python coleta informações detalhadas sobre os monitores conectados a um sistema Windows, incluindo fabricante, modelo, número de série e tamanho físico da tela. Os dados coletados são armazenados em um arquivo de texto localizado em `C:\Windows\Temp\Monitores_Dados.txt`.

## Funcionalidades
- Obtém informações detalhadas dos monitores através da interface WMI.
- Processa os dados para remover acentos e caracteres especiais.
- Calcula o tamanho físico da tela em polegadas com base nas dimensões fornecidas pelo sistema.
- Salva as informações no arquivo `Monitores_Dados.txt`.
- Caso nenhuma informação seja encontrada, remove o arquivo de saída, se existir.

## Requisitos
- Sistema operacional Windows.
- Python 3.x instalado.
- Biblioteca `wmi` instalada (`pip install wmi`).

## Instalação
1. Certifique-se de ter o Python instalado no sistema.
2. Instale a biblioteca `wmi` executando:
   ```sh
   pip install wmi
   ```
3. Salve o script em um arquivo `monitor_info.py`.

## Uso
1. Execute o script no terminal ou prompt de comando do Windows:
   ```sh
   python monitor_info.py
   ```
2. O arquivo `Monitores_Dados.txt` será gerado em `C:\Windows\Temp\` contendo as informações dos monitores conectados.

## Estrutura do Arquivo de Saída
O arquivo `Monitores_Dados.txt` conterá informações no seguinte formato:
```
Monitor1; Fabricante: Dell; Modelo: P2419H; Tamanho: 24; N de serie: ABC12345;
Monitor2; Fabricante: Lenovo; Modelo: L24q-30; Tamanho: 23; N de serie: XYZ67890;
```
Se nenhuma informação for encontrada, o arquivo será excluído automaticamente.

## Possíveis Erros e Soluções
- **Permissão negada ao criar o arquivo:** Execute o script como administrador.
- **Nenhum monitor detectado:** Verifique se os drivers dos monitores estão atualizados.
- **Erro ao importar `wmi`:** Instale a biblioteca com `pip install wmi`.

## Autor
Desenvolvido por Anderson para coleta de dados de monitores em ambientes Windows.

