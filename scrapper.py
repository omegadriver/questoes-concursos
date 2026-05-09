from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import json

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
url_base = "https://www.qconcursos.com/questoes-de-concursos/questoes"

q = input("Digite o termo de busca: ")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
folder_name = f"{q}_{timestamp}"
os.makedirs(folder_name, exist_ok=True)

metadata = {
    "sessao": {
        "termo_busca": q,
        "timestamp": timestamp,
        "url_base": url_base,
        "total_paginas": 0
    }
}

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(storage_state="session.json", user_agent=user_agent)
    page = context.new_page()

    def log_response(res):
        host = urlparse(res.url).hostname or ""
        if host == "www.qconcursos.com" and "cdn-cgi" not in res.url:
            print(f"[{res.status}] {res.url}")

    page.on("response", log_response)

    nu_pagina = 1
    while True:
        busca = f"?page={nu_pagina}&per_page=20&q={q}"
        page.goto(url_base + busca)

        if page.get_by_text("Nenhuma questão localizada com os filtros atuais. Escolha outro por favor.").count() > 0:
            print("fim")
            break

        pdf_path = f"{folder_name}/pagina_{nu_pagina}.pdf"
        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "1cm", "bottom": "1cm", "left": "1cm", "right": "1cm"}
        )
        print(f"Salvo: pagina_{nu_pagina}.pdf")

        nu_pagina += 1

    metadata["sessao"]["total_paginas"] = nu_pagina - 1

    with open(f"{folder_name}/metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"Metadata salvo: {folder_name}/metadata.json")

    browser.close()
