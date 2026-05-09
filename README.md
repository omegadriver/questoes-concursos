# questoes-concursos

Scraper para baixar questões de concursos do [QConcursos](https://www.qconcursos.com) em PDF.

## Como funciona

O fluxo é dividido em duas etapas:

### 1. Salvar a sessão de login

Como o QConcursos exige login, primeiro é necessário autenticar manualmente uma vez:

    python create_session.py

Isso abre um browser Chromium visível. Faça o login normalmente no site e, quando terminar, pressione **ENTER** no terminal. A sessão é salva em `session.json`.

> `session.json` não está no repositório — guarde esse arquivo localmente.

### 2. Rodar o scraper

    python scrapper.py

Digite o termo de busca quando solicitado (ex: `brute force`, `direito constitucional`, etc.).

O script vai:
- Paginar automaticamente os resultados (`?page=1`, `?page=2`, ...)
- Salvar cada página como PDF em uma pasta nomeada `{termo}_{timestamp}/`
- Parar quando não houver mais resultados
- Gerar um `metadata.json` na pasta com o resumo da sessão

**Exemplo de saída para o termo "brute force":**

    brute force_20260509_194205/
      pagina_1.pdf
      pagina_2.pdf
      ...
      pagina_22.pdf
      metadata.json

## Instalação

    pip install -r requirements.txt
    playwright install chromium

## Dependências

- [playwright](https://playwright.dev/python/) — automação do browser
