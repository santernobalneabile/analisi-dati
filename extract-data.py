# Author: Ugo B.
# 2024-06-01
# github.com/pastacolsugo

from pypdf import PdfReader
import os
import re
import sys

regex = {
    "campione" : r'^(\d{11}) Codice LIMS [0-9A-Z]{9}$',
    "lims" : r'^\d{11} Codice LIMS ([0-9A-Z]{9})$',
    "data_analisi" : r'^(\d{2}/\d{2}/\d{4})$',
    "data_prelievo" : r'^Data prelievo: ?(\d{2}/\d{2}/\d{4}).*$',
    "punto_prelievo" : r'^Punto di prelievo: (.*)$',
    "comune_prelievo" : r'^Comune di prelievo: (.*)$',
    "nota_campione" : r'^Nota Campione: (.*)$',
    "coliformi" : r'^(.*) UFC/100 mL \*\n.*Coliformi Totali$',
    "escherichia_coli" : r'^(.*) UFC/100 mL.*\n.*Escherichia coli$',
    "enterococchi" : r'^(.*) UFC/100 mL \*\n.*Enterococchi$',
    "salmonella" : r'^(.*) /1000 mL .*\n.*Salmonella spp$',
    "data_inizio_prove" : r'^.*Data inizio prove:(\d{2}/\d{2}/\d{4})$',
    "data_fine_prove" : r'^Data fine prove: (\d{2}/\d{2}/\d{4})$'
}
compiled_patterns = {name: re.compile(pattern, re.MULTILINE) for name, pattern in regex.items()}
output_file = ""

def extract_data(p):
    matches = {}
    for name, pattern in compiled_patterns.items():
        match = pattern.search(p)
        if match:
            matches[name] = match.group(1)
        else:
            matches[name] = 'Not found'

    for _, v in matches.items():
        if v != 'Not found':
            return matches
    return {}

def find_pdfs(root_dir):
    fps = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(dirpath, filename)
                fps.append(file_path)
    return fps


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("scrape.py : Estrai i dati dai PDF delle analisi")
        print("uso: crea un venv, installa pypdf, esegui")
        print("python3 scrape.py /path/to/directory/root output_file_name")
        print("dove: ")
        print("\t/path/to/directory/root è la cartella con le cartelle")
        print("\toutput_file_name è il nome del file che conterrà il risultato, in formato .tsv")
        print("\n")
        exit(0)
    tree_root = sys.argv[1]
    output_file = sys.argv[2]
    files = find_pdfs(tree_root)
  
    if files == []:
      print(f'nessun pdf trovato in {tree_root}')
      print('hai inserito il percorso corretto?')
      exit(0)
    
    with open(output_file, 'w') as of:
        of.write("\t".join(regex.keys()) + '\n')
        for f in files:
            reader = PdfReader(f)
            for i in range(len(reader.pages)):
                page = reader.pages[i].extract_text()
                matches = extract_data(page)
                print(matches)
                of.write("\t".join(matches.values()) + '\n')
                # print(page.extract_text())
                # print('\n\n')
