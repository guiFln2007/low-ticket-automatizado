---
name: automatico
description: Low Ticket Automatizado — software completo pra rodar low ticket no automatico. Mineracao de ofertas escaladas, modelagem de funil, criativos, cadastro em gateway e otimizacao de campanhas. Rodar quando o usuario digitar /automatico.
allowed-tools: [WebFetch, WebSearch, Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion, Skill, mcp__claude_ai_Meta_Ads__*, mcp__claude_ai_Higgsfield__*, mcp__claude_ai_Utmify__*]
---

# Low Ticket Automatizado

Sistema completo pra rodar operacao de low ticket no automatico. Funciona como um software interativo dentro do Claude Code.

## Ao iniciar

Mostrar este menu exatamente assim:

```
============================================
   LOW TICKET AUTOMATIZADO v1.0
   by @adsborba
============================================

  [1] Setup & Diagnostico
  [2] Minerar ofertas escaladas
  [3] Analisar & Definir produto
  [4] Gerar entregavel
  [5] Modelar funil
  [6] Gerar criativos
  [7] Cadastrar produto
  [8] Meta Ads
  [9] Configuracoes

Digite o numero:
```

Aguardar a resposta do usuario e executar o fluxo correspondente.

Quando qualquer fluxo terminar, perguntar se quer voltar ao menu ou sair.

---

## [1] SETUP & DIAGNOSTICO

### Objetivo
Verificar e instalar tudo que a skill precisa pra funcionar. O aluno deve rodar isso PRIMEIRO antes de usar qualquer outro modulo.

### Fluxo

Ao selecionar [1]:

```
SETUP & DIAGNOSTICO
=====================
Verificando dependencias...
```

Verificar cada item automaticamente e mostrar status:

```
DEPENDENCIAS
==============

FERRAMENTAS:
  Edge (scraper Reclame Aqui)       [?] verificando...
  dev-browser (automacao browser)   [?] verificando...
  Whisper (transcrever videos)      [?] verificando...
  video-downloader (baixar videos)  [?] verificando...

MCPs (conectores):
  Higgsfield                        [?] verificando...
  Utmify                            [?] verificando...

APIs:
  Apify (scraper Biblioteca)        [?] verificando...

CONTAS:
  Wiapy (gateway)                   [?] verificando...
  Meta Business (anuncios)          [?] verificando...
  RatoAds (mineracao premium)       [?] verificando...
```

**Como verificar cada item:**

1. **Edge:** verificar se `msedge.exe` existe em `C:\Program Files (x86)\Microsoft\Edge\Application\` ou rodar `where msedge`
2. **dev-browser:** rodar `dev-browser --help` — se retornar help, ta instalado
3. **Whisper:** rodar `which whisper` ou `whisper --help` no terminal
4. **video-downloader:** verificar se a skill existe em `~/.claude/skills/video-downloader/`
5. **MCP Higgsfield:** tentar chamar `balance` — se retornar dados, ta conectado
6. **MCP Utmify:** tentar chamar `get_dashboards` — se retornar dados, ta conectado
7. **Apify:** verificar se tem `apify_token` no config-automatico.json (nao null)
8. **Wiapy:** perguntar pro usuario se tem conta na Wiapy
9. **Meta Business:** perguntar pro usuario se tem conta de anuncios no Meta
10. **RatoAds:** verificar se tem credenciais validas no config-automatico.json

**Resultado:**

```
DIAGNOSTICO COMPLETO
=====================

FERRAMENTAS:
  Whisper                           [OK] instalado
  dev-browser                       [OK] instalado
  video-downloader                  [OK] instalado

MCPs:
  Higgsfield                        [OK] conectado
  Utmify                            [OK] conectado

APIs:
  Apify                             [FALTA] token nao configurado

CONTAS:
  Wiapy                             [OK] tem conta
  Meta Business                     [OK] tem conta
  RatoAds                           [FALTA] credenciais nao configuradas

============================================

RESUMO: 7/9 OK | 2 faltando

ITENS FALTANDO:
  1. Apify — precisa do token pra scrapar Biblioteca de Anuncios
  2. RatoAds — precisa de email/senha pra mineracao premium

[I] Instalar/configurar itens faltando
[0] Voltar ao menu
```

Se [I], perguntar qual item e rodar o fluxo de instalacao:

```
Qual quer configurar?

  [1] Whisper
  [2] dev-browser
  [3] video-downloader
  [4] MCP Higgsfield
  [5] MCP Utmify
  [6] Apify
  [7] Wiapy (login)
  [8] RatoAds (credenciais)

Digite o numero:
```

#### Instalacao de cada item:

**[1] Whisper:**
Rodar: `pip install openai-whisper`
Testar: `whisper --help`
Se der erro de ffmpeg: instruir instalacao manual.

**[2] dev-browser:**
```
O dev-browser conecta no seu Chrome pra automatizar sites.

Abra o Chrome com debug mode:
  Windows: chrome.exe --remote-debugging-port=9222
  Mac: open -a "Google Chrome" --args --remote-debugging-port=9222

Confirme que abriu (s/n):
> [resposta]
```
Testar conexao via dev-browser skill.

**[3] video-downloader:**
Rodar: `pip install yt-dlp`
Testar: `yt-dlp --version`

**[4] MCP Higgsfield:**
Testar: chamar `balance`.
Se falhar, instruir como adicionar o MCP no settings do Claude Code.

**[5] MCP Utmify:**
Testar: chamar `get_dashboards`.
Se falhar, instruir configuracao.

**[6] Apify:**
```
O Apify scrapa a Biblioteca de Anuncios do Meta automaticamente.
Plano free tem creditos suficientes pra comecar.

Ja tem conta no Apify? (s/n)

Se sim:
  Cole seu API token (apify.com > Settings > Integrations):
  > [token]

Salvando em config-automatico.json...
Testando conexao...
```

**[7] Wiapy:**
Verificar se ta logado via dev-browser em wiapy.com. Se nao, guiar login.

**[8] RatoAds:**
```
  [1] Ativar trial do curso (3/3/3 por 30 dias)
  [2] Ja tenho conta — configurar login
```
Mesmo fluxo do [2] Minerar > [C] RatoAds.

---

## [2] MINERAR OFERTAS ESCALADAS

### Objetivo
Encontrar ofertas de infoprodutos que estao vendendo muito (escaladas) no mercado BR, usando reclamacoes como proxy de volume.

### Fluxo

Ao selecionar [2], mostrar:

```
MINERACAO DE OFERTAS
====================

Metodo:
  [A] Reclame Aqui (gratis — scrapa gateways BR)
  [B] Biblioteca de Anuncios (Meta — busca visual)
  [C] RatoAds (premium — requer conta)

Qual metodo?
```

---

### Metodo A — Reclame Aqui

#### Logica
Gateways de pagamento recebem reclamacoes de compradores. Quanto mais reclamacao sobre um produto especifico, mais gente comprou = oferta escalada. O script `minerador-reclameaqui.py` scrapa o Reclame Aqui usando Edge headless + dev-browser.

#### Tecnologia
- **Edge headless** sobe em background (porta 9333) — passa Cloudflare sem ser bloqueado
- **dev-browser --connect** navega nas paginas do Reclame Aqui
- Script: `minerador-reclameaqui.py` no diretorio de trabalho
- Resultados salvos em `./mineracao/[data]-reclameaqui.json`

**Pre-requisitos:** Edge instalado + dev-browser instalado (`npm install -g dev-browser`)

#### Gateways (8 foco low ticket)

| Gateway | Slug |
|---------|------|
| Wiapy | `wiapy` |
| GGCheckout | `ggcheckout` |
| Yampi | `yampi` |
| Cakto | `cakto-pay` |
| Kirvano | `kirvano-pagamentos` |
| PerfectPay | `perfectpay` |
| Lastlink | `lastlink` |
| Eduzz | `eduzz` |

#### Passo 1 — Perguntar configuracao

```
MINERACAO VIA RECLAME AQUI
===========================
Usa Edge headless pra scrapar reclamacoes recentes.

Quantas paginas por gateway? (2-20) [padrao: 10]
> [resposta ou Enter]

Max detalhes por gateway? (5-30) [padrao: 15]
> [resposta ou Enter]

Gateways (separar por virgula, ou Enter pra todos os 8):
> [resposta ou Enter]

Tempo estimado: ~[X] minutos
Minerando...
```

#### Passo 2 — Rodar o script

```bash
python minerador-reclameaqui.py [gateways] [paginas] [max_detalhes]
```

Exemplos:
- `python minerador-reclameaqui.py` — todos os 8 gateways
- `python minerador-reclameaqui.py wiapy,cakto,kirvano 10 15` — 3 especificos

O script:
1. Sobe Edge headless automaticamente
2. Navega no Reclame Aqui de cada gateway, paginando
3. Entra em cada reclamacao e extrai: data, conteudo, preco, cidade
4. Classifica: low_ticket / possivel / generico
5. Extrai nome do produto e nicho automaticamente
6. Salva JSON em `./mineracao/`
7. Mata Edge no final

Tempo: ~2-3 min por gateway (8 gateways = ~20 min)

#### Passo 3 — Ler resultados e mostrar

Ler o JSON gerado e agrupar por produto. Mostrar rankeado por frequencia:

```
PRODUTOS ENCONTRADOS — RECLAME AQUI
=====================================
8 gateways | [X] reclamacoes | [X]s

#  | Recl. | Produto                        | Gateway    | Preco   | Nicho
---|-------|-------------------------------|-----------|---------|------------------
1  | [Xx]  | [nome]                         | [gateway]  | R$XX    | [nicho]
2  | [Xx]  | [nome]                         | [gateway]  | R$XX    | [nicho]
3  | [Xx]  | [nome]                         | [gateway]  | R$XX    | [nicho]
...

TERMOS PRA BUSCAR NA BIBLIOTECA DE ANUNCIOS:
  - "[nome produto 1]"
  - "[nome produto 2]"
  ...

============================================

[D] Ver detalhes de uma oferta (digite o numero)
[N] Nova mineracao com config diferente
[0] Voltar ao menu
```

#### Detalhe de oferta

```
DETALHE — [Nome do Produto]
===========================

Gateway: [gateway]
Reclamacoes: [X]
Nicho: [nicho]
Precos mencionados: [lista]

Reclamacoes:
  - [data] [cidade] "[titulo]"
    "[conteudo resumido]"
    URL: [link]
  ...

Proximo passo sugerido:
  → Buscar na Biblioteca de Anuncios
  → Ou rodar [3] Analisar & Definir produto

[0] Voltar pra lista
```

---

### Metodo B — Biblioteca de Anuncios (Meta)

#### Logica
A Biblioteca de Anuncios mostra TODOS os anuncios ativos no Brasil. Paginas com muitos anuncios ativos sobre o mesmo produto = oferta escalada. Buscar por palavras-chave de low ticket e ver quem ta rodando pesado.

#### Passo 1 — Escolher nicho

```
BIBLIOTECA DE ANUNCIOS — META
===============================

