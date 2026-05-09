from playwright.sync_api import sync_playwright

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
url_base = "https://www.qconcursos.com"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(user_agent=user_agent)
    page = context.new_page()
    page.goto(url_base)

    print("Navegue e faça login no browser.")
    print("Quando terminar, pressione ENTER aqui para salvar a sessão...")
    input()

    context.storage_state(path="session.json")
    print("Sessão salva em session.json")

    browser.close()
