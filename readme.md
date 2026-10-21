# 🤖 Agent Harness - Building the System Around the Model

Este projeto é uma implementação prática do conceito de **Harness Engineering** (Engenharia de Harness) para Agentes de IA. Ele demonstra como construir o sistema ao redor de um LLM (Large Language Model) para garantir segurança, validação, persistência e controle de execução.

Baseado no artigo *"A Practical Guide to Harness Engineering: Building the System Around the Model"*.

## 🌟 Principais Recursos

- **🗂️ Workspace Isolado (Sandbox):** O agente opera em um diretório temporário. Tentativas de ler ou escrever fora dessa pasta são bloqueadas.
- **🛡️ Tool Gate (Controle de Permissões):** Arquivos críticos (como testes e regras de projeto) são protegidos como somente-leitura.
- **✅ Verificação de Conclusão:** O agente não pode simplesmente "dizer" que terminou. O Harness executa os testes (`unittest`) e apenas aceita a finalização se os testes passarem.
- **💾 Estado Persistente (Durable State):** Cada passo do agente é salvo em `.harness/state.json`, permitindo retomada e auditoria.
- **🛑 Limite de Passos (Cost Limit):** Previne loops infinitos parando o agente após um número predefinido de passos.

## 📂 Arquitetura do Projeto

O projeto segue uma estrutura modular padrão de mercado:

```text
agent-harness/
├── src/
│   ├── core/           # Lógica central (Harness e exceções customizadas)
│   ├── models/         # Adaptadores para os LLMs (Scripted Model, Claude, etc.)
│   ├── tools/          # Definições das ferramentas (Tool Specs JSON schemas)
│   ├── utils/          # Utilitários (criação do ambiente mockado temporário)
├── main.py             # Ponto de entrada da aplicação
├── requirements.txt    # Dependências do projeto
├── README.md           # Documentação
```

## 🚀 Como Configurar e Instalar

1. **Clone ou acesse a pasta do projeto:**
   ```bash
   cd agent-harness
   ```

2. **Crie e ative um ambiente virtual (Recomendado):**
   - **Linux/macOS:**
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Instale as dependências:**
   *(O projeto base usa apenas a biblioteca padrão do Python. A instalação abaixo é necessária apenas se for utilizar o modelo real do Claude).*
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Como Executar

### 1. Modo Simulação (Offline e Gratuito)
Roda cenários predefinidos usando o `ScriptedModel`. Excelente para testar as travas de segurança do Harness sem gastar tokens.
```bash
python main.py
```
*Irá executar dois cenários: um onde o agente tenta burlar regras antes de consertar o código, e outro onde o agente entra em loop.*

### 2. Modo com LLM Real (Claude)
Conecta-se à API da Anthropic para resolver o problema de forma autônoma.
1. Configure sua variável de ambiente com a chave da API:
   - **Linux/macOS:** `export ANTHROPIC_API_KEY="sua_chave_aqui"`
   - **Windows (PowerShell):** `$env:ANTHROPIC_API_KEY="sua_chave_aqui"`
2. Execute com a flag `--claude`:
   ```bash
   python main.py --claude
   ```

## 🐞 Executando via VS Code (Debug)
O projeto já suporta execução direta pelo VS Code via `launch.json`. Basta ir na aba **Run and Debug** (`Cmd + Shift + D` ou `Ctrl + Shift + D`), selecionar o modo desejado no menu suspenso superior e clicar em "Play".

---
*Construído para fins educacionais e experimentação em arquitetura de Agentes de IA.*