Escolha o nicho pra buscar:

  [1] Geral (todos os nichos)
  [2] Saude / Emagrecimento
  [3] Artesanato / DIY
  [4] Culinaria
  [5] Beleza
  [6] Educacao / Concurso
  [7] Renda / Digital
  [8] Esoterico
  [9] Design / Social Media

Digite o numero:
```

#### Passo 2 — Palavras-chave

Mostrar palavras-chave curadas do nicho escolhido. O usuario escolhe uma ou digita a sua.

**[1] Geral:**
```
  1. pack                     5. +1000
  2. mega pack                6. acervo completo
  3. kit completo             7. combo
  4. +500                     8. moldes prontos
```

**[2] Saude / Emagrecimento:**
```
  1. seca barriga             5. barriga chapada
  2. truque pra emagrecer     6. detox
  3. receitas fit             7. dieta
  4. desinchar                8. metabolismo
```

**[3] Artesanato / DIY:**
```
  1. croche                   5. costura moldes
  2. bordado                  6. trico
  3. amigurumi                7. patchwork
  4. feltro                   8. pintura em tecido
```

**[4] Culinaria:**
```
  1. bolo caseiro             5. brigadeiro gourmet
  2. confeitaria              6. marmita fit
  3. doces gourmet            7. bolo no pote
  4. salgados                 8. receitas lucrativas
```

**[5] Beleza:**
```
  1. unhas decoradas          5. design sobrancelha
  2. cilios                   6. penteados
  3. alongamento              7. nail art
  4. micropigmentacao         8. extensao capilar
```

**[6] Educacao / Concurso:**
```
  1. questoes comentadas      5. reforco escolar
  2. simulado                 6. plano de aula
  3. apostila                 7. provas resolvidas
  4. atividades infantis      8. educacao infantil
```

**[7] Renda / Digital:**
```
  1. renda extra              5. dropshipping
  2. PLR                      6. marketing digital
  3. canva templates          7. dinheiro online
  4. trafego pago             8. afiliado
```

**[8] Esoterico:**
```
  1. tarot                    5. simpatias
  2. signos                   6. meditacao
  3. mapa astral              7. cristais
  4. oracoes                  8. numerologia
```

**[9] Design / Social Media:**
```
  1. artes editaveis          5. templates canva
  2. logos prontos             6. identidade visual
  3. posts prontos            7. artes para redes
  4. feed instagram           8. stories prontos
```

```
Escolha uma palavra-chave (numero) ou digite a sua:
> [resposta]
```

#### Passo 3 — Abrir Biblioteca

Construir a URL da Biblioteca de Anuncios com a palavra-chave escolhida:

URL: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&q=[KEYWORD]&media_type=all`

Onde `[KEYWORD]` e a palavra-chave URL-encoded.

Abrir a URL no navegador do usuario via dev-browser. Se dev-browser nao estiver disponivel, mostrar a URL pra copiar.

```
Abrindo Biblioteca de Anuncios...

Termo: "[keyword]"
URL: [url completa]

O QUE PROCURAR:
  - Paginas com 5+ anuncios ativos = sinal de escala
  - Anuncios rodando ha 30+ dias = lucrativos
  - Videos com variacoes = ta testando (funciona)
  - Precos baixos nos criativos (R$7-47) = low ticket

Quando encontrar uma oferta boa:
  → Copie o nome da pagina
  → Rode [3] Analisar & Definir produto
  → Ou rode [4] Modelar funil se ja tem o link da pagina

============================================

[N] Buscar outro termo
[T] Trocar de nicho
[0] Voltar ao menu
```

---

### Metodo C — RatoAds

#### Logica
O RatoAds ja tem interface visual completa com swipe, filtros, analise de criativos e metricas. Melhor abrir direto no navegador do que replicar no terminal.

#### Fluxo

**Se NAO tem credenciais no config:**

```
MINERACAO VIA RATOADS
=====================

Voce ainda nao conectou sua conta RatoAds.

Como aluno do Curso Low Ticket Automatizado, voce tem
direito a um trial exclusivo: 3 mineracoes, 3 analises
e 3 slots de rastreamento por 30 dias.

  [1] Ativar trial do curso (3/3/3 por 30 dias)
  [2] Ja tenho conta — configurar agora
  [3] Quero assinar — abrir ratoads.com.br

[0] Voltar ao menu
```

Se [1] — Ativar trial:
Pedir email + codigo. POST `https://ratoads.com.br/api/trial/curso`.
200 = conta criada, salvar no config. 403 = codigo invalido. 409 = email ja existe.

Se [2] — Ja tem conta:
Pedir email + senha. Salvar em `./config-automatico.json`.

Se [3] — Assinar:
Mostrar URL ratoads.com.br e planos (Starter R$57,90/mes, Premium R$147,90/tri).

**Se TEM credenciais no config:**

1. Autenticar via POST `https://ratoads.com.br/api/auth/login`
2. Se OK, abrir `https://ratoads.com.br` no navegador via dev-browser
3. Mostrar:

```
RatoAds aberto no navegador!
Plano: [plano] | [nome]

Use a interface do RatoAds pra minerar, analisar e rastrear ofertas.

Quando encontrar uma oferta boa:
  -> Copie o nome da pagina ou link
  -> Volte aqui e rode [3] Analisar & Definir produto

[0] Voltar ao menu
```

Se dev-browser nao disponivel, mostrar URL pra copiar.

---

## [3] ANALISAR & DEFINIR PRODUTO

### Objetivo
Analisar uma oferta da Biblioteca de Anuncios do Meta em profundidade (publico, criativos, funil, escala) e decidir a estrategia: clonar o produto (mesmo produto, execucao melhor) ou modelar (novo produto pro mesmo publico validado).

### Fluxo

Ao selecionar [3], mostrar:

```
ANALISAR & DEFINIR PRODUTO
===========================

  [1] Analisar oferta (Biblioteca de Anuncios)
  [2] Definir produto (clonar ou modelar)

Digite o numero:
```

---

### [1] ANALISAR OFERTA

```
> 1

Como quer informar a oferta?
  [A] Colar link da Biblioteca de Anuncios (pagina ou anuncio)
  [B] Nome da pagina/anunciante
  [C] Usar oferta da ultima mineracao

Qual opcao?
```

#### Passo 1 — Buscar dados da oferta

**Opcao A — Link da Biblioteca:**

O usuario cola um link tipo:
- `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&view_all_page_id=XXXXX`
- `https://www.facebook.com/ads/library/?id=XXXXX`

Extrair o `page_id` ou `ad_id` do link.
Usar WebFetch pra acessar e extrair os dados disponiveis.

**Opcao B — Nome:**

```
Nome da pagina ou anunciante:
> [nome]

Buscando na Biblioteca de Anuncios...
```

Usar WebSearch com query: `site:facebook.com/ads/library "[nome]" Brasil`

**Opcao C — Ultima mineracao:**

Ler o ultimo arquivo de `./mineracao/` e listar as ofertas encontradas.
O usuario escolhe pelo numero.

#### Passo 2 — Analise completa

Analisar TUDO que conseguir extrair sobre a oferta:

**O que analisar:**

1. **PAGINA/ANUNCIANTE**
   - Nome da pagina
   - Categoria
   - Quantidade de anuncios ativos
   - Ha quanto tempo ta anunciando (primeiro anuncio visivel)

2. **PUBLICO VALIDADO**
   - Quem e o publico-alvo baseado nos criativos (genero, idade provavel, interesses)
   - Que linguagem usam (formal, informal, tecnica)
   - Que dores/desejos os criativos atacam
   - Nivel de consciencia do publico (inconsciente, consciente do problema, consciente da solucao)

3. **OFERTA**
   - O que vendem (produto digital, fisico, servico)
   - Faixa de preco provavel (se visivel no criativo ou landing)
   - Angulo principal de venda (medo, ganancia, vaidade, curiosidade)
   - Nicho e sub-nicho

4. **CRIATIVOS**
   - Quantidade de criativos ativos
   - Formatos usados (video, imagem, carrossel)
   - Proporcao de cada formato
   - Hooks identificados (texto dos primeiros 3 segundos ou headline da imagem)
   - CTAs usados
   - Se tem variacao de angulo ou ta batendo na mesma tecla

5. **FUNIL**
   - URL da landing page (se visivel)
   - Tipo de funil (pagina direta, quiz, VSL, webinar)
   - Gateway de checkout (se identificavel)

6. **ESCALA**
   - Estimativa de escala baseada em: qtd anuncios, tempo rodando, variacao de criativos
   - Score de escala: Baixa / Media / Alta / Monstro

#### Passo 3 — Mostrar relatorio

```
ANALISE COMPLETA DA OFERTA
============================
Pagina: [nome]
Anuncios ativos: [X]
Tempo anunciando: [X dias/meses]
Score de escala: [BAIXA/MEDIA/ALTA/MONSTRO]

--------------------------------------------
PUBLICO VALIDADO
--------------------------------------------
Genero principal: [M/F/Ambos]
Faixa etaria provavel: [XX-XX anos]
Interesses/comportamento: [lista]
Dores atacadas:
  - [dor 1]
  - [dor 2]
  - [dor 3]
Desejos atacados:
  - [desejo 1]
  - [desejo 2]
Nivel de consciencia: [nivel]
Linguagem: [formal/informal/tecnica]

--------------------------------------------
OFERTA
--------------------------------------------
Tipo: [produto digital / fisico / servico]
Nicho: [nicho] > [sub-nicho]
Preco estimado: R$[XX]
Angulo principal: [medo/ganancia/vaidade/curiosidade]
Proposta de valor: "[frase que resume a promessa]"

--------------------------------------------
CRIATIVOS ([X] ativos)
--------------------------------------------
Formatos:
  Video: [X] ([X]%)
  Imagem: [X] ([X]%)
  Carrossel: [X] ([X]%)

Top hooks identificados:
  1. "[hook 1]"
  2. "[hook 2]"
  3. "[hook 3]"

CTAs mais usados:
  - "[cta 1]"
  - "[cta 2]"

Variedade de angulos: [Baixa/Media/Alta]
  [lista dos angulos diferentes identificados]

--------------------------------------------
FUNIL
--------------------------------------------
Landing page: [url ou "nao identificada"]
Tipo de funil: [direto/quiz/VSL/webinar]
Gateway: [gateway ou "nao identificada"]

============================================

VEREDICTO:
[Paragrafo curto com conclusao — vale clonar? vale modelar?
 O publico ta saturado ou tem espaco? Os criativos sao bons
 ou da pra fazer melhor facilmente?]

============================================

[D] Definir produto baseado nessa analise
[S] Salvar analise
[N] Analisar outra oferta
[0] Voltar ao menu
```

Se [S], salvar em `./analises/[nome-pagina]-[data].md`

---

### [2] DEFINIR PRODUTO

Se o usuario vier direto (sem ter analisado antes):

```
> 2

Voce ainda nao analisou nenhuma oferta nessa sessao.
Quer analisar uma primeiro?

  [1] Sim — ir pra analise
  [2] Nao — ja sei o que quero fazer

Qual opcao?
```

Se escolher [2] sem analise, pedir descricao manual:
```
Descreve brevemente a oferta que quer trabalhar:
  - Nicho:
  - Produto:
  - Publico:
  - Link (se tiver):
```

