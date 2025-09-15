

# **Gen AI-Powered HR Candidate & Role Insights — A Practical LangChain Demo**

## **Intro: Why Automate HR Research?**

Buzzwords aside, the day-to-day reality of HR means endless Googling, comparing candidate profiles and job requirements, and manually building up shortlists.   
Instead, what if you could ask a question like *“Best fit for a Product Manager role in Mumbai ?”*—and let an AI tool scour the web, summarize strengths, skills, and job-market needs, and instantly give you an actionable verdict?

This is exactly what we build in this tutorial: a real, working pipeline using LangChain, Google Gemini (free API), and DuckDuckGo search—all glued together with proper chains so you can clearly see each step. Perfect for HR professionals, GenAI learners, and anyone wanting to explore practical LLM app design.

[**Google collab notebook**](https://colab.research.google.com/drive/1x3FXno8bOgQoFwXEPiPbTESJFMSGMPjQ?usp=sharing)

***

## **Project Flow Diagram (Text Description)**

**INSERT IMAGE HERE**

***

## **Jupyter Notebook: Step-by-Step with Explanations**

***

### **Cell 1: Install All Required Packages**

```python
!pip install -U langchain langchain-google-genai langchain-community duckduckgo-search
```

**Explanation:**  
We install the latest versions of the core libraries for our pipeline:

- **langchain**: Orchestration of all LLM chains, agents, and tools.
- **langchain-google-genai**: Seamlessly integrates Google’s Gemini LLM with LangChain.
- **langchain-community**: Extra integrations, including tools and data connectors.
- **duckduckgo-search**: Provides free web search functionality, crucial for fetching real-world, up-to-date info on candidates or job skills.

***

### **Cell 2: Set up Gemini API Key**

```python
import os
os.environ["GOOGLE_API_KEY"] = "" # <--- YOUR KEY GOES HERE
```

**Explanation:**  
Here you securely save your Gemini API key in your Python environment—so the LLM can authenticate and run.  
**Pro Tip:** Always keep this key blank or in environment variables for sharing notebooks (never hard-code the real value publicly)!

***

### **Cell 3: Import LangChain Libraries and Helpers**

```python
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchResults
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain
```

**Explanation:**  
- The core LangChain classes/components.
- Gemini’s LLM connector.
- DuckDuckGo tool for free search.
- Prompt template classes to instruct both tools and LLMs.
- LLMChain and SimpleSequentialChain for composable pipeline steps.

***

### **Cell 4: Build a Custom LLM Wrapper for DuckDuckGo**

```python
class DuckDuckGoLLM(LLM):
    def _call(self, prompt, stop=None, run_manager: CallbackManagerForLLMRun = None, **kwargs):
        search = DuckDuckGoSearchResults()
        return search.run(prompt)
    @property
    def _llm_type(self):
        return "custom_duckduckgo"
```

**Explanation:**  
- LangChain encourages each “chain” to look like an LLM (even if it’s a tool).
- We make a minimal subclass that “pretends” to be an LLM but simply calls DuckDuckGo, returning a string of search results.
- This allows us to wire the search step right into a `SimpleSequentialChain` with no hacks!

***

### **Cell 5: Get Your HR User Input**

```python

target_role = "Product Manager"
location = "Mumbai"


search_query = (
    f'"{location}" ("{target_role}" OR "Senior {target_role}") site:linkedin.com/in '
    'resume projects skills 2025'
)
```

**Explanation:**  
- The HR user enters a Location and Target job role.
- Both are merged into a single, smart query—for richer, contextual web results (Location  + latest skill demands).

***

### **Cell 6: Define the Search Chain**

```python
search_prompt = PromptTemplate.from_template("{query}")

duckduck_llm = DuckDuckGoLLM()
search_chain = LLMChain(
    llm=duckduck_llm,
    prompt=search_prompt,
    output_key="search_results"
)
```

**Explanation:**  
- Sets up the first LangChain chain—using your custom LLM and a simple prompt template that inserts your full HR query.
- The chain will take the HR query, perform the DuckDuckGo search, and output free-text search results as `'search_results'`.

***

### **Cell 7: Define the Gemini Summarizer Chain**

```python

gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

summarize_prompt = ChatPromptTemplate.from_template(
    f"You're an HR assistant. "
    "Given these web search results (candidate info and top skills):\n{search_results}\n\n For all the different Candidiates "
    f"TARGET ROLE IS {target_role}"
    "Summarize in:\n"
    "- List all the candidates with thier links from the info "
    "- A list of each candidate's main strengths\n"
    "- Key candidates highlights matching the role\n"
    "- A ready-to-copy shortlist or not recommendation for busy HR.\n"
    "Use clear, up-to-date professional language."
)
summarize_chain = LLMChain(
    llm=gemini_llm,
    prompt=summarize_prompt
)

```

**Explanation:**  
- Sets up step two, using Gemini to process the fetched search results.
- The prompt is engineered (drawing from good prompt techniques) to give:
    - Bullet points of strengths
    - Match to role
    - Quick “shortlist or not” recommendation
- Designed to appeal to HR and to demo chained, composable LLM integration.  
- To learn more about *Prompt Engineering* used in thh above code snippet and make your own custom accurate prompts u can refer this [**Guide**](https://dev.to/raunaklallala/article-1-intro-to-gen-aillms-and-langchain-frameworkspart-c-48ij)
***

### **Cell 8: Combine Both Chains and Run!**

```python
overall_chain = SimpleSequentialChain(
    chains=[search_chain, summarize_chain],
    verbose=True
)

result = overall_chain.run(search_query)
print(result)
```

**Explanation:**  
- `SimpleSequentialChain` connects both steps so the output of `search_chain` becomes the input to `summarize_chain`.
- The process is fully modular, each chain is defined, testable, and reusable on its own!
- You pass your overall query and get back Gemini’s HR-friendly recommendation—just like a real hiring assistant would do.

***

## **Wrap-Up**

- **What did we build?**  
  An honest, simple LangChain pipeline:  
  _User input_ → _Search tool_ → _LLM summary_ → _Instant, actionable candidate verdict!_

- **What does this show off?**  
  - True, composable multi-step processing in LangChain
  - Prompt engineering best practices for HR
  - How to blend web tools and LLMs, even without complicated agent code

- **Where to go next?**  
  Try running with more candidate/role inputs, extending with another Gemini step, or producing a PDF/CSV for your HR team!

***