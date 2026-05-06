
```markdown
#  AI Self-Healing Debug Agent

An autonomous debugging system that uses an LLM + `pytest` to detect, fix, and validate bugs in Python code automatically.

---

##  Overview

This project implements a closed-loop debugging agent that:

- Runs test cases
- Detects failures
- Uses an LLM to fix code
- Validates correctness
- Iterates until success

Think of it as a self-healing CI agent for Python code.

---

##  How It Works

Run Tests → Fail → Plan → Fix → Validate → Review → Repeat

###  Execution Flow

1. Run tests using `pytest`
2. If tests fail:
   - Planner decides next action  
   - Debugger (LLM) generates code fix  
   - Structure Validator ensures code integrity  
   - Reviewer approves/rejects changes  
3. Repeat until:
   - All tests pass OR  
   - Max iterations reached  

---

## 📂 Project Structure

```

ai-debug-agent/
│
├── agent.py # Main agent loop (orchestrator)
├── app.py # Buggy source code (target)
├── llm.py # LLM integration (Ollama)
├── test_app.py # Test cases (pytest)
├── requirements.txt
└── README.md

````

---

##  Setup & Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ai-debug-agent
````

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Mac/Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

##  LLM Setup (Ollama)

### 1. Install Ollama

Mac:

```bash
brew install ollama
```

(For Linux/Windows: download from [https://ollama.com](https://ollama.com))

---

### 2. Start Ollama Server

```bash
ollama serve
```

---

### 3. Pull Model

```bash
ollama pull llama3
```

---

### 4. Test Model

```bash
ollama run llama3
```

---

##  Running the Agent

```bash
python agent.py
```