Se ja tem analise (veio do [D] do relatorio ou ja analisou):

```
DEFINIR PRODUTO
================
Baseado na analise de: [nome da pagina/oferta]

Qual estrategia?

  [1] CLONAR — Mesmo produto, execucao melhor
      Vai manter: nicho, tipo de produto, publico
      Vai melhorar: criativos, funil, copy, preco

  [2] MODELAR — Novo produto, mesmo publico validado
      Vai manter: publico validado, dores/desejos
      Vai criar: produto diferente pro mesmo publico

Qual opcao?
```

---

#### [1] CLONAR PRODUTO

```
> 1

CLONAR PRODUTO
===============
Oferta original: [nome]
Estrategia: mesmo produto, execucao superior

Analisando o que manter e o que melhorar...
```

**Output:**

```
PLANO DE CLONE
===============

PRODUTO:
  Nome sugerido: "[nome modelado — nao copia identico]"
  Tipo: [mesmo tipo do original]
  Preco sugerido: R$[XX] (original: R$[XX])
  Justificativa do preco: [por que esse preco]

O QUE MANTER DO ORIGINAL:
  - [elemento 1 que funciona]
  - [elemento 2 que funciona]
  - [elemento 3 que funciona]

O QUE MELHORAR:
  1. CRIATIVOS:
     - Problema: [o que ta fraco nos criativos originais]
     - Melhoria: [o que fazer diferente]
     - Formatos recomendados: [formatos]

  2. FUNIL:
     - Problema: [o que ta fraco no funil]
     - Melhoria: [o que fazer diferente]
     - Tipo de pagina: [recomendacao]

  3. COPY:
     - Headline sugerida: "[headline]"
     - Angulo de venda: [angulo]
     - CTA: "[cta]"

  4. ORDER BUMP sugerido:
     - "[nome do bump]" — R$[XX]
     - Por que combina: [justificativa]

  5. UPSELL sugerido:
     - "[nome do upsell]" — R$[XX]
     - Por que funciona: [justificativa]

ENTREGAVEL SUGERIDO:
  - [descricao do que entregar — PDF, area de membros, app, etc]
  - [como montar rapido]

============================================

Proximo passo:
  → [5] Modelar funil (gerar pagina de vendas)
  → [6] Gerar criativos

[S] Salvar plano
[0] Voltar ao menu
```

---

#### [2] MODELAR PRODUTO

```
> 2

MODELAR PRODUTO
================
Publico validado de: [nome da oferta original]
Estrategia: novo produto pro mesmo publico

Pensando em produtos que atendem as mesmas dores...
```

**O que a skill faz:**

1. Pega as dores e desejos identificados na analise
2. Identifica o que o concorrente JA cobre (pra nao repetir)
3. Pensa em 5 produtos com angulo OPOSTO ao concorrente
4. Filtra por criterios de qualidade (ver abaixo)

**Criterios obrigatorios — produto bom pra modelar:**

- **Numero grande na headline** — +200, +500, +1000. Volume = valor percebido. Sem numero = fraco
- **Angulo OPOSTO ao concorrente** — se ele vende teoria, modelar pratica. Se ele vende material visual, modelar ferramenta. NUNCA sugerir o que o concorrente ja faz ou da de bonus
- **Dor URGENTE do publico** — nao "aprender X", mas "passar na prova dia Y", "parar de perder dinheiro", "emagrecer pro verao". Urgencia real > curiosidade generica
- **Impossivel de achar gratis** — se o cara acha no Google de graca (mapas mentais, resumos, templates basicos), NAO presta como produto. Tem que ter volume ou especificidade que nao existe gratis
- **Facil de criar mas parece caro** — PDF com 500 itens parece muito trabalho pro comprador mas Claude gera em minutos. Planilha complexa parece cara mas e rapida de montar

**Produto RUIM (NUNCA sugerir):**
- Qualquer coisa que o concorrente ja da de bonus
- Material generico que acha no Google (mapas mentais, resumos basicos, templates simples)
- Sem numero na headline
- Sem urgencia real
- Curso/mentoria (nao e low ticket)
- App (complexo demais pra criar rapido)

**Output:**

```
MODELAGEM DE PRODUTO
=====================
Publico: [publico do concorrente — amplo]
Concorrente: [o que ele vende]
Angulo: [o que ele foca]

5 IDEIAS:

#1 — [+NUMERO Nome Curto]
  R$[XX] | [formato]
  [Angulo concorrente] → [ANGULO OPOSTO]
  [por que nao acha gratis] | [POTENCIAL]

#2 — [+NUMERO Nome Curto]
  R$[XX] | [formato]
  [Angulo concorrente] → [ANGULO OPOSTO]
  [por que nao acha gratis] | [POTENCIAL]

#3 — [+NUMERO Nome Curto]
  R$[XX] | [formato]
  [Angulo concorrente] → [ANGULO OPOSTO]
  [por que nao acha gratis] | [POTENCIAL]

#4 — [+NUMERO Nome Curto]
  R$[XX] | [formato]
  [Angulo concorrente] → [ANGULO OPOSTO]
  [por que nao acha gratis] | [POTENCIAL]

#5 — [+NUMERO Nome Curto]
  R$[XX] | [formato]
  [Angulo concorrente] → [ANGULO OPOSTO]
  [por que nao acha gratis] | [POTENCIAL]

Escolha (1-5):
```

**IMPORTANTE:** As 5 ideias devem cobrir angulos DIVERSOS pro publico do concorrente — nao ficar travado num sub-nicho so. Se o concorrente vende pra "estudantes de direito", as ideias devem cobrir: prova, profissional, professor, legislacao, pratica. Nao 5 variacoes de "questoes OAB".

Escolha um produto pra detalhar (1-5):
```

Quando o usuario escolher:

```
PRODUTO ESCOLHIDO: [nome]
==========================

DETALHAMENTO:

Nome completo: "[nome de venda — como aparece no checkout]"
Headline da pagina: "[headline sugerida]"
Preco: R$[XX]
Ancora: De R$[XX] por R$[XX]

ENTREGAVEL:
  - [item 1 do entregavel]
  - [item 2 do entregavel]
  - [item 3 do entregavel]
  Como montar: [instrucoes rapidas — ex: PDF no Canva, planilha no Google Sheets]

ORDER BUMP:
  - "[nome]" — R$[XX]
  - [descricao curta]

UPSELL:
  - "[nome]" — R$[XX]
  - [descricao curta]

BONUS SUGERIDOS:
  1. "[bonus 1]" — [descricao]
  2. "[bonus 2]" — [descricao]
  3. "[bonus 3]" — [descricao]

ANGULO DE VENDA:
  Dor principal atacada: [dor]
  Promessa: "[promessa em 1 frase]"
  Prova: [que tipo de prova usar — numeros, depoimentos, demonstracao]

============================================

Proximo passo:
  → [5] Modelar funil (gerar pagina de vendas)
  → [6] Gerar criativos

[S] Salvar produto
[E] Escolher outro produto da lista
[0] Voltar ao menu
```

Se [S], salvar em `./produtos/[nome-produto].md`

---

## [4] GERAR ENTREGAVEL

### Objetivo
Criar o produto digital completo que o comprador vai receber. Pega a definicao do [3] (nome, nicho, tipo, entregavel) e gera o conteudo inteiro — formatado e pronto pra entregar.

### Fluxo

Ao selecionar [4], mostrar:

```
GERAR ENTREGAVEL
=================

Vou criar o produto digital completo pra voce.

Qual formato?

  [1] PDF / Ebook (receitas, guias, manuais, apostilas)
  [2] Pack de conteudo (artes, templates, moldes, projetos)
  [3] Planilha (controle, calculadora, organizador)
  [4] Kit de materiais (checklist + guia + bonus combinados)
  [5] Questionario / Simulado (questoes com gabarito)

Digite o numero:
```

---

### [1] PDF / EBOOK

```
PDF / EBOOK
============

Sobre o produto:
  Nome: [puxar do [3] se tiver, senao perguntar]
  Nicho: [nicho]

Quantas paginas/itens? (ex: 50 receitas, 200 questoes, 30 capitulos)
> [resposta]

Estilo do conteudo:
  [1] Pratico/direto (passo a passo, sem enrolacao)
  [2] Educativo (explica o "por que", mais profundo)
  [3] Listagem (muitos itens curtos — tipo pack)

> [resposta]

Gerando conteudo...
```

**O que gerar:**

1. **Capa** — titulo + subtitulo + visual (gerar prompt pro ChatGPT/DALL-E)
2. **Sumario** — indice organizado por categorias
3. **Conteudo completo** — cada item com:
   - Titulo
   - Conteudo detalhado (receita completa, passo a passo, explicacao)
   - Dica extra ou variacao (agrega valor)
4. **Pagina final** — CTA pra upsell ou redes sociais

**Formato de saida:** HTML estilizado pronto pra converter em PDF.
- Layout limpo, mobile-friendly
- Fontes: Inter + Space Grotesk
- Cores do nicho
- Imagens placeholder com descricao do que colocar
- Salvar em `./entregaveis/[nome]/entregavel.html`

```
ENTREGAVEL GERADO!
===================
Arquivo: ./entregaveis/[nome]/entregavel.html

Conteudo:
  - Capa com titulo e subtitulo
  - Sumario com [X] categorias
  - [X] itens completos
  - Pagina final com CTA

COMO CONVERTER PRA PDF:
  1. Abra o arquivo .html no navegador
  2. Ctrl+P (ou Cmd+P)
  3. Destino: "Salvar como PDF"
  4. Pronto!

  OU use o site html2pdf.com pra converter online.

PROMPT PRA CAPA (cole no ChatGPT):
  "[prompt otimizado pra gerar capa profissional do produto]"

============================================

[V] Ver preview do conteudo
[A] Ajustar conteudo (adicionar/remover/editar itens)
[C] Gerar capa com IA (Higgsfield)
[0] Voltar ao menu
```

---

### [2] PACK DE CONTEUDO

```
PACK DE CONTEUDO
=================

Tipo de pack:
  [1] Artes editaveis (posts, stories, banners)
  [2] Templates (Canva, Google Docs, Notion)
  [3] Moldes / Projetos (PDF com medidas e instrucoes)
  [4] Colecao de materiais (mistura de formatos)

> [resposta]

Quantidade de itens:
> [ex: 500, 1000, +200]

Nicho/tema:
> [ex: serralheria, confeitaria, social media]

Gerando pack...
```

**O que gerar:**

Depende do tipo:
- **Artes:** gerar prompts otimizados pro Canva/ChatGPT pra cada arte + guia de como personalizar
- **Templates:** gerar os templates em HTML ou instrucoes detalhadas pra replicar no Canva
- **Moldes/Projetos:** gerar descricoes tecnicas completas, medidas, materiais, passo a passo
- **Colecao:** mix de tudo acima

**Saida:** HTML organizado por categorias + guia de uso.
Salvar em `./entregaveis/[nome]/`

```
PACK GERADO!
==============
Arquivo: ./entregaveis/[nome]/pack.html

Conteudo:
  - [X] itens organizados em [X] categorias
  - Indice navegavel
  - Guia de uso/personalizacao

