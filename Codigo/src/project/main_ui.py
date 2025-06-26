import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json, os, threading
from datetime import datetime, date
from tkcalendar import DateEntry

from project.config_manager import save_config, load_config
from moodle_fetchers.data_manager import MoodleDataManager
from project.llm_connector import enviar_para_ollama_stream
from moodle_fetchers.local_loader import load_all_data
from project.agent_core import run_agent


CONFIG_FILE = "last_prompt.json"
AGENT_CONFIG_FILE = "config_agente.json"
HISTORICO_FILE = "historico_agente.json"

class CustomUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Configuração do Agente IA")
        self.center_window(self.root, 750, 650)

        # Notebook com abas
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=True, fill="both")

        # Abas
        self.config_tab = ttk.Frame(self.tabs)
        self.init_sist_tab = ttk.Frame(self.tabs)
        self.reports_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.config_tab, text="Configurar Agente")
        self.tabs.add(self.init_sist_tab, text="Iniciar Sistema")
        self.tabs.add(self.reports_tab, text="Relatórios e Histórico")

        self.agent_name_var = tk.StringVar()
        self.language_var = tk.StringVar()
        self.formato_breve = tk.BooleanVar()
        self.formato_detalhado = tk.BooleanVar()
        self.formato_sugestoes = tk.BooleanVar()
        self.ollama_model_var = tk.StringVar(value="llama3")
        self.ollama_url_var = tk.StringVar(value="http://localhost:11434")
        self.agent_id_var = tk.StringVar(value=16)
        self.course_id_var = tk.StringVar(value=2)
        self.moodle_url_var = tk.StringVar(value="http://localhost:8081")
        self.moodle_token_var = tk.StringVar(value="f7589d878ac5f35a2a46583b45521b38")

        self.setup_config_tab()
        self.setup_init_sist()
        self.setup_reports_tab()

        self.root.mainloop()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def setup_config_tab(self):
        frame = tk.Frame(self.config_tab)
        frame.pack(padx=10, pady=10, anchor="w", fill="both")

        # Modelo Ollama
        tk.Label(frame, text="Modelo Ollama:").pack(anchor="w", pady=2)
        tk.Entry(frame, textvariable=self.ollama_model_var, width=40).pack(anchor="w", pady=2)

        # URL Ollama
        tk.Label(frame, text="URL do Ollama:").pack(anchor="w", pady=2)
        tk.Entry(frame, textvariable=self.ollama_url_var, width=40).pack(anchor="w", pady=2)

        # Nome do Agente
        tk.Label(frame, text="Nome do Agente:").pack(anchor="w", pady=(0, 2))
        self.agent_name_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.agent_name_var, justify="left", width=40).pack(anchor="w", pady=(0, 5))

        # Idioma
        tk.Label(frame, text="Idioma:").pack(anchor="w", pady=(0, 2))
        self.language_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.language_var, justify="left", width=20).pack(anchor="w", pady=(0, 5))

        # Formato de resposta (Checkbuttons)
        tk.Label(frame, text="Formato da Resposta:").pack(anchor="w", pady=(0, 2))
        formato_frame = tk.Frame(frame)
        formato_frame.pack(anchor="w", pady=(0, 5))

        self.formato_breve = tk.BooleanVar()
        self.formato_detalhado = tk.BooleanVar()
        self.formato_sugestoes = tk.BooleanVar()

        tk.Checkbutton(formato_frame, text="Breve", variable=self.formato_breve).pack(anchor="w")
        tk.Checkbutton(formato_frame, text="Detalhado", variable=self.formato_detalhado).pack(anchor="w")
        tk.Checkbutton(formato_frame, text="Com Sugestões", variable=self.formato_sugestoes).pack(anchor="w")

        # Regras Pedagógicas
        tk.Label(frame, text="Regras Pedagógicas:").pack(anchor="w", pady=(5, 2))
        self.pedagogical_rules_text = tk.Text(frame, height=10, width=100, wrap="word")
        self.pedagogical_rules_text.pack(anchor="w", pady=(0, 5))

        # Botão Guardar centrado
        tk.Button(frame, text="Guardar Configuração", command=self.save_config_ui).pack(pady=10)

        self.load_config_ui()

    def save_config_ui(self):
        config = {
            "ollama_model": self.ollama_model_var.get(),
            "ollama_url": self.ollama_url_var.get(),
            "agent_name": self.agent_name_var.get(),
            "language": self.language_var.get(),
            "formato_breve": self.formato_breve.get(),
            "formato_detalhado": self.formato_detalhado.get(),
            "formato_sugestoes": self.formato_sugestoes.get(),
            "pedagogical_rules": self.pedagogical_rules_text.get("1.0", "end").strip(),
        }
        save_config(config)
        messagebox.showinfo("Configuração", "Configuração guardada com sucesso!")
 
    def load_config_ui(self):
        config = load_config()
        self.ollama_model_var.set(config.get("ollama_model", "llama3"))
        self.ollama_url_var.set(config.get("ollama_url", "http://localhost:11434")) 
        self.agent_name_var.set(config.get("agent_name", "TutorIA"))
        self.language_var.set(config.get("language", "pt"))
        self.formato_breve.set(config.get("formato_breve", False))
        self.formato_detalhado.set(config.get("formato_detalhado", False))
        self.formato_sugestoes.set(config.get("formato_sugestoes", False))
        self.pedagogical_rules_text.delete("1.0", "end")
        self.pedagogical_rules_text.insert("1.0", config.get("pedagogical_rules", ""))

    def setup_init_sist(self):
        frame = tk.Frame(self.init_sist_tab)
        frame.pack(padx=20, pady=20, anchor="nw", fill="both", expand=True)

        # ID do Curso
        tk.Label(frame, text="ID interno da Unidade Curricular no Moodle:").pack(anchor="w")
        tk.Entry(frame, textvariable=self.course_id_var, width=20).pack(anchor="w", pady=(0, 5))

        # ID do Agente
        tk.Label(frame, text="ID interno do Agente no Moodle:").pack(anchor="w")
        tk.Entry(frame, textvariable=self.agent_id_var, width=20).pack(anchor="w", pady=(0, 5))

        # URL do Moodle
        tk.Label(frame, text="URL do Moodle:").pack(anchor="w")
        tk.Entry(frame, textvariable=self.moodle_url_var, width=50).pack(anchor="w", pady=(0, 5))

        # Token de Acesso
        tk.Label(frame, text="Token de Acesso:").pack(anchor="w")
        tk.Entry(frame, textvariable=self.moodle_token_var, width=50).pack(anchor="w", pady=(0, 5))
        
        # Botões de ação
        btn_frame = tk.Frame(frame)
        btn_frame.pack(anchor="w", pady=(0, 5))
        tk.Button(btn_frame, text="Obter Dados", command=self.obter_dados).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Iniciar Sistema", command=self.iniciar_sistema_ui).pack(side=tk.LEFT, padx=5)

        # Mensagens de estado
        self.status_label = tk.Label(frame, text="", fg="green")
        self.status_label.pack(anchor="w", pady=(0, 5))

        # Área de logs
        tk.Label(frame, text="Registo de Atualizações:", font=("Helvetica", 11, "bold")).pack(anchor="w")
        self.log_area = scrolledtext.ScrolledText(frame, height=10, state="disabled", wrap="word", font=("Helvetica", 10))
        self.log_area.pack(fill="both", expand=True)

    def ler_ultimos_updates(self, n=10, log_path="data_updates.log"):
        if not os.path.exists(log_path):
            return ["Nenhum registo encontrado."]
        
        with open(log_path, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            if not linhas:
                return ["Nenhum registo encontrado."]
            return [linha.strip() for linha in linhas[-n:]]
            
    def obter_dados(self):
        try:
            course_id = int(self.course_id_var.get())
            agent_id = int(self.agent_id_var.get())
            dados = MoodleDataManager(course_id, agent_id).fetch_all()

             # Mostrar os últimos 3 updates
            updates = self.ler_ultimos_updates(10)
            self.log_area.config(state="normal")
            self.log_area.delete("1.0", tk.END)
            self.log_area.insert(tk.END, "\n".join(updates))
            self.log_area.config(state="disabled")


            self.status_label.config(text="Dados obtidos com sucesso!", fg="green")

        except Exception as e:
            self.status_label.config(text="Erro ao obter dados!", fg="red")
            messagebox.showerror("Erro", f"Erro ao obter dados:\n{e}")

    def iniciar_sistema_ui(self):
        try:
            # 1. Obter valores da interface
            ollama_model = self.ollama_model_var.get().strip()
            url_ollama = self.ollama_url_var.get().strip()
            course_id = int(self.course_id_var.get())
            agent_id = int(self.agent_id_var.get())
            moodle_url = self.moodle_url_var.get().strip()
            moodle_token = self.moodle_token_var.get().strip()

            # 2. Verificar se os campos estão preenchidos
            if not ollama_model or not url_ollama or not course_id or not agent_id or not moodle_url or not moodle_token:
                messagebox.showwarning("Configuração", "Introduza o dados em falta.")
                return

            config = load_config()

            config.update({
                "course_id": course_id,
                "agent_id": agent_id,
                "moodle_url": moodle_url,
                "moodle_token": moodle_token 
            })

            # 3. Guarda a configuração
            save_config(config)

            # 4. Iniciar o agente
            threading.Thread(target=self.run_agente_thread, args=(config,), daemon=True).start()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar sistema:\n{e}")

    def run_agente_thread(self, config):
        try:
            run_agent(config)
            self.root.after(0, lambda: messagebox.showinfo("Sistema", "Agente executado com sucesso!"))
        except Exception as e:
            self.root.after(0, lambda err=e: messagebox.showerror("Erro", f"Erro ao executar o agente: {err}"))

    def setup_reports_tab(self):
        frame = tk.Frame(self.reports_tab)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Filtros
        filter_frame = tk.Frame(frame)
        filter_frame.pack(anchor="w", pady=(0, 10))

        self.date_from_var = tk.StringVar()
        self.date_to_var = tk.StringVar()
        self.action_type_var = tk.StringVar()

        # Linha 1 - De / Até
        linha1 = tk.Frame(filter_frame)
        linha1.pack(anchor="w", pady=2)
        # Valores por omissão com a data de hoje
        self.date_from_var = tk.StringVar(value=date.today().isoformat())
        self.date_to_var = tk.StringVar(value=date.today().isoformat())

        tk.Label(linha1, text="De:").pack(side="left", padx=(0, 5))
        self.date_from = tk.Entry(linha1, textvariable=self.date_from_var, width=12)
        self.date_from.pack(side="left", padx=(0, 15))

        tk.Label(linha1, text="Até:").pack(side="left", padx=(0, 5))
        self.date_to = tk.Entry(linha1, textvariable=self.date_to_var, width=12)
        self.date_to.pack(side="left")

        # Linha 2 - Tipo de Ação (Combobox em vez de Entry)
        linha2 = tk.Frame(filter_frame)
        linha2.pack(anchor="w", pady=5)
        tk.Label(linha2, text="Tipo de Ação:").pack(side="left", padx=(0, 5))

        tipos_acoes = ["Todas", "Intervenções em Fóruns", "Mensagens Privadas", "Alterações na Disciplina"]
        self.action_type_combobox = ttk.Combobox(linha2, textvariable=self.action_type_var, values=tipos_acoes, width=30, state="readonly")
        self.action_type_combobox.current(0)
        self.action_type_combobox.pack(side="left", padx=(0, 10))

        # Área do histórico (pode mostrar uma prévia ou sumário)
        tk.Label(frame, text="Registo de Ações:", font=("Helvetica", 11, "bold")).pack(anchor="w")
        self.historico_area = scrolledtext.ScrolledText(frame, wrap="word", height=20)
        self.historico_area.pack(fill="both", expand=True, pady=5)

        # Filtrar + Gerar Relatório
        botoes_frame = tk.Frame(filter_frame)
        botoes_frame.pack(anchor="w", pady=(5, 5))

        tk.Button(botoes_frame, text="Filtrar", command=self.filtrar_historico).pack(side="left", padx=(0, 10))
        tk.Button(filter_frame, text="Gerar Relatório", command=self.gerar_relatorio).pack(anchor="w", pady=(0, 5))
    
    from datetime import datetime

    def gerar_relatorio(self):
        tipo = self.action_type_var.get()
        data_de = self.date_from_var.get()
        data_ate = self.date_to_var.get()

        if tipo == "Todas":
            tipo = ""

        if not os.path.exists(HISTORICO_FILE):
            messagebox.showinfo("Relatório", "O histórico ainda não está disponível.")
            return

        with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
            historico = json.load(f)

        # Converter as datas de filtro
        data_de_dt = datetime.strptime(data_de, "%Y-%m-%d") if data_de else None
        data_ate_dt = datetime.strptime(data_ate, "%Y-%m-%d") if data_ate else None
        if data_ate_dt:
            data_ate_dt = data_ate_dt.replace(hour=23, minute=59, second=59)

        entradas = []
        for entrada in historico:
            data_str = entrada.get("data", "")
            acao = entrada.get("acao", "").lower()
            detalhes = entrada.get("detalhes", "")

            try:
                data_dt = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue  # ignora entradas mal formatadas

            if data_de_dt and data_dt < data_de_dt:
                continue
            if data_ate_dt and data_dt > data_ate_dt:
                continue
            if tipo and tipo.lower() not in acao:
                continue

            entradas.append(f"{data_str} | {entrada['acao']}\n{detalhes}\n")

        conteudo = f"Relatório\nTipo de Ação: {tipo or 'Todas'}\nPeríodo: {data_de} a {data_ate}\n\n"
        conteudo += "\n".join(entradas) if entradas else "Nenhuma entrada corresponde aos filtros aplicados.\n"

        # Janela do relatório
        janela = tk.Toplevel()
        janela.title("Relatório Gerado")
        janela.geometry("600x450")

        tk.Label(janela, text="Relatório Gerado com Sucesso", font=("Helvetica", 12, "bold")).pack(pady=(10, 5))
        texto = scrolledtext.ScrolledText(janela, wrap="word")
        texto.pack(fill="both", expand=True, padx=10, pady=5)
        texto.insert("1.0", conteudo)
        texto.config(state="disabled")

        def guardar():
            ficheiro = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Ficheiros de Texto", "*.txt")])
            if ficheiro:
                with open(ficheiro, "w", encoding="utf-8") as f:
                    f.write(conteudo)
                messagebox.showinfo("Relatório", "Relatório guardado com sucesso.")
                janela.destroy()

        botoes = tk.Frame(janela)
        botoes.pack(pady=10)
        tk.Button(botoes, text="Guardar", command=guardar).pack(side="left", padx=10)
        tk.Button(botoes, text="Fechar", command=janela.destroy).pack(side="left")

    def filtrar_historico(self):
        try:
            self.historico_area.configure(state="normal")
            self.historico_area.delete("1.0", tk.END)

            if not os.path.exists(HISTORICO_FILE):
                self.historico_area.insert(tk.END, "Histórico ainda não disponível.")
                self.historico_area.configure(state="disabled")
                return

            with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
                historico = json.load(f)

            data_de = self.date_from_var.get()
            data_ate = self.date_to_var.get()
            tipo = self.action_type_var.get().strip().lower()

            data_de_dt = datetime.strptime(data_de, "%Y-%m-%d") if data_de else None
            data_ate_dt = datetime.strptime(data_ate, "%Y-%m-%d") if data_ate else None

            resultados = []
            for entrada in historico:
                acao = entrada.get("acao", "").lower()
                data_str = entrada.get("data", "")
                try:
                    data_registo = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue  # ignora entradas mal formatadas

                if data_de_dt and data_registo < data_de_dt:
                    continue
                if data_ate_dt and data_registo > data_ate_dt.replace(hour=23, minute=59, second=59):
                    continue

                # Filtro por tipo de ação (ignorar se for "todas")
                if tipo != "todas" and tipo not in acao:
                    continue

                resultados.append(f"{data_str} | {entrada['acao']}\n{entrada['detalhes']}\n")

            if resultados:
                self.historico_area.insert(tk.END, "\n".join(resultados))
            else:
                self.historico_area.insert(tk.END, "Nenhuma entrada corresponde aos filtros aplicados.")

            self.historico_area.configure(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao filtrar histórico:\n{e}")


if __name__ == "__main__":
    CustomUI()
