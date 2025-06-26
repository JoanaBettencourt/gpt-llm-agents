import requests
import json
from project.agent_logic import construir_contexto_agente
from project.config_manager import load_config

def enviar_para_ollama_stream(system_prompt: str, modelo: str, ollama_url: str, dados: dict) -> str:
    """Envia os dados para o modelo Ollama, com base na configuração do agente."""
    
    # Preparar prompt do utilizador
    resumo_dados = json.dumps(dados, indent=2, ensure_ascii=False)
    user_prompt = (
        "Com base nas instruções acima, analisa os seguintes dados do Moodle.\n"
        "Devolve a tua resposta num destes formatos:\n"
        "- <ação>: descrição da ação principal\n"
        "- <mensagem>: conteúdo explicativo (opcional)\n"
        "Exemplo:\n"
        "ação: Publicar no fórum alerta para entrega do trabalho .\n"
        "mensagem: X estudantes ainda não entregram o trabalho 2. Recomenda-se publicar no fórum um alerta.\n\n"
        "Segue os dados:\n"
        f"{resumo_dados}"
    )

    payload = {
        "model": modelo,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": True
    }

    resposta_total = ""
    try:
        with requests.post(f"{ollama_url}/api/chat", json=payload, stream=True) as resposta:
            resposta.raise_for_status()
            for linha in resposta.iter_lines():
                if linha:
                    parte = json.loads(linha.decode("utf-8"))["message"]["content"]
                    resposta_total += parte
        return resposta_total

    except Exception as e:
        return f"Erro ao comunicar com o Ollama: {e}"