[V] Ver preview
[A] Ajustar
[0] Voltar ao menu
```

---

### [3] PLANILHA

```
PLANILHA
=========

Tipo:
  [1] Controle / Organizador (financeiro, estoque, rotina)
  [2] Calculadora (orcamento, precificacao, metricas)
  [3] Tracker (habitos, metas, progresso)
  [4] Lista / Banco de dados (fornecedores, contatos, receitas)

> [resposta]

Descricao do que a planilha faz:
> [resposta]

Gerando planilha...
```

**O que gerar:**

Gerar arquivo CSV ou HTML tabular com:
- Cabecalhos formatados
- Formulas descritas (pra o usuario replicar no Google Sheets/Excel)
- Dados de exemplo preenchidos
- Aba de instrucoes

Salvar em `./entregaveis/[nome]/planilha.csv` + `instrucoes.html`

```
PLANILHA GERADA!
=================
Arquivos:
  - ./entregaveis/[nome]/planilha.csv
  - ./entregaveis/[nome]/instrucoes.html

COMO USAR:
  1. Abra o .csv no Google Sheets ou Excel
  2. Siga as instrucoes no arquivo instrucoes.html
  3. Personalize com sua marca/dados

[V] Ver preview
[A] Ajustar colunas/dados
[0] Voltar ao menu
```

---

### [4] KIT DE MATERIAIS

```
KIT DE MATERIAIS
=================

Um kit combina varios formatos num pacote so.
Ideal pra aumentar valor percebido.

O que incluir no kit?
  [1] Guia principal (PDF) + Checklist + Bonus
  [2] Ebook + Planilha + Templates
  [3] Manual + Video-aulas (roteiros) + Materiais de apoio
  [4] Personalizado (me diz o que quer)

> [resposta]

Gerando kit completo...
```

Gera cada peca separada usando os fluxos acima e organiza numa pasta:

```
KIT GERADO!
=============
Pasta: ./entregaveis/[nome]/

  📁 principal/
     guia.html (PDF principal)
  📁 bonus/
     checklist.html
     planilha.csv
     templates.html
  📁 capas/
     prompts-capas.md (prompts pra gerar capas no ChatGPT)

Total: [X] pecas prontas

[V] Ver conteudo de uma peca
[A] Ajustar
[0] Voltar ao menu
```

---

### [5] QUESTIONARIO / SIMULADO

```
QUESTIONARIO / SIMULADO
=========================

Area:
> [ex: OAB, concurso, ENEM, certificacao]

Quantidade de questoes:
> [ex: 500, 200, 100]

Formato:
  [1] Multipla escolha (4 alternativas + gabarito comentado)
  [2] Certo/Errado com justificativa
  [3] Mix (multipla escolha + dissertativas)

> [resposta]

Nivel:
  [1] Basico
  [2] Intermediario
  [3] Avancado
  [4] Mix de niveis

> [resposta]

Gerando questoes...
```

**O que gerar:**

- Questoes organizadas por tema/materia
- Cada questao com: enunciado, alternativas, gabarito, comentario explicativo
- Indice por materia
- Simulado cronometrado (sugestao de tempo por questao)

Salvar em `./entregaveis/[nome]/simulado.html`

```
SIMULADO GERADO!
==================
Arquivo: ./entregaveis/[nome]/simulado.html

Conteudo:
  - [X] questoes em [X] materias
  - Gabarito comentado questao por questao
  - Indice por materia
  - Sugestao de cronometro

[V] Ver preview
[A] Ajustar questoes
[G] Gerar mais questoes (expandir)
[0] Voltar ao menu
```

---

### Regras gerais do modulo

1. **Sempre puxar dados do [3]** se o usuario ja definiu o produto — nao perguntar de novo
2. **Conteudo real e util** — nao gerar lixo. Cada item deve ter valor genuino pro comprador
3. **Volume importa** — se o produto promete "+500 receitas", gerar as 500. Nao enrolar
4. **Formato HTML** — sempre gerar em HTML estilizado pra facilitar conversao pra PDF
5. **Salvar em** `./entregaveis/[nome-produto]/`
6. **Oferecer ajustes** — o usuario pode pedir pra adicionar, remover ou editar itens ate ficar satisfeito
7. **Nao plagiar** — gerar conteudo original inspirado no nicho, nunca copiar de fontes especificas

---

## [5] MODELAR FUNIL

### Objetivo
Pegar a pagina de vendas do concorrente, analisar, e gerar uma versao melhorada. SEMPRE parte da pagina do concorrente como base — nunca gera do zero.
- Se o cara escolheu CLONAR no [3]: mesmo produto, melhora a pagina (design, pontos fracos, reorganiza secoes)
- Se o cara escolheu MODELAR no [3]: usa a pagina do concorrente como base mas adapta pro produto novo que ele definiu

### Fluxo

Ao selecionar [5], mostrar:

```
MODELAR FUNIL
==============

Preciso da pagina do concorrente pra usar como base.

  [A] Colar link da pagina de vendas
  [B] Colar HTML salvo (se ja baixou a pagina)

Qual opcao?
```

---

### Passo 1 — Obter a pagina do concorrente

**Opcao A — Link:**

```
> A

Cola o link da pagina de vendas do concorrente:
> [link]

Baixando pagina...
```

Usar WebFetch pra acessar o link.
- Se 403/bloqueio (cloaker): sugerir opcao B
  ```
  Pagina bloqueou o acesso (provavelmente cloaker).
  Abra no celular, salve como HTML, e use opcao [B].

  [B] Colar HTML
  [0] Voltar ao menu
  ```
- Se OK: seguir pro Passo 2

**Opcao B — HTML colado:**

```
> B
Cole o HTML (ou caminho do arquivo .html):
> [html ou caminho]
```

Ler o conteudo e seguir pro Passo 2.

---

### Passo 2 — Analisar a pagina do concorrente

Analisar o HTML e mapear cada secao pra estrutura TSL padrao:

```
ANALISE DO FUNIL
================
URL: [url]

SECAO                | NOTA | STATUS     | ANALISE
---------------------|------|------------|---------------------------
Sticky bar/urgencia  | X/10 | [tem/falta] | [analise]
Hero (headline+img)  | X/10 | [tem/falta] | [analise]
Pain points/dor      | X/10 | [tem/falta] | [analise]
O que voce recebe    | X/10 | [tem/falta] | [analise]
Prova social         | X/10 | [tem/falta] | [analise]
Bonus                | X/10 | [tem/falta] | [analise]
Pricing/ancora       | X/10 | [tem/falta] | [analise]
Garantia             | X/10 | [tem/falta] | [analise]
FAQ                  | X/10 | [tem/falta] | [analise]
CTA final            | X/10 | [tem/falta] | [analise]

NOTA GERAL: X/10

SECOES FORTES (manter modelado):
  - [secao]: [por que funciona]
  ...

SECOES FRACAS (reescrever):
  - [secao]: [problema + como melhorar]
  ...

SECOES FALTANDO (adicionar):
  - [secao]: [por que precisa]
  ...

============================================

[G] Gerar versao melhorada
[D] Ver detalhe de uma secao
[0] Voltar ao menu
```

Se [D], mostrar detalhe da secao com 5 sugestoes de melhoria.

Se [G], perguntar a estrategia:

```
Qual estrategia pra essa pagina?

  [1] CLONAR — Mesmo produto, pagina melhorada
      Mantém o produto/oferta original. Melhora design,
      pontos fracos, reorganiza secoes.

  [2] MODELAR — Produto diferente, pagina adaptada
      Usa essa pagina como base mas adapta pro seu
      produto (definido no passo [3]).

Qual opcao?
```

Se escolher [2] e nao tem produto definido no [3]:
```
Voce ainda nao definiu um produto no passo [3].

  [1] Ir pro passo [3] primeiro
  [2] Descrever o produto rapidamente agora

Qual opcao?
```

Se [2], pedir: Nome, Nicho, Preco, Entregavel, Publico-alvo.

Seguir pro **Gerador de Pagina**.

---

### GERADOR DE PAGINA

Sempre parte da pagina do concorrente como base. Nunca gera do zero.

**Logica:**
- Secoes com nota >= 7: MANTER a estrutura, modelar o conteudo (nao copiar texto 1:1)
- Secoes com nota < 7: REESCREVER usando as regras da estrutura TSL padrao
- Secoes faltando: ADICIONAR seguindo a estrutura TSL padrao
- Se o concorrente tem uma secao extra que funciona bem e nao ta no padrao, incluir

**Diferenca entre clone e modelar:**
- CLONE: mantém produto, preco, entregavel, publico — so melhora a PAGINA
- MODELAR: troca produto, preco, entregavel, copy — mantém a ESTRUTURA que funciona da pagina do concorrente, adaptada pro novo produto

#### Estrutura TSL padrao (referencia)

A estrutura abaixo e a predefinicao ideal. Se o concorrente tem secoes na mesma ordem, otimo. Se nao, reorganizar pra ficar mais perto disso — a nao ser que a ordem do concorrente esteja funcionando bem (nota alta).

```
ESTRUTURA DA PAGINA
====================

1. STICKY BAR (urgencia)
   Timer regressivo ou frase de escassez no topo fixo

2. HERO
   - Header (logo ou nome da marca — opcional)
   - Headline (simples e impactante — formula: [numero] + [beneficio] + [qualificador])
   - Imagem do produto OU video (depende da oferta)
   - CTA principal
   - Sub-CTA (ex: "Acesso imediato. Pagamento unico.")
   - Stats de prova rapida (ex: "+4.700 compraram", "92% satisfacao")

3. DOR / PAIN POINTS (opcional — depende do nicho)
   Lista de problemas que o publico enfrenta
   Fechar com frase de transicao: "A verdade e que..."

4. O QUE VOCE VAI RECEBER
   Cards/grid mostrando cada item do entregavel
   Formato: icone/emoji + titulo + descricao curta
   Se o produto tem categorias (ex: serralheria tem portoes, churrasqueiras, etc.), mostrar grid

5. PROVA SOCIAL
   Depoimentos (idealmente 3)
   Formato: nome + local + estrelas + texto
   Se tiver video de depoimento, melhor ainda

6. BONUS
   Cards com cada bonus
   Formato: tag "BONUS X" + titulo + descricao + preco riscado (ex: "R$997")
   Fechar com: "Tudo isso sai DE GRACA adquirindo hoje"

7. PRICING (cards de plano)
   Plano Basico: so o produto principal, preco baixo (R$7-10)
   Plano Premium (DESTAQUE): produto + bonus + extras, preco real (R$17-37)
   Badge "MAIS VENDIDO" no premium
   Ancora de preco: "De R$XXX por apenas R$XX"
   CTAs diferentes em cada plano
   Badges de confianca: garantia + vitalicio + seguro

8. GARANTIA
   Imagem do selo de garantia
   Headline: "Risco ZERO: Garantia de 7 Dias"
   Texto: devolvemos cada centavo, sem perguntas

9. FAQ (accordion)
   5-8 perguntas frequentes
   Perguntas padrao: "Como recebo?", "Funciona pra [objecao]?", "E se nao gostar?", "O acesso e vitalicio?"

