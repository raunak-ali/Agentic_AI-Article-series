# **Agentic AI based Smart Code Review Workflows That Actually Think:LangGraph in Action**

*Why simple LLMs and LangChain fall short when you need intelligent routing, memory, and conditional logic*

***

## **The Problem: One-Size-Fits-All Code Reviews**

Picture this: your development team receives dozens of pull requests daily. Some are simple documentation updates that need a quick style check. Others are complex security implementations that require deep architectural analysis. 

Currently, most teams either:
- **Manually assign reviewers** (time-consuming, inconsistent)
- **Use round-robin systems** (wastes senior developers' time on trivial changes)
- **Apply single LLM reviews** (generic feedback regardless of complexity)

What if your code review system could **intelligently analyze complexity** and **route to specialized reviewers** automatically? That's exactly what we'll build with LangGraph.

***

## **Why LangGraph > Simple LLM + LangChain**

Let's break down why traditional approaches fall short:

| Approach | What It Does | What It Misses |
|----------|-------------|----------------|
| **Single LLM** | Analyzes code → Generic review | No complexity routing, no memory |
| **LangChain** | Chains LLM calls → Sequential processing | Can't autonomously branch based on conditions |
| **LangGraph** | Analyzes → Routes → Specialized review + Memory | **Adaptive workflows with state** |

**The LangGraph Advantage:**
- ** Nodes**: Modular functions (complexity analyzer, specialized reviewers)
- ** Edges**: Conditional routing based on complexity score  
- ** State**: Maintains context throughout the entire workflow
- *What to explore the Langrapgh compoennts conceptutally in detail check out [**Understanding Core Concepts of LangGraph (Deep Dive)**]()*
***

## **What We're Building**

A **Smart Code Review System** that:

1. **Analyzes** code complexity using Python logic
2. **Routes** to either Quick Reviewer or Technical Reviewer  
3. **Maintains** context and complexity scores throughout
4. **Adapts** behavior based on the input

**INSERT IMAGE HERE**



## **Implementation: Step by Step**

### **Cell 1: Installation & Setup**

```python
# Install required packages
!pip install -qU langchain langgraph langchain-google-genai

# Import everything we need
import os
from typing import TypedDict, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END

# Set your Google API key
os.environ["GOOGLE_API_KEY"] = "your_api_key_here"  # Replace with your actual key
```

**Why these packages?**
- `langchain` - Core framework
- `langgraph` - Stateful workflows with conditional routing
- `langchain-google-genai` - Google Gemini integration

***

### **Cell 2: Define State Schema**

```python
# State schema - this carries data through all nodes
class ReviewState(TypedDict):
    code_changes: str      # Input code to review
    complexity_score: int  # Calculated complexity (0-10)
    review_type: str      # "Quick Review" or "Technical Review"  
    final_review: str     # Generated review content

# State schema defined
```

**Why State matters**: Unlike stateless chains, this lets every node access and modify shared context. The complexity score flows from analyzer → router → reviewer.

***

### **Cell 3: Setup LLM**

```python
# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Free tier model
    temperature=0.7            # Balanced creativity
)

#LLM initialized
```

***

### **Cell 4: Build Complexity Analyzer Node**

```python
def analyze_complexity(state: ReviewState) -> ReviewState:
    """
    Python function that analyzes code changes and assigns complexity score
    This is our 'smart routing' logic
    """
    code = state["code_changes"]
    score = 0
    
    # Count lines changed
    lines = len(code.split('\n'))
    if lines > 50:
        score += 3
    elif lines > 20:
        score += 2
    elif lines > 5:
        score += 1
    
    # Check for complex patterns
    complex_keywords = ['async', 'threading', 'database', 'security', 'authentication', 'payment']
    for keyword in complex_keywords:
        if keyword.lower() in code.lower():
            score += 2
    
    # Check file types
    if any(ext in code.lower() for ext in ['.sql', '.py', '.js', '.java']):
        score += 1
    
    # Documentation-only changes get lower scores
    if any(keyword in code.lower() for keyword in ['readme', 'documentation', 'comment', '# ']):
        score = max(0, score - 2)
    
    # Cap at 10 and store in state
    state["complexity_score"] = min(score, 10)
    print(f"🔍 Complexity Analysis: {state['complexity_score']}/10")
    
    return state

# Complexity analyzer ready
```

**Why this works**: Pure Python logic gives us **deterministic, explainable** complexity scoring. No LLM overhead for simple logic tasks.  
*In next chapters we would explore how we can aid agents with tools to handle the Logic + resoning parts*

***

### **Cell 5: Create Quick Reviewer Agent**

```python
# Quick reviewer for simple changes
quick_reviewer_prompt = """
You are a Quick Code Reviewer for simple changes. Focus on:
- Code style and formatting
- Basic functionality  
- Documentation clarity
- Simple bug catches

Keep reviews concise (2-3 bullet points) and encouraging.
You're reviewing straightforward changes that don't need deep analysis.
"""

quick_reviewer = create_react_agent(
    llm, 
    tools=[], 
    prompt=quick_reviewer_prompt
)

def quick_review_node(state: ReviewState) -> ReviewState:
    """Node that handles simple code reviews"""
    response = quick_reviewer.invoke({
        "messages": [("user", f"Review this code change:\n\n{state['code_changes']}\n\nFocus on style, basic functionality, and clarity.")]
    })
    
    state["review_type"] = "Quick Review"
    state["final_review"] = response["messages"][-1].content
    print(" Quick review completed")
    
    return state

# Quick reviewer agent created
# Note how when we wanna add a agent as a node in Langrapgh we first create an Agent and then invoke that agent inside a Node and use the Agents output to update the state of the grapgh inside the actual node not inside the Agent
```

***

### **Cell 6: Create Technical Reviewer Agent**

```python
# Technical reviewer for complex changes
technical_reviewer_prompt = """
You are a Senior Technical Reviewer for complex changes. Focus on:
- Architecture and design patterns
- Performance implications
- Security considerations  
- Scalability and maintainability
- Integration with existing systems

Provide detailed analysis with specific recommendations.
You're reviewing complex changes that could impact the system significantly.
"""

technical_reviewer = create_react_agent(
    llm, 
    tools=[], 
    prompt=technical_reviewer_prompt
)

def technical_review_node(state: ReviewState) -> ReviewState:
    """Node that handles complex code reviews"""
    response = technical_reviewer.invoke({
        "messages": [("user", f"Review this code change:\n\n{state['code_changes']}\n\nProvide thorough technical analysis focusing on architecture, performance, and security.")]
    })
    
    state["review_type"] = "Technical Review"
    state["final_review"] = response["messages"][-1].content
    print(" Technical review completed")
    
    return state

# Technical reviewer agent created
```

**Why separate agents?** Each agent has **specialized expertise** and **different review depths**. Quick reviewer saves time on simple changes; technical reviewer provides comprehensive analysis for complex ones.    
- Both Agents were equipped with targeted, strategic prompts to delve deeper into the fundamentals of **Prompt Engineering** [READ .](https://dev.to/raunaklallala/article-1-intro-to-gen-aillms-and-langchain-frameworkspart-c-48ij)

***

### **Cell 7: Define Routing Logic ( Making of Conditional Edge  )**

```python
def route_to_reviewer(state: ReviewState) -> Literal["quick_review", "technical_review"]:
    """
    Conditional edge logic - this is where the magic happens!
    Routes based on complexity score from our Python function
    """
    score = state["complexity_score"]
    
    if score <= 3:
        print(f"Routing to Quick Reviewer (Score: {score})")
        return "quick_review"
    else:
        print(f" Routing to Technical Reviewer (Score: {score})")
        return "technical_review"

# Routing logic defined, The conditioan edge is Defined on state values
```

**The Power of Conditional Edges**: This single function enables **intelligent branching**. Simple LLM chains can't do this - they're linear. LangGraph makes workflows **adaptive**.

***

### **Cell 8: Build the LangGraph Workflow**

```python
# Create the state graph
workflow = StateGraph(ReviewState)

# Add all nodes
workflow.add_node("analyze_complexity", analyze_complexity)
workflow.add_node("quick_review", quick_review_node)
workflow.add_node("technical_review", technical_review_node)

# Set entry point
workflow.set_entry_point("analyze_complexity")

# Add conditional edges - this is the branching logic
workflow.add_conditional_edges(
    "analyze_complexity",           # From this node
    route_to_reviewer,             # Use this function to decide
    {
        "quick_review": "quick_review",         # If returns "quick_review"
        "technical_review": "technical_review" # If returns "technical_review"
    }
)

# Both reviewers end the workflow
workflow.add_edge("quick_review", END)
workflow.add_edge("technical_review", END)

# Compile the graph
app = workflow.compile()

# LangGraph workflow built and compiled!
```

**Why this architecture wins**:
- **Modular**: Each node has a single responsibility
- **Adaptive**: Routes change based on input
- **Stateful**: Context flows through the entire pipeline
- **Scalable**: Easy to add new reviewer types or complexity rules

***

### **Cell 9: Test with Simple Change**

```python
# Test Case 1: Simple documentation change
simple_change = """
# README.md
## Installation


pip install our-package


## Usage
Updated usage examples with clearer variable names.
Added more descriptive comments for better readability.
"""

print("=== TESTING SIMPLE CHANGE ===")
result = app.invoke({
    "code_changes": simple_change,
    "complexity_score": 0,
    "review_type": "",
    "final_review": ""
})

print(f"\n Final Results:")
print(f"Complexity Score: {result['complexity_score']}")
print(f"Review Type: {result['review_type']}")
print(f"\n  Review Content:")
print(result['final_review'])
```

**Expected behavior**: Low complexity score → Routes to Quick Reviewer → Concise, style-focused feedback.

***

### **Cell 10: Test with Complex Change**

```python
# Test Case 2: Complex security implementation
complex_change = """
# auth.py
import bcrypt
import jwt
import asyncio
from database import get_user_by_email, update_login_attempts
from datetime import datetime, timedelta

async def authenticate_user(email: str, password: str, request_ip: str):
    # Check rate limiting first
    login_attempts = await get_login_attempts(request_ip)
    if login_attempts > 5:
        raise SecurityException("Too many login attempts")
    
    user = await get_user_by_email(email)
    if not user:
        await update_login_attempts(request_ip, increment=True)
        return None
        
    # New secure password verification with timing attack protection
    if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
        # Generate JWT token with enhanced security
        payload = {
            'user_id': user.id,
            'email': user.email,
            'ip': request_ip,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        # Reset login attempts on success
        await update_login_attempts(request_ip, reset=True)
        return token
    else:
        await update_login_attempts(request_ip, increment=True)
        return None
"""

print("=== TESTING COMPLEX CHANGE ===")
result = app.invoke({
    "code_changes": complex_change,
    "complexity_score": 0,
    "review_type": "",
    "final_review": ""
})

print(f"\n Final Results:")
print(f"Complexity Score: {result['complexity_score']}")
print(f"Review Type: {result['review_type']}")
print(f"\n Review Content:")
print(result['final_review'])
```

**Expected behavior**: High complexity score → Routes to Technical Reviewer → Detailed security, architecture, and performance analysis.

***

## **Why This Matters: LangGraph vs Alternatives**

### **Simple LLM Approach:**
```python
# What you'd get with a single LLM call
llm.invoke("Review this code: [code here]")
# Result: Generic review regardless of complexity
```

### **LangChain Sequential Approach:**
```python
# What you'd get with LangChain
chain = LLMChain(llm=llm, prompt=review_prompt)
chain.run(code=code_changes)
# Result: Same review depth for all code, no routing
```

### **LangGraph Approach:**
```python
# What we built
app.invoke({"code_changes": code, ...})
# Result: Intelligent analysis → Specialized routing → Context-aware review
```

***

## **Real-World Impact**

This system demonstrates **three core LangGraph advantages**:

1. ** Intelligent Routing**: Complexity-based decisions that simple chains can't make
2. ** Stateful Memory**: Context flows through the entire workflow  
3. ** Conditional Logic**: Adaptive behavior based on input characteristics

**For Development Teams:**
- **Saves senior developer time** on simple reviews
- **Ensures complex changes** get appropriate attention  
- **Maintains consistency** across all reviews
- **Scales effortlessly** as the team grows

***

## **Next Steps**

Want to extend this system? Try:

- **Adding more reviewer types** (security-focused, performance-focused)
- **Implementing feedback loops** (if review confidence is low, route to human)
- **Adding tools** (code analyzers, security scanners, test runners)
- **Building memory** (remember team coding standards, common issues)

The beauty of LangGraph is that adding these features means adding nodes and edges - the core architecture stays clean and modular.

***

**What's Next in the Series?**
In the next article, we'll add **real tools** to our agents (code analyzers, GitHub APIs, security scanners) and see how LangGraph handles **tool-calling workflows** with branching logic.

***


***