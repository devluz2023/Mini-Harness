import json
import os


def unificar_arquivos(
 
    extensoes=(".py",".tf", ".sql", ".ipynb", ".sh", ".yml", ".md", ".json", ".toml", ".java", "yaml", ".xml", ".Dockerfile", ".json"),
    # extensoes=(".py", ".ts", ".css", ".html", ".js")
):
  diretorio="agent-harness"
  arquivo_saida= diretorio + ".txt"
  if not os.path.exists(diretorio):
    print(f"Erro: A pasta '{diretorio}' não foi encontrada.")
    return

  print(f"Buscando arquivos na pasta específica: {os.path.abspath(diretorio)}")

  contador = 0
  with open(arquivo_saida, "w", encoding="utf-8") as outfile:
    for root, dirs, files in os.walk(diretorio):
      # Ignora pastas ocultas (como .git ou .ipynb_checkpoints)
      dirs[:] = [d for d in dirs if not d.startswith(".")]

      for file in files:
        if file.endswith(extensoes):
          filepath = os.path.join(root, file)
          rel_path = os.path.relpath(filepath, diretorio)

          # Pula o próprio script se estiver na mesma árvore
          if file == "unificar.py":
            continue

          print(f"Lendo: {rel_path}")
          contador += 1

          # Cabeçalho para separar cada arquivo no txt final
          outfile.write("=" * 80 + "\n")
          outfile.write(f"ARQUIVO: {rel_path}\n")
          outfile.write("=" * 80 + "\n\n")

          if file.endswith(".ipynb"):
            try:
              with open(filepath, "r", encoding="utf-8") as f:
                nb = json.load(f)
                for cell in nb.get("cells", []):
                  cell_type = cell.get("cell_type")
                  source = "".join(cell.get("source", []))
                  if cell_type == "code":
                    outfile.write("# [Célula de Código]\n")
                    outfile.write(source + "\n\n")
                  elif cell_type == "markdown":
                    outfile.write("# [Célula Markdown]\n")
                    outfile.write(source + "\n\n")
            except Exception as e:
              outfile.write(f"# Erro ao ler o notebook: {e}\n")
          else:
            try:
              with open(filepath, "r", encoding="utf-8") as f:
                outfile.write(f.read())
            except Exception as e:
              outfile.write(f"# Erro ao ler o arquivo: {e}\n")

          outfile.write("\n\n")

  print(
      f"\nConcluído! {contador} arquivos da pasta '{diretorio}' foram unidos"
      f" em: {arquivo_saida}"
  )


if __name__ == "__main__":
  unificar_arquivos()