10. CTA FINAL (urgencia)
    Headline de urgencia: "Amanha esse preco nao existe mais" ou similar
    Ultimo botao de compra
    Frase ancora: "R$XX hoje ou R$XXXX de prejuizo"

11. FOOTER
    Texto legal minimo (gateway, direitos reservados)

12. POPUP DOWNSELL (opcional)
    Dispara quando clica no plano basico
    Oferece o premium com desconto
    "Por apenas R$X a mais voce leva tudo"
```

#### Regras de geracao do HTML

**Design:**
- Mobile-first (80%+ do trafego pago vem do celular)
- Inline CSS (sem dependencias externas pesadas)
- Carregar fontes do Google Fonts: Inter (corpo) + Space Grotesk (headlines, precos)
- Responsivo: max-width 600px no container principal
- Cores: definir paleta baseada no nicho (escuro pra masculino, claro pra feminino, etc.)
- Botao CTA: cor contrastante, grande, com hover effect
- Cards com border-radius 12px, sombra sutil, hover translateY

**Copy:**
- Headline: formula [numero] + [beneficio] + [qualificador sem objecao]
  Exemplos:
  - "+500 Questoes OAB Comentadas"
  - "Pack 1000 do Serralheiro"
  - "47 Receitas Fit Pra Perder 7kg em 14 Dias"
- Bullets: especificos com numeros, nunca genericos
- CTA: verbo de acao + urgencia ("QUERO COMECAR AGORA", "PARAR DE PERDER DINHEIRO")
- Ancora: 5-7x o preco real (De R$197 por R$27)
- Tom: informal BR, direto, sem floreio

**Elementos interativos (incluir no HTML):**
- Timer regressivo na sticky bar (15min a partir do acesso)
- FAQ accordion (click pra expandir/colapsar)
- Popup downsell no click do plano basico (se tiver 2 planos)
- Social proof notification flutuante (opcional — "[Nome] acabou de comprar ha X minutos")

**Placeholders:**
- Imagens: usar placeholder descritivo no src (ex: `src="assets/hero.jpg"`) + comentario HTML dizendo o que colocar
- Links de checkout: usar `#checkout-premium` e `#checkout-basico` como placeholder — o usuario substitui pelo link da Wiapy/gateway
- Pixel: deixar espaco comentado pra Meta Pixel e Utmify
  ```html
  <!-- META PIXEL: cole seu pixel aqui -->
  <!-- UTMIFY: cole seu pixel aqui -->
  ```

#### Adaptacao por estrategia

**Se CLONE (mesmo produto, pagina melhorada):**
- Manter mesmo produto, preco, entregavel, publico do concorrente
- Headline: reformular (nao copiar 1:1) — manter a promessa mas melhorar a formulacao
- Secoes com nota >= 7: manter a ESTRUTURA mas reescrever o texto (modelar, nao plagiar)
- Secoes com nota < 7: reescrever totalmente usando as regras da estrutura TSL
- Secoes faltando no original: adicionar (ex: se nao tem FAQ, bonus, ou garantia — incluir)
- Design: melhorar layout, cores, responsividade — pode mudar visual completamente

**Se MODELAR (produto novo, pagina adaptada):**
- Trocar produto, preco, entregavel, copy — tudo vira do NOVO produto (definido no [3])
- Manter a ESTRUTURA de secoes do concorrente que funciona (ordem, disposicao, formato)
- Secoes com nota >= 7: manter o formato/layout mas reescrever copy pro novo produto
- Secoes com nota < 7: reescrever usando estrutura TSL + dados do novo produto
- Secoes faltando: adicionar baseado no que o novo produto precisa
- Ex: concorrente tem carrossel de projetos (nota 8) → manter carrossel mas com imagens do novo produto

#### Output

```
PAGINA GERADA!
===============
Arquivo: ./funis/[nome-produto]/pagina-vendas.html

ESTRUTURA FINAL:
  1. Sticky bar — timer 15min
  2. Hero — "[headline gerada]"
  3. O que voce recebe — [X] cards
  4. Prova social — [X] depoimentos
  5. Bonus — [X] bonus
  6. Pricing — [X] planos (basico R$[X] + premium R$[X])
  7. Garantia — 7 dias
  8. FAQ — [X] perguntas
  9. CTA final — urgencia
  10. Footer + popup downsell

PLACEHOLDERS PRA SUBSTITUIR:
  - [ ] Imagem hero: trocar assets/hero.jpg pela sua
  - [ ] Depoimentos: trocar por depoimentos reais
  - [ ] Link checkout premium: #checkout-premium → link da Wiapy
  - [ ] Link checkout basico: #checkout-basico → link da Wiapy
  - [ ] Meta Pixel: colar ID do pixel
  - [ ] Utmify Pixel: colar ID do pixel

Preview: abra o arquivo no navegador.

============================================

[A] Ajustar algo especifico
[R] Refazer com estilo/tom diferente
[P] Adicionar pixels (Meta + Utmify)
[0] Voltar ao menu
```

### [A] Ajustar algo especifico

```
> A
O que quer ajustar?
> [descricao]

Ajustando...
```

Editar o HTML gerado, salvar, mostrar o que mudou. Repetir ate satisfeito.

### [R] Refazer com estilo diferente

```
> R

Qual estilo?
  [1] Dark mode (fundo escuro, texto claro — estilo Pack Serralheiro)
  [2] Light mode (fundo claro, cores suaves — estilo OAB)
  [3] Colorido (cores vibrantes do nicho)
  [4] Minimalista (branco puro, menos secoes)

Qual?
```

Regenerar o HTML com a paleta e estilo escolhido.

### [P] Adicionar pixels

```
> P

ID do Meta Pixel (Facebook):
> [id ou Enter pra pular]

ID do Utmify:
> [id ou Enter pra pular]

Pixels adicionados ao HTML!
Eventos configurados:
  - PageView (automatico)
  - ViewContent (ao ver secao de pricing)
  - InitiateCheckout (ao clicar CTA)
```

Inserir os scripts de pixel no HTML e salvar.

---

## [6] GERAR CRIATIVOS

### Objetivo
Scrapar os criativos reais do concorrente via Apify, transcrever videos, e gerar criativos modelados em cima das copies que JA VENDEM.

### Pre-requisito
- Analise do [3] feita (tem page_id do concorrente)
- Apify token configurado no config-automatico.json
- Produto definido no [3] (nome, preco, angulo)

### Fluxo

Ao selecionar [6]:



---

### Passo 1 — Scrapar criativos do concorrente (Apify)

Usar o page_id da analise do [3] pra scrapar todos os anuncios ativos.



Rodar via apify-client Python:


Mostrar progresso:


### Passo 2 — Ranquear e selecionar

Criterios pra rankear (mais escalado = melhor):
- Tempo rodando (mais antigo = mais gasto)
- Variantes do mesmo criativo (testando = funciona)
- Ativo ha 30+ dias = sinal forte

Mostrar top 7:


### Passo 3 — Transcrever videos

Se tem videos nos top criativos:
1. Baixar video via URL do Apify
2. Transcrever com Whisper
3. Salvar transcricao



### Passo 4 — Gerar criativos MODELADOS

**REGRA: NUNCA inventar copy do zero. SEMPRE modelar em cima das copies reais do concorrente que ja vendem.**

Pra cada criativo:
1. Pegar a copy real do concorrente
2. Manter a ESTRUTURA e MECANISMO que funciona
3. Trocar produto, preco, entregavel pro novo produto
4. Ajustar angulo se necessario

Gerar 4 videos + 3 imagens:

**Videos (4):**
- Video 1 e 2: CLONE da copy real do concorrente, modelado pro novo produto. Mesma estrutura, mesmo mecanismo, so troca produto/preco/entregavel
- Video 3: DIRETO — estilo "+500 Questoes por R$10". Headline de impacto + bullets do que recebe + bonus + preco + CTA. Copy objetiva, sem storytelling
- Video 4: EMOCIONAL — storytelling em 1a pessoa. Comecar com dor real ("quase desisti", "me sentia burra"), contar jornada, apresentar solucao, fechar com preco

**Imagens (3):**
- Imagem 1: CLONE do formato visual do concorrente, adaptado pro produto
- Imagem 2: PROVA SOCIAL — depoimento/resultado ("consegui", "passei", "mudou minha vida")
- Imagem 3: DIRETO — headline com numero + preco destaque

**REGRA:** Os 2 clones SEMPRE partem da copy REAL scrapada do concorrente. Os outros 5 experimentam angulos novos (direto, emocional, prova social) mas mantendo o MESMO publico e produto.

**Imagens:**
- Baseadas nas imagens reais do concorrente
- Mesmo layout/formato, produto diferente

Formato de cada roteiro (linhas curtas pro terminal):


### Passo 5 — Montar material pro CapCut

Depois de gerar os 7 scripts, montar TODO o material. O cara so junta no CapCut.

**PASSO 1 — Videos de fundo (TikTok)**

Buscar no TikTok videos que combinem com cada copy:
- WebSearch por TikToks virais do nicho
- Usar skill /video-downloader pra baixar
- Criterios: sem legenda, sem marca dagua, vertical 9:16, visual do nicho
- Baixar 6-8 videos (10-30s cada)
- Salvar em `./criativos/[nome]/videos-fundo/`
- Nomear por criativo: fundo-clone1.mp4, fundo-direto.mp4, etc

**PASSO 2 — Gravacao de tela do entregavel**

Instruir o usuario a gravar a tela do produto (PDF, planilha) pra usar como demonstracao:

Orientacao pro usuario:
- Abrir o PDF/material no PC
- Gravar scrollando pelas paginas (15-20s)
- Salvar em `./criativos/[nome]/tela-produto.mp4`
- Vai nos videos na parte de demonstracao

**PASSO 3 — Texto pra voz (MiniMax)**

Gerar o texto CORRIDO de cada video, limpo, sem emojis, sem marcacao de tempo. Pronto pra colar no MiniMax ou outro gerador de voz IA.

Um arquivo por video em `./criativos/[nome]/vozes/`:
- voz-clone1.txt
- voz-clone2.txt
- voz-direto.txt
- voz-emocional.txt

**PASSO 4 — Prompts de imagem**

3 prompts pro ChatGPT/DALL-E em `./criativos/[nome]/imagens/prompts.md`

### Passo 6 — Orientar montagem no CapCut

Mostrar a pasta organizada e instruir:

```
MATERIAL PRONTO!
=================
Pasta: ./criativos/[nome]/

  videos-fundo/    (6-8 videos TikTok)
  vozes/           (4 textos pro MiniMax)
  imagens/         (3 prompts pro ChatGPT)
  roteiros/        (7 scripts completos)

MONTAGEM NO CAPCUT:
  1. Gera a voz no MiniMax (cola o texto)
  2. Importa video de fundo + voz + tela
  3. Sincroniza legenda com a voz
  4. Adiciona musica trending
  5. Exporta 1080x1920

COMECA PELO VIDEO 1 (clone).
E a copy que JA vende pro concorrente.
Menor risco. Sobe esse primeiro.

[V] Ver roteiro de um video
[A] Ajustar
[0] Voltar ao menu
```

