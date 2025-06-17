from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv
import litellm

load_dotenv()

# Set provider & base URL if not already in .env
os.environ["LITELLM_PROVIDER"] = "ollama"
os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"

# CrewAI uses LiteLLM internally, so we just set the model name correctly
ollama_llm = "ollama/phi"  # Must match LiteLLM model naming scheme

# Define Agent
redaction_agent = Agent(
    name="Redaction Agent",
    role="Identifies and Redacts sensitive info in text",
    goal="Ensure that any sensitive content is replaced with redacted tags",
    backstory="An AI that specializes in document sanitization and privacy",
    llm=ollama_llm  # use string model name, not LangChain object
)

def redact_text_with_crew(text: str) -> str:
    task = Task(
        description=f"""
You are a redaction assistant. Your job is to detect and redact **sensitive information** from the given text. 

Sensitive info includes:
- Email addresses
- Phone numbers
- Passwords
- Social Security Numbers (SSNs)
- API keys
- Any obvious identifiers (like full names, usernames)

**Instructions:**
- Replace each sensitive item with `[REDACTED]` (keep the format, spacing, and line structure intact).
- Do **not** explain anything.
- Return only the redacted version of the input.

### INPUT TEXT:
{text}

### REDACTED OUTPUT:
""",
        agent=redaction_agent,
        expected_output="Redacted text only. No commentary or explanation."
    )

    crew = Crew(agents=[redaction_agent], tasks=[task])
    result = crew.kickoff()

    # 🧼 Post-process to remove assistant chatter and extract clean output
    raw_output = str(result)
    if "### REDACTED OUTPUT:" in raw_output:
        redacted_text = raw_output.split("### REDACTED OUTPUT:")[-1].strip()
        redacted_text = redacted_text.split("Output:")[0].split("Assistant:")[0].strip()
    else:
        redacted_text = raw_output.strip()

    return redacted_text




# from crewai import Agent, Task, Crew
# import os
# # from langchain_community.llms.ollama import Ollama
# from dotenv import load_dotenv
# from langchain.chat_models import ChatOpenAI

# load_dotenv()
# os.environ["LLM_PROVIDER"] = "openrouter"
# api_key = os.getenv("OPENAI_API_KEY")
# # ollama_llm = Ollama(model="phi")
# # llm = ChatOpenAI(model_name="gpt-4-1106-preview", openai_api_key=api_key)

# llm = ChatOpenAI(
#     openai_api_base="https://openrouter.ai/api/v1",
#     openai_api_key=api_key,
#     model_name="meta-llama/llama-3.3-8b-instruct:free"  # or any OpenRouter model
# )

# redaction_agent = Agent(
#     name = "Redaction Agent",
#     role = "Identifies and Redacts sensitive info in text",
#     goal = "Ensure that any sensitive content is replaces with redacted tags",
#     backstory = "An AI that specializes in dodument sanitization and privacy",
#     llm = llm
# )

# def redact_text_with_crew(text: str) -> str:
#     task = Task(
#         description=f"Scan this text and replace any sensitive info such as passwords, emails, or phone numbers with [REDACTED]:\n\n{text}",
#         agent=redaction_agent,
#         expected_output="The redacted version of the original text."
#     )

#     crew = Crew(agents=[redaction_agent], tasks=[task])
#     result = crew.kickoff()
#     return result