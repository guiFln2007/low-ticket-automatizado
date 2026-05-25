"""
Minerador de ofertas low ticket via Reclame Aqui
Edge headless + dev-browser --connect.

Uso:
  python minerador-reclameaqui.py                          # todos os gateways
  python minerador-reclameaqui.py monetizze,cakto          # gateways especificos
  python minerador-reclameaqui.py monetizze 4 15           # 4 paginas, 15 detalhes max
"""

import json
import os
import subprocess
import sys
import time
import re
from datetime import datetime, timedelta

GATEWAYS = {
    "monetizze": "monetizze",
    "kirvano": "kirvano-pagamentos",
    "cakto": "cakto-pay",
    "perfectpay": "perfectpay",
    "braip": "braip",
    "greenn": "greenn",
    "pepper": "pepper",
    "ticto": "ticto",
    "doppus": "doppus",
    "lastlink": "lastlink",
    "digital-manager-guru": "digital-manager-guru",
    "wiapy": "wiapy",
    "yampi": "yampi",
    "ggcheckout": "ggcheckout",
    "eduzz": "eduzz",
}

# Palavras que indicam produto low ticket na reclamacao
LOW_TICKET_SIGNALS = [
    "pack", "kit", "ebook", "e-book", "planilha", "molde", "receita", "projeto",
    "guia", "apostila", "template", "curso", "acervo", "combo", "app ", "aplicativo",
    "comunidade", "desafio", "checklist", "simulado", "quest", "artes", "conteudo digital",
]

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
EDGE_PORT = 9333
EDGE_DATA = os.path.join(os.environ.get("TEMP", "/tmp"), "edge-scraper")
DEVBROWSER_CMD = r"C:\Users\Pichau\AppData\Roaming\npm\dev-browser.cmd"
TEMP_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".tmp-devbrowser.js")


