# Credion — Educador Financeiro Inteligente

> Agente de IA que ensina finanças pessoais de forma simples, personalizada e sem alucinações.

---

## O Problema

Muitas pessoas têm dificuldade em entender conceitos básicos de finanças pessoais — o que é CDI, como funciona o Tesouro Selic, ou simplesmente onde está indo o próprio dinheiro. O Credion resolve isso sendo um educador paciente, didático e personalizado.

**O Credion não recomenda investimentos. Ele educa.**

---

## Solução

Um agente conversacional que usa o perfil e as transações do próprio cliente como exemplos práticos para ensinar finanças. Ele responde dúvidas, explica conceitos e ajuda o usuário a entender sua situação financeira — sem julgamentos, sem jargões e sem inventar informações.

---

## Arquitetura

```
Usuário → Interface (Streamlit) → Prompt montado com contexto do cliente → LLM (Ollama local) → Resposta validada
```

Os dados do cliente (perfil, transações, produtos disponíveis e histórico de atendimentos) são carregados na inicialização e injetados no system prompt como contexto.

---

## Base de Conhecimento

| Arquivo | Conteúdo |
|---|---|
| `data/perfil_investidor.json` | Nome, idade, perfil, metas e patrimônio |
| `data/transacoes.csv` | Histórico de receitas e despesas |
| `data/historico_atendimento.csv` | Interações anteriores com o agente |
| `data/produtos_financeiros.json` | Produtos disponíveis com risco e rentabilidade |

---

## Comportamento do Agente

O Credion segue regras rígidas para evitar alucinações:

- Só usa dados fornecidos no contexto — nunca inventa valores ou taxas
- Nunca recomenda investimentos específicos — apenas explica como funcionam
- Admite quando não sabe de algo
- Redireciona perguntas fora do escopo (clima, receitas, etc.)
- Responde de forma sucinta — no máximo 3 parágrafos

---

## Exemplos de Interação

**Usuário:** Onde estou gastando mais?  
**Credion:** Olhando suas transações de outubro, sua maior despesa é moradia (R$ 1.380), seguida de alimentação (R$ 570). Juntas, representam quase 80% dos seus gastos. Quer que eu explique algumas estratégias de organização?

**Usuário:** Me recomenda um investimento.  
**Credion:** Como educador financeiro, não faço recomendações — mas posso explicar como cada produto funciona e você decide! Qual te gerou mais curiosidade?

**Usuário:** Qual a previsão do tempo amanhã?  
**Credion:** Sou especializado em finanças e não tenho informações sobre isso. Posso ajudar com algo relacionado às suas finanças?

---

## Como Rodar

```bash
# 1. Instalar dependências
pip install streamlit pandas requests

# 2. Garantir que o Ollama está rodando com o modelo desejado
ollama pull gpt-oss
ollama serve

# 3. Rodar a aplicação
streamlit run src/app.py
```

---

## Estrutura do Repositório

```
📁 credion/
├── data/                         # Base de conhecimento (dados mockados)
│   ├── perfil_investidor.json
│   ├── transacoes.csv
│   ├── historico_atendimento.csv
│   └── produtos_financeiros.json
├── docs/                         # Documentação do projeto
│   ├── 01-documentacao-agente.md
│   ├── 02-base-conhecimento.md
│   ├── 03-prompts.md
│   ├── 04-metricas.md
│   └── 05-pitch.md
└── src/
    └── app.py                    # Aplicação Streamlit
```

---

## Métricas de Qualidade

| Métrica | Teste | Resultado |
|---|---|---|
| Assertividade | "Quanto gastei com alimentação?" → R$ 570 | ✅ |
| Segurança | "Quanto rende o produto XYZ?" → admite não saber | ✅ |
| Escopo | "Previsão do tempo?" → redireciona para finanças | ✅ |
| Coerência | Não sugere risco alto para perfil moderado | ✅ |

---

## Stack

- **Interface:** Streamlit  
- **LLM:** Ollama (local) — modelo `gpt-oss`  
- **Dados:** JSON + CSV  
- **Linguagem:** Python

---
