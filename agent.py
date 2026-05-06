import subprocess
import json
import re
from llm import call_llm

# ---------------- UTIL ----------------

def read_code():
    with open("app.py", "r") as f:
        return f.read()

def write_code(code):
    with open("app.py", "w") as f:
        f.write(code)

def run_tests():
    result = subprocess.run(["pytest"], capture_output=True, text=True)
    return result.stdout + result.stderr


# ---------------- PARSERS ----------------

def clean(text):
    match = re.search(r"```python(.*?)```", text, re.S)
    if match:
        return match.group(1).strip()

    match = re.search(r"```(.*?)```", text, re.S)
    if match:
        return match.group(1).strip()

    match = re.search(r"(class |def |import )", text, re.S)
    if match:
        return text[match.start():].strip()

    return text.strip()


def extract_json(text):
    try:
        return json.loads(text)
    except:
        pass

    match = re.search(r"\{.*\}", text, re.S)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    return None


# ---------------- STRUCTURE VALIDATION ----------------

def validate_structure(code):
    required = [
        "class BankAccount",
        "def deposit",
        "def withdraw",
        "def total_balance",
        "def richest"
    ]
    return all(r in code for r in required)


def validate_review(obj):
    if not isinstance(obj, dict):
        return False

    if obj.get("decision") not in ["approve", "reject"]:
        return False

    if not isinstance(obj.get("issues"), list):
        return False

    if not isinstance(obj.get("confidence"), (int, float)):
        return False

    return True


# ---------------- CONFIG ----------------

MAX_ITERS = 5
MAX_ATTEMPTS = 3


# ---------------- PLANNER ----------------

def planner(test_output):
    prompt = f"""
Return ONLY JSON:

{{
  "action": "fix",
  "reason": "short explanation"
}}

No extra text.

Test output:
{test_output}
"""

    raw = call_llm(prompt).strip()
    parsed = extract_json(raw)

    return parsed if parsed else {"action": "fix", "reason": "fallback"}


# ---------------- DEBUGGER ----------------

def debugger(code, error):
    prompt = f"""
You are a senior Python engineer.

You are editing an existing file.

CRITICAL RULES:
- DO NOT remove working classes or functions
- DO NOT delete existing logic unless broken
- Preserve structure exactly
- Only fix root cause bugs

Return ONLY full corrected code.

FAILURES:
{error}

CODE:
{code}
"""

    return clean(call_llm(prompt))


# ---------------- REVIEWER ----------------

def reviewer(old_code, new_code, output):
    prompt = f"""
Return ONLY valid JSON:

{{
  "decision": "approve" | "reject",
  "issues": ["..."],
  "confidence": 0.0
}}

Rules:
- decision must be approve or reject
- issues must be list
- confidence must be 0-1 number

No extra text.

Old Code:
{old_code}

New Code:
{new_code}

Test Output:
{output}
"""

    raw = call_llm(prompt).strip()
    parsed = extract_json(raw)

    if parsed and validate_review(parsed):
        return parsed

    return {
        "decision": "reject",
        "issues": ["invalid reviewer output"],
        "confidence": 0.0
    }


# ---------------- MAIN LOOP ----------------

def run_agent():
    print("📂 Loading code...")
    code = read_code()

    for i in range(MAX_ITERS):
        print(f"\n🔁 ITERATION {i+1}")

        output = run_tests()
        print(output)

        if "failed" not in output.lower():
            print("✅ All tests passed!")
            break

        plan = planner(output)
        print("🧠 Plan:", plan)

        fixed = False

        for attempt in range(MAX_ATTEMPTS):
            print(f"🛠 Fix attempt {attempt+1}")

            new_code = debugger(code, output)

            # 🔒 HARD SAFETY GATE
            if not validate_structure(new_code):
                print("⚠️ Structure broken — rejecting rewrite")
                continue

            review = reviewer(code, new_code, output)
            print("🧠 Reviewer:", review)

            if review["decision"] == "approve":
                code = new_code
                write_code(code)
                print("✅ Fix applied")
                fixed = True
                break
            else:
                print("❌ Fix rejected")

        if not fixed:
            print("⚠️ No valid improvement this iteration")

    print("\n🏁 DONE")


if __name__ == "__main__":
    run_agent()