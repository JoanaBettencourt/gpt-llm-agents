import json

# Função que usa os dados da configuração para construir o contexto do agente
def construir_contexto_agente(config):
    nome_agente = config.get("agent_name", "Agente")
    idioma = config.get("language", "pt")
    formato = []
    if config.get("formato_breve"): formato.append("breve")
    if config.get("formato_detalhado"): formato.append("detalhado")
    if config.get("formato_sugestoes"): formato.append("com sugestões")
    regras = config.get("pedagogical_rules", "")

    return f"O teu nome é {nome_agente}. Responde em {idioma} com formato {' e '.join(formato)}. {regras}"