def start_edge():
    """Sobe Edge headless em background."""
    # Matar instancia antiga se existir
    subprocess.run(
        'powershell -Command "Get-Process msedge -ErrorAction SilentlyContinue | '
        "Where-Object {$_.CommandLine -like '*--headless*'} | Stop-Process -Force\"",
        shell=True, capture_output=True,
    )
    time.sleep(1)

    subprocess.Popen(
        [EDGE_PATH, "--headless", f"--remote-debugging-port={EDGE_PORT}",
         "--disable-gpu", "--no-first-run", "--disable-extensions",
         f"--user-data-dir={EDGE_DATA}", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    time.sleep(3)


def stop_edge():
    subprocess.run(
        'powershell -Command "Get-Process msedge -ErrorAction SilentlyContinue | '
        "Where-Object {$_.CommandLine -like '*--headless*'} | Stop-Process -Force\"",
        shell=True, capture_output=True,
    )


def run_devbrowser(script, timeout=15):
    """Executa script no dev-browser conectado ao Edge."""
    try:
        with open(TEMP_SCRIPT, "w", encoding="utf-8") as f:
            f.write(script)
        result = subprocess.run(
            f'"{DEVBROWSER_CMD}" --connect http://localhost:{EDGE_PORT} --timeout {timeout} < "{TEMP_SCRIPT}"',
            capture_output=True, text=True, encoding="utf-8",
            timeout=timeout + 10, shell=True,
        )
        output = result.stdout.strip()
        if result.stderr and result.stderr.strip():
            print(f"    [dev-browser stderr] {result.stderr.strip()[:120]}", flush=True)
        if output:
            for line in reversed(output.split("\n")):
                line = line.strip()
                if line.startswith("{") or line.startswith("["):
                    try:
                        return json.loads(line)
                    except json.JSONDecodeError as e:
                        print(f"    [JSON error] {e} — line: {line[:100]}", flush=True)
                        return None
        else:
            print(f"    [dev-browser] no output (rc={result.returncode})", flush=True)
        return None
    except subprocess.TimeoutExpired:
        print(f"    [dev-browser] timeout ({timeout}s)", flush=True)
        return None
    except Exception as e:
        print(f"    [dev-browser] error: {e}", flush=True)
        return None
    finally:
        try: os.remove(TEMP_SCRIPT)
        except: pass


def list_pages(slug, pages=10):
    """Lista reclamacoes de multiplas paginas."""
    all_links = []
    empty_streak = 0
    for pg in range(1, pages + 1):
        script = f"""
const page = await browser.getPage("main");
await page.goto("https://www.reclameaqui.com.br/empresa/{slug}/lista-reclamacoes/?pagina={pg}", {{ waitUntil: "domcontentloaded" }});
await new Promise(r => setTimeout(r, 6000));
const items = await page.evaluate((s) => {{
  const r = [];
  const seen = new Set();
  document.querySelectorAll('a').forEach(a => {{
    const h = a.href || '';
    const t = a.textContent.trim();
    if (h.includes('/' + s + '/') && h.length > 60
        && !h.includes('/lista-') && !h.includes('/empresa/')
        && !h.includes('/conteudos/') && !h.includes('/sobre/')
        && !h.endsWith('/' + s + '/')
        && t.length > 10 && !t.toLowerCase().includes('ler reclama')
        && !seen.has(h)) {{
      seen.add(h);
      r.push({{ title: t.substring(0, 200), url: h }});
    }}
  }});
  return r;
}}, "{slug}");
console.log(JSON.stringify(items));
"""
        result = run_devbrowser(script, timeout=30)
        if result and isinstance(result, list) and len(result) > 0:
            empty_streak = 0
            for l in result:
                if l["url"] not in {x["url"] for x in all_links}:
                    all_links.append(l)
        else:
            empty_streak += 1
            if empty_streak >= 4:
                break

    return all_links


def get_detail(url):
    """Extrai detalhes de 1 reclamacao."""
    script = f"""
const page = await browser.getPage("main");
await page.goto("{url}", {{ waitUntil: "domcontentloaded" }});
await new Promise(r => setTimeout(r, 4000));
const d = await page.evaluate(() => {{
  const body = document.body.innerText;
  const lines = body.split('\\n').map(l => l.trim()).filter(l => l.length > 0);

  let date = '', time = '';
  for (const l of lines) {{
    const m = l.match(/(\\d{{2}}\\/\\d{{2}}\\/\\d{{4}})\\s+[aà]s\\s+(\\d{{2}}:\\d{{2}})/);
    if (m) {{ date = m[1]; time = m[2]; break; }}
  }}

  let city = '';
  for (const l of lines) {{
    if (l.match(/^[A-ZÀ-Ú].*\\s-\\s[A-Z]{{2}}$/) && l.length < 40) {{ city = l; break; }}
  }}

  let content = '', cap = false;
  for (const l of lines) {{
    if (l.match(/^ID:\\s*\\d+/)) {{ cap = true; continue; }}
    if (cap) {{
      if (l.match(/^(Financeiras|Atendimento|Cobrança|Estorno|Propaganda|Produto|Entrega)/)) continue;
      if (l.includes('Reclamações Parecidas') || l.includes('Compartilhe')
          || l.includes('Resposta da empresa') || l.includes('RA Ads')) break;
      if (l.length > 3) content += l + ' ';
    }}
  }}
  if (content.trim().length < 20) {{
    let best = '';
    for (const l of lines) {{
      if (l.length > best.length && l.length > 40 && l.length < 3000
          && !l.includes('Entrar') && !l.includes('Reclame AQUI') && !l.includes('RA Ads')) best = l;
    }}
    content = best;
  }}

  const prices = [...new Set((body.match(/R\\$\\s*[\\d]+[.,]\\d{{2}}/g) || []))].slice(0, 5);
  return {{ date, time, city, content: content.trim().substring(0, 1200), prices }};
}});
console.log(JSON.stringify(d));
"""
    return run_devbrowser(script, timeout=20)


def classify_complaint(title, content):
    """Classifica a reclamacao: low_ticket, generico, ou irrelevante."""
    text = (title + " " + content).lower()

    # Ignorar reclamacoes genericas de plataforma
    ignore_patterns = [
        "saldo bloqueado", "trocar dado", "alterar email", "alterar senha",
        "saque", "comiss", "afiliado", "produtor", "nao consigo acessar minha conta",
        "suporte nao responde", "taxa abusiva", "problema no saque",
    ]
    for pattern in ignore_patterns:
        if pattern in text:
            return "generico", None

    # Detectar low ticket
    for signal in LOW_TICKET_SIGNALS:
        if signal in text:
            return "low_ticket", signal

    # Detectar por preco baixo
    prices = re.findall(r'R\$\s*([\d]+)[.,]\d{2}', text)
    for p in prices:
        val = int(p)
        if 5 <= val <= 50:
            return "low_ticket", f"R${val}"

    return "possivel", None


def extract_product_name(title, content):
    """Tenta extrair o nome do produto da reclamacao."""
    text = title + " " + content

    # Patterns comuns: "comprei o/a [PRODUTO]", "produto [NOME]", "curso [NOME]"
    patterns = [
        r'(?:comprei|adquiri|paguei)\s+(?:o|a|um|uma|pelo|pela)?\s*["\']?([^"\',.]{5,60})',
        r'(?:produto|curso|ebook|pack|kit|planilha|guia)\s+["\']?([^"\',.]{5,60})',
        r'["\u201c]([^"\u201d]{5,60})["\u201d]',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            if len(name) > 5 and not any(x in name.lower() for x in ["reclame", "reembolso", "estorno", "cancelamento"]):
                return name[:80]

    return None


def classify_niche(title, content):
    """Classifica o nicho baseado no conteudo."""
    text = (title + " " + content).lower()
    niches = {
        "Saude / Emagrec.": ["emagrecer", "receita fit", "dieta", "seca barriga", "detox", "glicemia", "metabolismo", "saude", "medic"],
        "Dinheiro / Renda": ["renda extra", "ganhar dinheiro", "investimento", "trader", "trade", "financeiro", "pix", "bitcoin", "cripto", "lotofacil"],
        "Artesanato / DIY": ["croche", "bordado", "costura", "molde", "feltro", "artesanato", "trico", "amigurumi"],
        "Culinaria": ["receita", "bolo", "confeitaria", "brigadeiro", "culinaria", "doce", "salgado", "cozinha"],
        "Beleza": ["unha", "cilio", "sobrancelha", "cabelo", "beleza", "estetica", "micropigmentacao"],
        "Educacao": ["questao", "simulado", "apostila", "concurso", "prova", "oab", "estudo", "curso"],
        "Construcao": ["projeto", "planta", "serralheiro", "marcenaria", "construcao", "obra"],
        "Design / Digital": ["arte", "template", "canva", "logo", "design", "post", "instagram", "social media"],
        "Esoterico": ["tarot", "taro", "signo", "astral", "oracao", "numerologia"],
    }
    for niche, keywords in niches.items():
        for kw in keywords:
            if kw in text:
                return niche
    return "Outro"


def run(gateways_to_scrape=None, pages=3, max_details=10):
    if gateways_to_scrape is None:
        gateways_to_scrape = list(GATEWAYS.keys())

    print(f"\n  MINERADOR RECLAME AQUI (Edge)")
    print(f"  ==============================")
    print(f"  {len(gateways_to_scrape)} gateways | {pages} pgs | max {max_details} detalhes/gw")
    print()

    start_edge()
    start_time = datetime.now()
    all_complaints = []

    for idx, gw in enumerate(gateways_to_scrape):
        if gw not in GATEWAYS:
            continue
        slug = GATEWAYS[gw]

        # Restart Edge between gateways to avoid stale tabs
        if idx > 0:
            stop_edge()
            time.sleep(2)
            start_edge()

        links = list_pages(slug, pages=pages)
        if not links:
            print(f"  [{gw.upper():.<25}] 0 reclamacoes")
            continue

        complaints = []
        for link in links[:max_details]:
            detail = get_detail(link["url"])
            if detail and detail.get("date"):
                classification, signal = classify_complaint(link["title"], detail.get("content", ""))
                product = extract_product_name(link["title"], detail.get("content", ""))
                niche = classify_niche(link["title"], detail.get("content", ""))

                entry = {
                    "gateway": gw,
                    "title": link["title"],
                    "url": link["url"],
                    "date": detail["date"],
                    "time": detail.get("time", ""),
                    "city": detail.get("city", ""),
                    "content": detail.get("content", ""),
                    "prices": detail.get("prices", []),
                    "classification": classification,
                    "signal": signal,
                    "product_name": product,
                    "niche": niche,
                }
                complaints.append(entry)

        all_complaints.extend(complaints)

        # Resumo
        lt = len([c for c in complaints if c["classification"] == "low_ticket"])
        total = len(complaints)
        print(f"  [{gw.upper():.<25}] {total} reclamacoes ({lt} low ticket)")

    elapsed = (datetime.now() - start_time).total_seconds()

    # Separar e rankear
    low_tickets = [c for c in all_complaints if c["classification"] == "low_ticket"]
    possiveis = [c for c in all_complaints if c["classification"] == "possivel"]

    # Salvar
    os.makedirs("./mineracao", exist_ok=True)
    output_file = f"./mineracao/{datetime.now().strftime('%Y-%m-%d')}-reclameaqui.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "date": datetime.now().isoformat(),
            "gateways": gateways_to_scrape,
            "elapsed_seconds": round(elapsed),
            "total": len(all_complaints),
            "low_ticket_count": len(low_tickets),
            "low_tickets": low_tickets,
            "possiveis": possiveis,
            "all_complaints": all_complaints,
        }, f, ensure_ascii=False, indent=2)

    stop_edge()

    # Resultado
    print(f"\n  ==============================")
    print(f"  {len(all_complaints)} reclamacoes em {round(elapsed)}s")
    print(f"  {len(low_tickets)} low ticket | {len(possiveis)} possiveis")
    print(f"  {output_file}")
    print(f"  ==============================")

    if low_tickets:
        print(f"\n  TOP LOW TICKET ENCONTRADOS:")
        for i, c in enumerate(low_tickets[:15], 1):
            price = f" | {', '.join(c['prices'])}" if c['prices'] else ""
            product = f" [{c['product_name']}]" if c['product_name'] else ""
            print(f"  {i:>2}. [{c['gateway']}] {c['date']} {c['title'][:50]}{product}{price}")
            print(f"      Nicho: {c['niche']} | Sinal: {c['signal']}")

    return output_file


if __name__ == "__main__":
    if len(sys.argv) > 1:
        gws = sys.argv[1].split(",")
        pages = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        max_d = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        run(gws, pages=pages, max_details=max_d)
    else:
        run(pages=10, max_details=15)
