# Article 1 :Intro to Gen AI,LLMS and LangChain Frameworks(Part F:The Practical)

## Chapter F: Practical LangChain Demo with Google Gemini & DuckDuckGo
---
This tutorial walks you through building a **LangChain-powered app** that connects Google’s **Gemini model** with a **search tool (DuckDuckGo)**.  
We’ll cover prerequisites, installation, and why each step is needed.

---

###  Prerequisites
Before starting, make sure you have:
- Python 3.8 or higher
- A Google API Key (get it from [Google AI Studio](https://ai.google.dev/))
- Basic knowledge of Python

---

###  Installation

We’ll install the required packages:  

```bash
pip install -U langchain langchain-google-genai langchain-community duckduckgo-search
````

* **langchain** → the framework to chain LLMs with tools.
* **langchain-google-genai** → connector for Google Gemini.
* **langchain-community** → community-maintained integrations (like DuckDuckGo).
* **duckduckgo-search** → enables web search from LangChain.

---

###  Setting Up API Keys

```python
import os

# put your key here (replace with your actual key)
os.environ["GOOGLE_API_KEY"] = "your_api_key_here"
```

* Storing your key in `os.environ` makes it secure and reusable across code.
* You can also set it in your system environment variables or Colab secrets.

---

###  Loading the Gemini Model

```python
from langchain_google_genai import ChatGoogleGenerativeAI

# use the free Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
```

* We’re using **Gemini 1.5 Flash**, which is free and optimized for quick responses.
* This acts as our **core LLM** that will generate answers.

---

###  Adding a Search Tool

```python
from langchain_community.tools import DuckDuckGoSearchResults

# search tool
search = DuckDuckGoSearchResults()
```

* This tool allows the LLM to **fetch real-time info** from DuckDuckGo.
* It’s useful when the model needs **up-to-date knowledge** beyond its training data.

---

###  Creating a Prompt Template

```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "Search the web and summarize the latest news about {topic}."
)
```

* `ChatPromptTemplate` lets you **structure prompts** dynamically.
* The `{topic}` placeholder means we can reuse the same template for any topic.

---

###  Building Chains

```python
from langchain.chains import LLMChain, SequentialChain

# first chain: search results
search_chain = LLMChain(llm=llm, prompt=prompt)

# sequential chain: combines search + LLM summarization
overall_chain = SequentialChain(
    chains=[search_chain],
    input_variables=["topic"],
    output_variables=["text"]
)
```

* `LLMChain` connects a model with a specific prompt.
* `SequentialChain` lets you **stack multiple chains together** (e.g., search → summarize).
* This modular design makes your pipeline scalable.

---

###  Running the Demo

```python
result = overall_chain({"topic": "AI in healthcare"})
print(result)
```

* Input: `"AI in healthcare"`
* Process:

  1. Search latest info using DuckDuckGo
  2. Gemini summarizes findings
* Output: A clean summary of current news!

---

###  Why This Matters

* LangChain simplifies combining **LLMs + external tools**.
* Gemini provides **fast, accurate generation**.
* DuckDuckGo adds **real-time context**.

This workflow is perfect for building **research assistants, news aggregators, or knowledge tools**.

---

###  Next Steps

* Add more tools (e.g., calculators, APIs).
* Explore memory features in LangChain for multi-turn conversations.
* Deploy your chain into a web app using **Streamlit** or **FastAPI**.

---

->You now have a **working LangChain pipeline** with Google Gemini + DuckDuckGo search!
