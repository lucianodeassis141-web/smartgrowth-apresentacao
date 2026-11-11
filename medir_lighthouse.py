# -*- coding: utf-8 -*-
"""Mede as prévias publicadas com o Google Lighthouse (celular, 4G simulado) e grava medidas.json.
Uso:  python medir_lighthouse.py [medições por marca, padrão 5]
Depois:  python gerar.py   (os cartões de número dos casos usam medidas.json)
Precisa de Node (npx) e do Chrome instalado."""
import json, os, subprocess, sys, statistics, tempfile, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = "https://lucianodeassis141-web.github.io/smartgrowth-apresentacao/previa/"
MARCAS = ["nike", "smartfit", "boticario", "natura", "havaianas"]
N = int(sys.argv[1]) if len(sys.argv) > 1 else 5

def medir(marca, pasta):
    notas, lcps = [], []
    for r in range(N):
        saida = os.path.join(pasta, f"{marca}-{r}.json")
        subprocess.run(["npx", "--yes", "lighthouse", BASE + marca + "/", "--only-categories=performance",
                        "--output=json", f"--output-path={saida}", "--chrome-flags=--headless=new", "--quiet"],
                       shell=(os.name == "nt"), check=False)
        if os.path.exists(saida):
            d = json.load(open(saida, encoding="utf-8"))
            notas.append(round(d["categories"]["performance"]["score"] * 100))
            lcps.append(d["audits"]["largest-contentful-paint"]["numericValue"] / 1000)
    return notas, lcps

def gravar(resultados):
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    med = {m: {"nota": int(statistics.median(n)), "lcp": round(statistics.median(l), 1), "medicoes": len(n), "data": hoje, "notas": n}
           for m, (n, l) in resultados.items() if n}
    json.dump(med, open(os.path.join(AQUI, "medidas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return med

if __name__ == "__main__":
    pasta = tempfile.mkdtemp(prefix="lh-")
    print(gravar({m: medir(m, pasta) for m in MARCAS}))