---

## [7] CADASTRAR PRODUTO

### Objetivo
Entrar na Wiapy via dev-browser, criar o produto do zero, configurar checkout, order bump, upsell, entregavel, capa, e integrar pixel do Meta Ads + Utmify. Tudo automatizado — o aluno so confirma.

### Pre-requisito
- Conta na Wiapy (wiapy.com) — o aluno precisa estar logado no Chrome
- Produto definido no passo [3] (nome, preco, entregavel, bonus, order bump, upsell)
- Entregavel gerado no passo [4] (o produto digital pronto)
- Pagina de vendas gerada no passo [5] (link do checkout vai apontar pra ca)
- Pixel do Meta Ads (ID) e Utmify (ID) — se ja tiver

### Fluxo

Ao selecionar [7], mostrar:

```
CADASTRAR PRODUTO
==================

Vou entrar na Wiapy pelo seu navegador e criar tudo automaticamente.

Pre-checklist:
  [x] Voce esta logado na Wiapy no Chrome? (wiapy.com)
  [ ] Tem o nome e preco do produto?
  [ ] Tem imagem de capa? (caminho do arquivo ou vai gerar?)
  [ ] Tem o entregavel pronto? (PDF, link, area de membros)

  [1] Tudo certo — comecar
  [2] Preciso configurar algo primeiro

Qual opcao?
```

Se [2]:
```
O que falta?
  [A] Nao tenho conta na Wiapy — criar agora
  [B] Nao tenho capa — gerar com IA
  [C] Nao tenho entregavel pronto
  [0] Voltar ao menu
```

Se [A]: abrir wiapy.com via dev-browser e guiar o cadastro.
Se [B]: gerar prompt de capa pro ChatGPT ou usar Higgsfield generate_image.
Se [C]: sugerir formatos de entregavel rapido (PDF no Canva, Google Drive, etc).

---

### Passo 1 — Coletar dados do produto

Se tem produto definido do [3], puxar automaticamente:
```
Dados do produto (do passo [3]):
  Nome: [nome]
  Preco principal: R$[XX]
  Descricao: [descricao curta]
  Entregavel: [tipo + link/arquivo]
  Order bump: [nome] — R$[XX]
  Upsell: [nome] — R$[XX]

Tudo certo? (s/n)
> [resposta]
```

Se nao tem dados do [3], perguntar um por um:

```
DADOS DO PRODUTO
=================

Nome do produto:
> [nome]

Preco principal (R$):
> [preco]

Descricao curta (aparece no checkout):
> [descricao]

Tipo de entregavel:
  [1] PDF / arquivo (vou precisar do link ou caminho)
  [2] Area de membros (link de acesso)
  [3] Link externo (Google Drive, Notion, etc)
> [opcao]

Link ou caminho do entregavel:
> [link/caminho]

Imagem de capa:
  [1] Ja tenho (caminho do arquivo)
  [2] Gerar prompt pra criar no ChatGPT
> [opcao]

Se [1]:
  Caminho da capa:
  > [caminho]

Se [2]:
  Gerando prompt de capa...
  [mostra prompt otimizado pra gerar capa no ChatGPT — mockup do produto, estilo profissional]
  Cole no ChatGPT, salve a imagem e me diz o caminho:
  > [caminho]
```

---

### Passo 2 — Order bump

```
CONFIGURAR ORDER BUMP
======================

O order bump e uma oferta extra que aparece no checkout.
O comprador marca um checkbox e paga junto.

Quer configurar order bump? (s/n)
> [resposta]
```

Se sim:
```
Nome do bump:
> [nome]

Preco (R$):
> [preco]

Descricao curta (1-2 linhas — convence o cara a marcar):
> [descricao]

Entregavel do bump:
> [link/caminho]

Capa do bump (caminho ou pular):
> [caminho ou Enter]
```

---

### Passo 3 — Upsell

```
CONFIGURAR UPSELL
==================

O upsell e uma oferta que aparece DEPOIS da compra.
O cara ja pagou e ve uma oferta especial antes de receber o produto.

Quer configurar upsell? (s/n)
> [resposta]
```

Se sim:
```
Nome do upsell:
> [nome]

Preco (R$):
> [preco]

Descricao:
> [descricao]

Entregavel:
> [link/caminho]
```

---

### Passo 4 — Resumo e confirmacao

```
RESUMO DO PRODUTO
==================

PRODUTO PRINCIPAL:
  Nome: [nome]
  Preco: R$[preco]
  Descricao: [descricao]
  Entregavel: [tipo + link]
  Capa: [arquivo]

ORDER BUMP:
  [nome] — R$[preco]
  [descricao]

UPSELL:
  [nome] — R$[preco]

============================================

Confirma? Vou entrar na Wiapy e criar tudo.

  [1] Sim — criar agora
  [2] Ajustar algo
  [0] Cancelar

Qual opcao?
```

---

### Passo 6 — Criar na Wiapy via dev-browser

```
Abrindo Wiapy no navegador...
```

Usar dev-browser pra executar o fluxo na Wiapy. Cada acao mostra o progresso:

```
CRIANDO PRODUTO NA WIAPY
==========================

[1/8] Abrindo wiapy.com...                    ✓
[2/8] Navegando pra Produtos > Criar...       ✓
[3/8] Preenchendo dados do produto...          ✓
      Nome: [nome]
      Preco: R$[preco]
      Descricao: [descricao]
[4/8] Fazendo upload da capa...                ✓
[5/8] Configurando entregavel...               ✓
      Tipo: [tipo]
      Link: [link]
[6/8] Configurando order bump...               ✓
      [nome] — R$[preco]
[7/8] Configurando upsell...                   ✓
      [nome] — R$[preco]
[8/8] Salvando produto...                      ✓

Produto criado!
```

**Navegacao na Wiapy (passo a passo do dev-browser):**

1. Ir pra `wiapy.com` (verificar se ta logado)
2. Menu lateral > **Produtos** > botao de criar novo produto
3. Preencher:
   - Nome do produto
   - Descricao
   - Preco
   - Upload de capa (imagem)
4. Configurar entrega:
   - Tipo de entrega (arquivo/link/area de membros)
   - Link ou upload do entregavel
5. Ir em **Checkout** > configurar o checkout do produto
6. Adicionar order bump (se configurado):
   - Nome, preco, descricao, entregavel do bump
7. Adicionar upsell (se configurado)
8. Salvar tudo

Se algum passo falhar, informar e perguntar se quer tentar de novo ou fazer manual:
```
Erro no passo [X]: [descricao do erro]

  [1] Tentar de novo
  [2] Pular e fazer manualmente
  [0] Cancelar

Qual opcao?
```

---

### Passo 7 — Configurar webhook (opcional)

```
WEBHOOK (opcional)
===================

Quer configurar webhook pra receber eventos de pagamento?
Util pra: email automatico, dar acesso, remarketing, etc.

  [1] Sim — configurar
  [2] Nao — pular

Qual opcao?
```

Se [1]:
```
URL do webhook (pra onde a Wiapy manda os eventos):
> [url]

Token de autenticacao (opcional):
> [token ou Enter]

Quais eventos ativar?
  [x] Pagamento aprovado
  [x] Pagamento estornado
  [x] Chargeback
  [ ] Pagamento pendente
  [ ] Cartao recusado
  [ ] Carrinho abandonado

Ajusta os marcados e confirma (s/n):
> [resposta]
```

Via dev-browser:
1. Ir em Integracoes > Configurar Webhook
2. Selecionar o checkout do produto criado
3. Colar URL do webhook
4. Colar token (se tiver)
5. Marcar os eventos
6. Salvar

---

### Passo 9 — Resultado final

```
PRODUTO PRONTO!
================

Produto: [nome]
Preco: R$[preco]
Order bump: [nome] — R$[preco]
Upsell: [nome] — R$[preco]

Link do checkout:
  [URL do checkout na Wiapy — copiar da pagina]

Webhook: [✓ configurado / ✗ nao configurado]

============================================

PROXIMO PASSO:
  1. Cole o link do checkout na sua pagina de vendas:
     Substitua #checkout-premium → [link real]
     Substitua #checkout-basico → [link real do plano basico, se tiver]

  2. Rode [8] Meta Ads > Criar pixel (se ainda nao tem)
  3. Rode [8] Meta Ads > Criar campanha (subir criativos + configurar tudo)
  4. Rode [8] Meta Ads > Otimizar quando tiver trafego rodando

============================================

[T] Testar checkout (abre no navegador)
[L] Copiar link do checkout
[0] Voltar ao menu
```

Se [T]: abrir o link do checkout via dev-browser pra conferir se ta tudo certo.

---

## [8] META ADS

### Objetivo
Criar pixel, subir campanhas e otimizar via Meta Marketing API. Sem Advantage+, campanha de vendas manual, config baseada no modelo validado do @adsborba.

### Fluxo

Ao selecionar [8], mostrar:

```
META ADS
=========

  [1] Criar pixel
  [2] Criar campanha
  [3] Otimizar campanhas

Digite o numero:
```

---

### [1] CRIAR PIXEL

```
CRIAR PIXEL
=============

Vou criar um pixel no Meta Ads pra rastrear conversoes do seu produto.

Nome do pixel (ex: "Pixel OAB", "Pixel Serralheiro"):
> [nome]

Criando pixel...
```

Usar Meta Marketing API:
1. `ads_get_ad_accounts` — listar contas de anuncio
2. Perguntar qual conta usar (se tiver mais de uma)
3. Criar pixel na conta selecionada (ou via dev-browser se MCP nao tiver endpoint direto)

```
Pixel criado!

  Nome: [nome]
  ID: [pixel_id]

Proximo passo:
  - Cole o ID no seu site (pagina de vendas + checkout)
  - Ou rode [5] Cadastrar produto pra configurar na Wiapy

[0] Voltar ao menu
```

---

### [2] CRIAR CAMPANHA

```
CRIAR CAMPANHA
===============

Vou criar uma campanha de vendas no Meta Ads.
Preciso de algumas infos:
```

#### Passo 1 — Coletar dados

```
DADOS DA CAMPANHA
==================

Nome da campanha:
> [nome — ex: "CTV 4 V2", "Serralheiro V1"]

Qual produto? (preco do front):
> R$ [preco — ex: 19.90]

URL da pagina de vendas:
> [url — ex: https://oabquinhentos.smartquiz.shop/]

Link de exibicao (aparece no anuncio):
> [dominio curto — ex: oabquinhentos.com.br]

Orcamento diario (R$):
> [valor — padrao sugerido: mesmo valor do produto]

Pixel (nome ou ID):
> [nome/id — ex: "Pixel OAB"]

Pagina do Facebook (pra vincular o anuncio):
> [nome da pagina]
```

Se tem criativos do passo [6]:
```
Usar criativos gerados no passo [6]? (s/n)
> [resposta]
```

Se nao, pedir:
```
Caminho dos criativos (video ou imagem):
> [caminho ou lista de arquivos]

Texto principal do anuncio:
> [copy]

Titulo do anuncio:
> [titulo curto]

Descricao (opcional):
> [ex: "⭐⭐⭐⭐⭐ 4.9/5"]
```

