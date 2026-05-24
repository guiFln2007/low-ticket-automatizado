# /automatico — Low Ticket Automatizado

Skill do Claude Code que automatiza toda a operacao de low ticket: mineracao, analise, funil, criativos, cadastro e Meta Ads.

by [@adsborba](https://instagram.com/adsborba)

## Instalacao

1. Tenha o [Claude Code](https://docs.anthropic.com/en/docs/claude-code) instalado
2. Rode no terminal:

```bash
claude mcp add-skill https://github.com/guiFln2007/low-ticket-automatizado
```

Ou manualmente:

```bash
# Copie o SKILL.md pra pasta de skills do Claude
mkdir -p ~/.claude/skills/automatico
curl -o ~/.claude/skills/automatico/SKILL.md https://raw.githubusercontent.com/guiFln2007/low-ticket-automatizado/main/SKILL.md
```

3. Abra o Claude Code e digite `/automatico`

## O que faz

- **Minerar ofertas escaladas** — Reclame Aqui, Biblioteca de Anuncios, RatoAds
- **Analisar & definir produto** — analise de concorrente + definicao da sua oferta
- **Gerar entregavel** — conteudo completo em PDF gerado por IA
- **Modelar funil** — copia e melhora pagina do concorrente
- **Gerar criativos** — roteiros, copies e variacoes automaticas
- **Cadastrar produto** — preenche gateway automaticamente
- **Meta Ads** — pixel, campanha, otimizacao e escala

## Requisitos

- Claude Code instalado e autenticado
- Node.js 18+
- Conta Anthropic ativa
