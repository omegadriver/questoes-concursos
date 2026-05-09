import fitz
import re
import json

path = r"C:\Sistemas\dev\auto\v2\linux_20260509_204700\pagina_69.pdf"
doc = fitz.open(path)
texto = "\n".join(page.get_text(sort=True) for page in doc)
doc.close()

texto = texto.strip(" [www.qconcursos.com\n](https://www.qconcursos.com\n)")

block = re.search(r'Respostas\b([\s\S]*)', texto)
if block:
    matches = re.findall(r'(\d+):\s+([ABCDEX])', block.group(1))
    gabarito = {int(q): r for q, r in matches}

_INICIO_ENUNCIADO = re.compile(
    r'^(Sobre|Assinale|Analise|Julgue|Com |No |Na |Nos |Nas |O |A |Os |As |Em |'
    r'Para |Acerca|Qual|Quais|NÃO|Dentre|Considerando|Tendo|São|Leia|Observe|'
    r'Marque|Indique|Avalie|De acordo|Segundo|Um |Uma |Ao |À |Dos |Das |Como |'
    r'Considere|Entre |Dado|Sabendo|Acerca)',
    re.IGNORECASE
)

def _norm(s):
    return ' '.join(s.split())

def _e_continuacao_prova(s):
    return len(s) <= 150 and not _INICIO_ENUNCIADO.match(s) and not s.endswith('.')

def extrair_metadado(pattern, bloco):
    m = re.search(pattern, bloco)
    return _norm(m.group(1)) if m else None

def extrair_prova(bloco):
    m = re.search(r'Provas?:\s*(.+?)(?=\n\n|\Z)', bloco, re.DOTALL)
    if not m:
        return None, 0

    partes = [_norm(m.group(1))]
    pos = m.end()

    while True:
        seg = re.match(r'\n\n(.+?)(?=\n\n|\Z)', bloco[pos:], re.DOTALL)
        if not seg:
            break
        candidato = _norm(seg.group(1))
        if _e_continuacao_prova(candidato):
            partes.append(candidato)
            pos += seg.end()
        else:
            break

    return ' '.join(partes), pos


blocos = re.split(r'\n(?=\s*\d+\s+Q\d+)', texto)

questoes = []
for bloco in blocos:
    if not bloco.strip():
        continue

    cabecalho = re.match(r'\s*(\d+)\s+(Q\d+)\s+(.+)', bloco)
    if not cabecalho:
        continue

    ano   = extrair_metadado(r'Ano:\s*(\d+)', bloco)
    banca = extrair_metadado(r'Banca:\s*(.+?)(?=\s{2,}|\n)', bloco)
    orgao = extrair_metadado(r'Órgão:\s*(.+?)(?=\s{2,}|\n)', bloco)
    prova, pos_enunciado = extrair_prova(bloco)

    corpo = bloco[pos_enunciado:]
    antes_alts = re.split(r'\n\s*[A-E]\s{2,}', corpo)[0]
    paragrafos = re.split(r'\n\n+', antes_alts.strip())
    enunciado = ' '.join(
        p.strip() for p in paragrafos
        if not re.search(r'Ano:|Banca:|Órgão:|Provas?:', p)
        and not re.match(r'\s*\d+\s+Q\d+', p)
    ).strip()

    alts = dict(re.findall(r'^\s*([A-E])\s{2,}(.+?)$', bloco, re.MULTILINE))

    questoes.append({
        'numero':       int(cabecalho.group(1)),
        'qcode':        cabecalho.group(2),
        'categoria':    cabecalho.group(3).strip(),
        'ano':          ano,
        'banca':        banca,
        'orgao':        orgao,
        'prova':        prova,
        'enunciado':    enunciado,
        'alternativas': alts,
    })

print(json.dumps(questoes, ensure_ascii=False, indent=2))
