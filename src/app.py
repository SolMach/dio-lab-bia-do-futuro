# import json
# import pandas as pd
# import requests
# import streamlit as st

# #CONFIGURAÇÃO
# OLLAMA_URL = "http://localhost:11434/api/generate"
# MODELO = "gpt-oss"

# # DADOS
# perfil = json.load(open('./data/perfil_investidor.json'))
# transacoes = pd.read_csv('./data/transacoes.csv')
# historico = pd.read_csv('./data/historico_atendimento.csv')
# produtos = json.load(open('./data/produtos_financeiros.json'))

# # CONTEXTO
# contexto = f"""
# CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
# OBJETIVO: {perfil['objetivo_principal']}
# PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

# TRANSAÇÕES RECENTES: 
# {transacoes.to_string(index=False)}

# ATENDIMENTOS ANTERIORES: 
# {historico.to_string(index=False)}

# PRODUTOS DISPONÍVEIS:
# {json.dumps(produtos, indent=2, ensure_ascii=False)}
# """

# #SYSTEM PROMPT
# SYSTEM_PROMPT = """Você é o Credion, um educador financeiro amigável e didático.

# OBJETIVO:
# Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos.

# REGRAS:
# - NUNCA recomende investimentos específicos, apenas explique como funcionam;
# - JAMAIS responda a perguntas fora do tema ensino de finanças pessoais.
#   Quando ocorrer, responda lembrando o seu papel de educador financeiro;
# - Use os dados fornecidos para dar exemplos personalizados;
# - Linguagem simples, como se explicasse para um amigo;
# - Se não souber algo, admita: "Não tenho essa informação, mas posso explicar...";
# - Sempre pergunte se o cliente entendeu;
# - Responda de forma sucinta e direta, com no máximo 3 parágrafos.
# """

# #CHAMAR OLLAMA
# def perguntar(msg):
#     prompt = f"""
#     {SYSTEM_PROMPT}

#     CONTEXTO DO CLIENTE:
#     {contexto}

#     Pergunta: {msg}
# """
    
#     r = requests.post(OLLAMA_URL, json= {"model": MODELO, "prompt": prompt, "stream": False})
#     return r.json()['response']

# # INTERFACE
# st.title("Credion, seu educador financeiro.")

# if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
#     st.chat_message("user").write(pergunta)
#     with st.spinner("..."):
#         st.chat_message("assistant").write(perguntar(pergunta))

import json
import pandas as pd
import requests
import streamlit as st
import os

# CONFIGURAÇÃO
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss:20b"  # troque se quiser, mas precisa existir no Ollama

# FUNÇÃO PRA GARANTIR CAMINHO CERTO
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def carregar_json(caminho):
    with open(os.path.join(BASE_DIR, caminho), encoding="utf-8") as f:
        return json.load(f)

def carregar_csv(caminho):
    return pd.read_csv(os.path.join(BASE_DIR, caminho))

# DADOS
perfil = carregar_json("data/perfil_investidor.json")
transacoes = carregar_csv("data/transacoes.csv")
historico = carregar_csv("data/historico_atendimento.csv")
produtos = carregar_json("data/produtos_financeiros.json")

# CONTEXTO
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES: 
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES: 
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# SYSTEM PROMPT
SYSTEM_PROMPT = """Você é o Credion, um educador financeiro amigável e didático.

OBJETIVO:
Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos.

REGRAS:
- NUNCA recomende investimentos específicos, apenas explique como funcionam;
- JAMAIS responda a perguntas fora do tema ensino de finanças pessoais.
  Quando ocorrer, responda lembrando o seu papel de educador financeiro;
- Use os dados fornecidos para dar exemplos personalizados;
- Linguagem simples, como se explicasse para um amigo;
- Se não souber algo, admita: "Não tenho essa informação, mas posso explicar...";
- Sempre pergunte se o cliente entendeu;
- Responda de forma sucinta e direta, com no máximo 3 parágrafos.
"""

# CHAMAR OLLAMA
def perguntar(msg):
    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO DO CLIENTE:
{contexto}

Pergunta: {msg}
"""

    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": MODELO, "prompt": prompt, "stream": False},
            timeout=60
        )
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão com o Ollama: {e}"

    # tenta converter resposta
    try:
        data = r.json()
    except:
        return f"Erro ao interpretar resposta da API:\n{r.text}"

    # erro HTTP
    if r.status_code != 200:
        return f"Erro HTTP {r.status_code}: {data}"

    # resposta esperada
    if "response" in data:
        return data["response"]

    # fallback
    return f"Resposta inesperada da API: {data}"

# INTERFACE
st.title("Credion, seu educador financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)

    with st.spinner("Pensando..."):
        resposta = perguntar(pergunta)

    st.chat_message("assistant").write(resposta)