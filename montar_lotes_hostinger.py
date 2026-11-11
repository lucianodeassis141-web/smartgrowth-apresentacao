# -*- coding: utf-8 -*-
"""Monta os lotes de envio do site para a Hostinger (smartgrowthai.com.br).
Cada lote é um script para o navegador (browser_run_code_unsafe com filename), rodado com a aba do
File Browser da Hostinger na frente. O index.html vai sozinho no último lote."""
import os, base64, json

AQUI = os.path.dirname(os.path.abspath(__file__))
DEST = r"C:\Users\Luciano\Documents\cerebro\.playwright-mcp"
FORA_PASTAS = {".git", "__pycache__"}
FORA_ARQS = {".gitignore", ".nojekyll", "gerar.py", "medir_lighthouse.py", "medidas.json", "LEIA-ME.md", "montar_lotes_hostinger.py"}

MODELO = r"""async (page) => {
  const files = __ARQS__;
  const out = await page.evaluate(async (files) => {
    const code = location.pathname.split('/')[1]; const jwt = localStorage.getItem('jwt');
    const res = []; let k = 0;
    async function um() { while (k < files.length) { const [p, b] = files[k++];
      const bin = atob(b); const u = new Uint8Array(bin.length); for (let j = 0; j < bin.length; j++) u[j] = bin.charCodeAt(j);
      const r = await fetch('/' + code + '/api/resources/public_html/' + p.split('/').map(encodeURIComponent).join('/') + '?override=true', { method: 'POST', headers: { 'X-Auth': jwt }, body: u });
      res.push(p + ':' + r.status); } }
    await Promise.all(Array.from({ length: 8 }, um));
    return res;
  }, files);
  const ruins = out.filter(x => !/:2\d\d$/.test(x));
  return '__NOME__: ' + out.length + ' enviados, falhas: ' + JSON.stringify(ruins);
}"""

def main():
    arqs = []
    for raiz, dirs, fs in os.walk(AQUI):
        dirs[:] = [d for d in dirs if d not in FORA_PASTAS]
        for f in fs:
            if f in FORA_ARQS:
                continue
            arqs.append(os.path.relpath(os.path.join(raiz, f), AQUI).replace(os.sep, "/"))
    arqs.sort(key=lambda p: (p == "index.html", p))
    tam = sum(os.path.getsize(os.path.join(AQUI, p)) for p in arqs)
    print(len(arqs), "arquivos", round(tam / 1e6, 2), "MB")
    lotes, atual, soma = [], [], 0
    for p in arqs:
        b = base64.b64encode(open(os.path.join(AQUI, p), "rb").read()).decode()
        if atual and (p == "index.html" or soma + len(b) > 3_500_000):
            lotes.append(atual); atual, soma = [], 0
        atual.append([p, b]); soma += len(b)
    lotes.append(atual)
    for i, l in enumerate(lotes, 1):
        js = MODELO.replace("__ARQS__", json.dumps(l)).replace("__NOME__", f"lote {i}")
        open(os.path.join(DEST, f"sg-lote{i}.js"), "w", encoding="utf-8").write(js)
        print(f"sg-lote{i}.js", len(l), "arquivos")

if __name__ == "__main__":
    main()
