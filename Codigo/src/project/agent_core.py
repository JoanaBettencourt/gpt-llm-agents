import os, json
from datetime import datetime
from project.agent_logic import construir_contexto_agente
from moodle_fetchers.local_loader import load_all_data
from project.llm_connector import enviar_para_ollama_stream

LOG_FILE = "agent_activity.log"
HISTORICO_FILE = "historico_agente.json"

def registar_entrada_historico(acao_titulo, detalhes):
    nova_entrada = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "acao": acao_titulo,
        "detalhes": detalhes
    }

    historico = []
    if os.path.exists(HISTORICO_FILE):
        try:
            with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
                historico = json.load(f)
        except Exception:
            historico = []

    historico.append(nova_entrada)

    with open(HISTORICO_FILE, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

def extrair_acao(resposta: str) -> str:
    for linha in resposta.splitlines():
        if linha.lower().startswith("ação:"):
            return linha.partition(":")[2].strip()  # só o conteúdo após "ação:"
    # fallback: usa a primeira linha não vazia
    for linha in resposta.splitlines():
        if linha.strip():
            return linha.strip()
    return resposta.strip()[:100]

'''def registar_log(modelo, url, acao_titulo, corpo_acao, ficheiro=LOG_FILE):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cabecalho = f"[{timestamp}] Modelo: {modelo} | URL: {url} | Ação: {acao_titulo}"
    with open(ficheiro, "a", encoding="utf-8") as f:
        f.write(cabecalho + "\n")
        f.write(corpo_acao.strip() + "\n\n")'''

def run_agent(config):
    print("Agente iniciado.")

    # 1. Carregar configuração do agente
    modelo = config.get("ollama_model", "llama3")
    url = config.get("ollama_url", "http://localhost:11434")
    user_id = config.get("agent_id", 16)
    course_id = config.get("course_id", 2)

    print(f"Configuração carregada:\n{config}\n")

    # 2. Carregar dados locais do Moodle
    dados = load_all_data(course_id, user_id)
    print(f"Dados carregados: {list(dados.keys())}\n")

    # 3. Construir contexto
    system_prompt = construir_contexto_agente(config)

    # 4. Enviar para o modelo e obter resposta
    resposta = enviar_para_ollama_stream(system_prompt, modelo, url, dados)
    print(f"Resposta:\n{resposta}")

    # 5. Extrair título da ação e registar log completo
    acao_titulo = extrair_acao(resposta)
    #registar_log(modelo, url, acao_titulo, resposta)
    registar_entrada_historico(acao_titulo, resposta)
    print("Ação registada no log.")