#### Passo 2 — Perguntar estrutura

```
ESTRUTURA DA CAMPANHA
======================

Quantos conjuntos de anuncio?
  [1] 1 conjunto, 1 anuncio (simples — testar 1 criativo)
  [2] 1 conjunto, varios anuncios (testar criativos no mesmo publico)
  [3] Varios conjuntos (testar publicos diferentes)
  [4] Personalizado

Qual opcao?
> [resposta]
```

Se [3] ou [4], perguntar detalhes de cada conjunto (publico, interesses, etc).

#### Passo 3 — Resumo e confirmacao

```
RESUMO DA CAMPANHA
====================

CAMPANHA:
  Nome: [nome]
  Objetivo: Vendas
  Advantage+: DESATIVADO
  Tipo de compra: Leilao
  Orcamento: R$[valor]/dia (CBO — distribuido pela campanha)
  Estrategia de lance: Volume mais alto

CONJUNTO DE ANUNCIOS:
  Nome: [nome do conjunto]
  Conversao: Site
  Evento: Comprar
  Pixel: [nome] (ID: [id])
  Meta de desempenho: Maximizar conversoes
  Meta de custo: Nenhum
  Inicio: [data de hoje]
  Termino: Sem data
  Publico: Brasil, amplo (Advantage+ publico ativado)
  Posicionamentos: MANUAL
    Plataformas: Facebook + Instagram
    Feeds: ativado
    Stories/Status/Reels: ativado
    In-stream/Pesquisa/Apps: desativado

ANUNCIO:
  Nome: [nome]
  Pagina: [pagina do Facebook]
  Formato: Imagem ou video unico
  Midia: [arquivo do criativo]
  Destino: Site → [url]
  Link de exibicao: [dominio]
  Texto principal: "[copy]"
  Titulo: "[titulo]"
  Descricao: "[descricao]"
  CTA: Saiba mais
  Aprimoramentos Advantage+: DESATIVADOS
  Rastreamento: Pixel [nome]
  UTM: utm_source=FB&utm_campaign={{campaign.name}}&utm_content={{ad.name}}

============================================

Confirma? (s/n)
```

#### Passo 4 — Criar via Meta Marketing API

Pre-requisito: token do usuario com permissao ads_management salvo no config.

Usar curl via Bash na ordem:

1. **Listar contas:** GET `/me/adaccounts?fields=id,name,account_status,currency`
2. **Criar campanha:** POST `/act_{id}/campaigns` com name, objective=OUTCOME_SALES, status=PAUSED, buying_type=AUCTION, bid_strategy=LOWEST_COST_WITHOUT_CAP, daily_budget=[ticket em centavos], special_ad_categories=[]
3. **Criar conjunto:** POST `/act_{id}/adsets` com campaign_id, optimization_goal=OFFSITE_CONVERSIONS, billing_event=IMPRESSIONS, promoted_object={pixel_id, PURCHASE}, targeting={BR, 18-65, pt, advantage_audience:1, mobile, FB+IG todos posicionamentos}, attribution_spec=[7d click, 1d view, 1d engaged]
4. **Criar anuncio:** POST `/act_{id}/ads` com adset_id, creative={creative_id}, url_tags=[UTMs com IDs]

Campanha criada PAUSADA. Perguntar se quer ativar.
Pra ativar: POST `/{campaign_id}` com status=ACTIVE

Mostrar progresso:

```
CRIANDO CAMPANHA
=================

[1/5] Verificando conta de anuncios...         ✓
[2/5] Criando campanha "[nome]"...              ✓
[3/5] Criando conjunto de anuncios...           ✓
[4/5] Fazendo upload do criativo...             ✓
[5/5] Criando anuncio...                        ✓

Campanha criada!

  Campanha: [nome] (ID: [id])
  Conjunto: [nome] (ID: [id])
  Anuncio: [nome] (ID: [id])
  Status: Pausada (publicar quando quiser)

============================================

[P] Publicar agora (ativar campanha)
[A] Adicionar mais anuncios nessa campanha
[0] Voltar ao menu
```

Se [P]: ativar via POST `/{campaign_id}` com status=ACTIVE.

**Config padrao da campanha (baseado na operacao real @adsborba):**

CAMPANHA:
- Objetivo: Vendas (OUTCOME_SALES)
- Tipo compra: AUCTION
- Orcamento: CBO diario = ticket medio do produto (em centavos)
- Lance: Volume mais alto (LOWEST_COST_WITHOUT_CAP)
- Advantage+ campanha: DESATIVADO (GUIDED_CREATION)
- Categorias especiais: nenhuma
- Budget rebalance: OFF

CONJUNTO:
- Otimizacao: OFFSITE_CONVERSIONS
- Evento: PURCHASE (pixel do cara)
- Cobranca: IMPRESSIONS
- Publico: Brasil, 18-65, todos generos, portugues
- Advantage+ PUBLICO: ATIVADO (advantage_audience: 1)
- Device: MOBILE only
- Posicionamentos Facebook: feed, reels, profile_feed, notification, marketplace, story
- Posicionamentos Instagram: stream, story, reels, explore_home, profile_feed
- Atribuicao: 7d click, 1d view, 1d engaged video
- Sem data de termino

ANUNCIO:
- Formato: video ou imagem unico
- CTA: LEARN_MORE (Saiba mais)
- Advantage+ criativo: DESATIVADO
- UTMs: utm_source=FB&utm_campaign={{campaign.name}}|{{campaign.id}}&utm_medium={{adset.name}}|{{adset.id}}&utm_content={{ad.name}}|{{ad.id}}&utm_term={{placement}}
- Vincular pagina FB + conta IG do cara

**Estrutura: CBO Triplo 1** = 1 campanha, 1 conjunto, 1 anuncio. Cada criativo (CTV) vira uma campanha separada.

---

### [3] OTIMIZAR CAMPANHAS

#### Metodo de otimizacao — @adsborba

A otimizacao segue um metodo especifico. Estrutura de teste:

**Setup inicial (feito no [2] Criar campanha):**
- 7 CTVs (4 video + 3 imagem, gerados no passo [6]), cada um com 2 campanhas (original + copia) = 14 campanhas
- Orcamento de cada campanha = ticket do produto front (ex: produto R$29,90 = orcamento R$29,90/dia)
- CPA ideal = metade do ticket (ex: produto R$29,90 → CPA ideal R$15,00)

**Regras de otimizacao:**
1. **MATAR:** campanha gastou mais que o CPA ideal (metade do ticket) com 0 vendas → DESATIVAR
2. **ESCALAR +30%:** campanha vendeu → aumentar orcamento 30%
3. **DOBRAR:** campanha com 3+ vendas, ROI alto, 2h+ desde ultima otimizacao → sugerir dobrar orcamento
4. **SEMPRE perguntar antes de executar qualquer acao**
5. Otimizar a cada ~2 horas

#### Fluxo

```
OTIMIZAR CAMPANHAS
===================

Como quer fornecer os dados?
  [A] Puxar do Meta Ads automaticamente (via MCP)
  [B] Informar manualmente

Qual opcao?
```

#### Passo 1 — Puxar dados

**Opcao A — Via MCP:**

```
> A

Qual o ticket do produto front (R$)?
> [preco — ex: 29.90]

Buscando campanhas ativas...
```

Usar MCP:
1. GET `/act_{id}/campaigns?fields=id,name,status,daily_budget` — listar campanhas
2. GET `/act_{id}/insights?level=campaign&date_preset=today` — metricas de hoje

**Opcao B — Manual:**

```
> B

Ticket do produto front (R$):
> [preco]

Me passa as campanhas ativas.
Formato: Nome | Gasto | Vendas

> CTV 1 | R$10 | 0
> CTV 1 (Copia) | R$15 | 0
> CTV 2 | R$10 | 1
> CTV 2 (Copia) | R$15 | 0
> CTV 3 | R$10 | 1
> CTV 3 (Copia) | R$5 | 0
> pronto
```

#### Passo 2 — Dashboard

```
OTIMIZACAO — [horario atual]
==============================
Ticket: R$[preco] | CPA ideal: R$[metade do preco]

CAMPANHA             | Gasto   | Vendas | Lucro   | Status
---------------------|---------|--------|---------|----------
CTV 1                | R$10    | 0      | -R$10   | rodando
CTV 1 (Copia)        | R$15    | 0      | -R$15   | rodando
CTV 2                | R$10    | 1      | +R$19,90| rodando
CTV 2 (Copia)        | R$15    | 0      | -R$15   | rodando
CTV 3                | R$10    | 1      | +R$19,90| rodando
CTV 3 (Copia)        | R$5     | 0      | -R$5    | rodando

Total gasto: R$65 | Total vendas: 2 | Lucro bruto: +R$24,80

============================================
```

#### Passo 3 — Recomendacoes

Aplicar as regras automaticamente e mostrar:

```
ACOES RECOMENDADAS
===================

  1. MATAR  — CTV 1 (Copia)
     Motivo: gastou R$15 (> CPA ideal R$15) com 0 vendas

  2. MATAR  — CTV 2 (Copia)
     Motivo: gastou R$15 (> CPA ideal R$15) com 0 vendas

  3. ESCALAR +30% — CTV 2
     Motivo: 1 venda, lucro R$19,90
     Orcamento: R$29,90 → R$38,87

  4. ESCALAR +30% — CTV 3
     Motivo: 1 venda, lucro R$19,90
     Orcamento: R$29,90 → R$38,87

  5. MANTER — CTV 1
     Motivo: gastou R$10, ainda nao bateu CPA ideal (R$15)

  6. MANTER — CTV 3 (Copia)
     Motivo: gastou R$5, ainda nao bateu CPA ideal (R$15)

============================================

Executar? (confirmo cada acao individualmente)
  [1] Executar acoes recomendadas
  [2] Escolher quais executar
  [3] So ver, nao mexer
  [0] Voltar ao menu
```

#### Passo 4 — Executar com confirmacao

SEMPRE perguntar antes de cada acao:

```
Executando acoes...

  [1] Matar CTV 1 (Copia)? (s/n)
  > s
  Desativando... ✓

  [2] Matar CTV 2 (Copia)? (s/n)
  > s
  Desativando... ✓

  [3] Escalar CTV 2: R$29,90 → R$38,87? (s/n)
  > s
  Aumentando orcamento... ✓

  [4] Escalar CTV 3: R$29,90 → R$38,87? (s/n)
  > s
  Aumentando orcamento... ✓

Acoes executadas!

Campanhas restantes:
  CTV 1        — R$29,90/dia — monitorando
  CTV 2        — R$38,87/dia — escalando
  CTV 3        — R$38,87/dia — escalando
  CTV 3 (Copia) — R$29,90/dia — monitorando

Proxima otimizacao: daqui 2 horas
Rode /automatico > [8] > [3] de novo.

[0] Voltar ao menu
```

#### Otimizacao subsequente (2h depois)

Na proxima rodada, se uma campanha ja tem 3+ vendas com ROI alto:

