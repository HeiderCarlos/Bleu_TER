import sacrebleu
import sys
import os

def avaliar_traducoes(arquivo_hipotese, arquivo_referencia, arquivo_saida="resultados.txt"):
    # tenta abrir em UTF-8, se falhar, usa CP1252
    def ler_arquivo(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return [linha.strip() for linha in f.readlines()]
        except UnicodeDecodeError:
            with open(caminho, "r", encoding="cp1252") as f:
                return [linha.strip() for linha in f.readlines()]

    hipoteses = ler_arquivo(arquivo_hipotese)
    referencias = ler_arquivo(arquivo_referencia)

    if len(hipoteses) != len(referencias):
        raise ValueError("Os arquivos não têm o mesmo número de linhas.")

    # Calcula BLEU e TER
    bleu = sacrebleu.corpus_bleu(hipoteses, [referencias])
    ter = sacrebleu.corpus_ter(hipoteses, [referencias])

    # Salva resultados em um único arquivo
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.write("=== Avaliação de Tradução ===\n\n")
        f.write(f"BLEU score: {bleu.score:.2f}\n")
        f.write(str(bleu) + "\n\n")
        f.write(f"TER score: {ter.score:.2f}\n")
        f.write(str(ter) + "\n")

    print(f"Resultados salvos em {os.path.abspath(arquivo_saida)}")

# -------------------------------
# Execução pelo terminal:
# python scores.py maquina.txt humano.txt resultados.txt
# -------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python avaliar.py <arquivo_maquina> <arquivo_humano> [arquivo_saida]")
    else:
        arquivo_hipotese = sys.argv[1]
        arquivo_referencia = sys.argv[2]
        arquivo_saida = sys.argv[3] if len(sys.argv) > 3 else "resultados.txt"
        avaliar_traducoes(arquivo_hipotese, arquivo_referencia, arquivo_saida)