```
ACOES RECOMENDADAS
===================

  1. DOBRAR — CTV 2
     Motivo: 3 vendas, ROI alto, 2h desde ultima escalada
     Orcamento: R$38,87 → R$77,74
     (Alternativa conservadora: +30% → R$50,53)

Qual prefere?
  [1] Dobrar (R$77,74)
  [2] +30% conservador (R$50,53)
  [3] Valor personalizado
  [0] Nao mexer
```

#### Regras fixas de otimizacao

- **CPA ideal = metade do ticket** (produto R$29,90 → CPA ideal R$15)
- **Matar:** gastou > CPA ideal com 0 vendas
- **Escalar +30%:** vendeu (qualquer quantidade)
- **Dobrar:** 3+ vendas + ROI alto + 2h+ desde ultima otimizacao
- **NUNCA executar sem perguntar** — sempre confirma cada acao
- **Frequencia:** a cada ~2 horas
- **Lucro = (vendas x ticket) - gasto**

---

## [9] CONFIGURACOES

### Objetivo
Setup inicial + diagnostico continuo. Na primeira vez, instala tudo que a skill precisa. Nas vezes seguintes, verifica se ta tudo funcionando, mostra status de cada dependencia, e exibe metricas gerais da operacao.

### Fluxo

Ao selecionar [9], mostrar:

```
CONFIGURACOES
==============

  [1] Diagnostico completo (verificar tudo)
  [2] Instalar/configurar dependencia especifica
  [3] Metricas da operacao
  [4] Resetar configuracoes

Digite o numero:
```

---

### [1] DIAGNOSTICO COMPLETO

Roda automaticamente na primeira vez que o usuario abre a skill. Nas vezes seguintes, so quando pedir.

```
DIAGNOSTICO DO SISTEMA
========================
Verificando dependencias...
```

Verificar cada item e mostrar status:

```
DEPENDENCIAS
==============

FERRAMENTAS:
  Whisper (transcrever videos)      [?] verificando...
  dev-browser (automacao browser)   [?] verificando...
  video-downloader (baixar videos)  [?] verificando...
  CapCut (edicao de video)          [?] verificando...

MCPs (conectores):
  Meta Ads                          [?] verificando...
  Higgsfield                        [?] verificando...
  Utmify                            [?] verificando...

APIs:
  Apify (scraper Biblioteca)        [?] verificando...

CONTAS:
  Wiapy (gateway)                   [?] verificando...
  Meta Business (anuncios)          [?] verificando...
  RatoAds (mineracao premium)       [?] verificando...
```

**Como verificar cada item:**

1. **Whisper:** rodar `which whisper` ou `whisper --help` no terminal
2. **dev-browser:** verificar se o script existe em `~/.claude/skills/dev-browser/`
3. **video-downloader:** verificar se a skill existe em `~/.claude/skills/video-downloader/`
4. **CapCut:** nao da pra verificar automaticamente — perguntar pro usuario se tem instalado
5. **Meta Marketing API:** tentar chamar `ads_get_ad_accounts` — se retornar dados, ta conectado
6. **MCP Higgsfield:** tentar chamar `balance` — se retornar dados, ta conectado
7. **MCP Utmify:** tentar chamar `get_dashboards` — se retornar dados, ta conectado
8. **Apify:** verificar se tem APIFY_TOKEN no env ou no config-automatico.json
9. **Wiapy:** verificar se consegue acessar wiapy.com via dev-browser (logado?)
10. **Meta Business:** verificar via Meta Marketing API se tem ad account
11. **RatoAds:** verificar se tem credenciais no config-automatico.json

**Resultado:**

```
DIAGNOSTICO COMPLETO
=====================

FERRAMENTAS:
  Whisper                           [OK] v20231117, modelo small
  dev-browser                       [OK] instalado
  video-downloader                  [OK] instalado
  CapCut                            [??] nao verificavel — confirme manualmente

MCPs:
  Meta Ads                          [OK] conta: [nome] (ID: [id])
  Higgsfield                        [OK] creditos: [X]
  Utmify                            [OK] dashboards: [X]

APIs:
  Apify                             [FALTA] token nao configurado

CONTAS:
  Wiapy                             [OK] logado como [email]
  Meta Business                     [OK] [X] contas de anuncio
  RatoAds                           [FALTA] credenciais nao configuradas

============================================

RESUMO: 8/11 OK | 2 faltando | 1 nao verificavel

ITENS FALTANDO:
  1. Apify — precisa do token pra scrapar Biblioteca de Anuncios
  2. RatoAds — precisa de email/senha pra mineracao premium

[I] Instalar/configurar itens faltando agora
[0] Voltar ao menu
```

Se [I], ir pro fluxo de instalacao de cada item faltando.

---

### [2] INSTALAR/CONFIGURAR DEPENDENCIA

```
INSTALAR DEPENDENCIA
=====================

Qual quer configurar?
  [1] Whisper
  [2] dev-browser
  [3] video-downloader
  [4] Meta Marketing API
  [5] MCP Higgsfield
  [6] MCP Utmify
  [7] Apify
  [8] Wiapy (login)
  [9] RatoAds (credenciais)

Digite o numero:
```

#### Instalacao de cada item:

**[1] Whisper:**
```
Instalando Whisper...
```
Rodar: `pip install openai-whisper`
Testar: `whisper --help`
Se der erro de ffmpeg: `pip install ffmpeg-python` ou instruir instalacao manual.

**[2] dev-browser:**
```
O dev-browser conecta no seu Chrome pra automatizar sites.

Passo 1: Abra o Chrome com debug mode:
  Windows: chrome.exe --remote-debugging-port=9222
  Mac: /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

Passo 2: Confirme que abriu (s/n):
> [resposta]
```

Testar conexao via dev-browser skill.

**[3] video-downloader:**
```
Instalando yt-dlp (baixa videos de qualquer plataforma)...
```
Rodar: `pip install yt-dlp`
Testar: `yt-dlp --version`

**[4] Meta Marketing API:**
```
O Meta Marketing API conecta na sua conta do Meta Business.

Se voce ja tem ele configurado no Claude Code, vou testar a conexao.
Se nao, precisa adicionar no settings do Claude Code.

Testando conexao...
```
Testar: curl GET `/me/adaccounts` com token do usuario.
Se falhar, instruir como criar App no Meta Developers e gerar token.

**[5] MCP Higgsfield:**
```
O Higgsfield gera videos e imagens com IA (expert, avatares).

Testando conexao...
```
Testar: chamar `balance`.
Se falhar, instruir configuracao.

**[6] MCP Utmify:**
```
O Utmify rastreia performance das suas ofertas.

Testando conexao...
```
Testar: chamar `get_dashboards`.

**[7] Apify:**
```
O Apify scrapa a Biblioteca de Anuncios do Meta automaticamente.

Voce precisa de uma conta no Apify (apify.com).
Plano free tem creditos suficientes pra comecar.

Ja tem conta? (s/n)
> [resposta]

Se sim:
  Cole seu API token (encontra em apify.com > Settings > Integrations):
  > [token]

Salvando em config-automatico.json...
Testando conexao...
```

**[8] Wiapy:**
```
Preciso verificar se voce ta logado na Wiapy no Chrome.

Abrindo wiapy.com...
```
Usar dev-browser pra checar. Se nao ta logado, guiar login.

**[9] RatoAds:**
```
Conectar sua conta do RatoAds pra mineracao premium.

  [1] Ativar trial do curso (3/3/3 por 30 dias)
  [2] Ja tenho conta — configurar login

Qual opcao?
```
Mesmo fluxo do [1] Minerar > RatoAds.

---

### [3] METRICAS DA OPERACAO

Puxa dados de todas as fontes conectadas e mostra um dashboard geral.

```
METRICAS DA OPERACAO
=====================
Puxando dados...
```

**Dados que puxa:**

1. **Meta Ads (MCP):** campanhas ativas, gasto total, vendas, ROAS, CPA
2. **Utmify (MCP):** faturamento, conversoes, taxa de conversao
3. **Wiapy:** produtos ativos, vendas recentes (se tiver API, senao pula)
4. **RatoAds:** creditos restantes, mineracoes usadas

```
DASHBOARD GERAL
================
Data: [data atual]

META ADS:
  Campanhas ativas: [X]
  Gasto hoje: R$[XX]
  Gasto mes: R$[XX]
  Vendas hoje: [X]
  Vendas mes: [X]
  ROAS hoje: [X]
  ROAS mes: [X]
  CPA medio: R$[XX]
  Melhor campanha: "[nome]" (ROAS [X])
  Pior campanha: "[nome]" (ROAS [X])

UTMIFY:
  Faturamento hoje: R$[XX]
  Faturamento mes: R$[XX]
  Taxa de conversao: [X]%
  Ticket medio: R$[XX]
  Top produto: "[nome]" — R$[XX]

RATOADS:
  Plano: [plano]
  Mineracoes restantes: [X]/[max]
  Analises restantes: [X]/[max]
  Slots radar: [X]/[max]

SAUDE DA OPERACAO:
  [status geral — baseado nos numeros]

  Se ROAS > 2: "Operacao saudavel. Escala mais."
  Se ROAS 1-2: "No break-even. Otimiza criativos e mata campanhas ruins."
  Se ROAS < 1: "Prejuizo. Pausa tudo, revisa criativos e funil."

============================================

[O] Ir pra otimizacao (Meta Ads > Otimizar)
[D] Detalhar metricas de uma campanha
[0] Voltar ao menu
```

Se [D], pedir nome da campanha e mostrar breakdown completo (gasto por dia, vendas por dia, tendencia).

---

### [4] RESETAR CONFIGURACOES

```
RESETAR
========

O que quer resetar?
  [1] Credenciais do RatoAds
  [2] Token do Apify
  [3] Tudo (apagar config-automatico.json)

Qual opcao?
```

Se [3]:
```
Isso vai apagar todas as credenciais salvas.
Voce vai precisar configurar tudo de novo.

Tem certeza? (s/n)
> [resposta]
```

Se sim, deletar `./config-automatico.json`.

---

### PRIMEIRA EXECUCAO (auto-detectar)

Quando o usuario roda `/automatico` pela primeira vez, antes de mostrar o menu principal, verificar se `./config-automatico.json` existe.

Se NAO existe (primeira vez):

```
============================================
   LOW TICKET AUTOMATIZADO v1.0
   by @adsborba
============================================

Primeira vez aqui! Vou rodar o setup pra
garantir que ta tudo funcionando.

Rodando diagnostico...
```

Rodar automaticamente o fluxo do [1] Setup & Diagnostico.
Se tiver itens faltando, oferecer instalar.
Depois de tudo OK, criar `./config-automatico.json` e mostrar o menu principal.

---

## Regras gerais

1. Sempre manter o formato visual com `===` e tabelas pra parecer um software
2. Nunca inventar dados — so mostrar o que realmente encontrou no scraping
3. Se uma gateway nao retornar resultados, informar e seguir pra proxima
4. Se o scraping falhar em alguma gateway, tentar via WebSearch como fallback
5. Manter tom direto e objetivo — sem explicacoes longas durante a execucao
6. Sempre oferecer opcao de voltar ao menu
7. Salvar resultados de mineracao em `./mineracao/[data]-resultados.md` pra consulta futura
