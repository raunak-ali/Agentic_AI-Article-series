# Install dependencies:
# pip install -qU langchain langgraph langchain-google-genai

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal
import re

# ✅ State Schema
class ReviewState(TypedDict):
    code_changes: str
    complexity_score: int
    review_type: str
    final_review: str

# ✅ Setup LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key="AIzaSyA6Y5IXAN3z5nDAOg9mmN5VIwzufwUREDg")

# ✅ Python Function Node - Complexity Analyzer
def analyze_complexity(state: ReviewState) -> ReviewState:
    """
    Analyzes code changes and returns complexity score
    Simple heuristic based on lines changed, keywords, file types
    """
    code = state["code_changes"]
    
    # Simple complexity scoring (0-10)
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
    
    # Documentation-only changes get low score
    if any(keyword in code.lower() for keyword in ['readme', 'documentation', 'comment', '# ']):
        score = max(0, score - 2)
    
    state["complexity_score"] = min(score, 10)  # Cap at 10
    return state

# ✅ Agent 1: Quick Reviewer (Junior/Mid-level focus)
quick_reviewer_prompt = """
You are a Quick Code Reviewer for simple changes. You focus on:
- Code style and formatting
- Basic functionality
- Documentation clarity
- Simple bug catches

Keep your review concise (2-3 bullet points) and encouraging. 
You're reviewing straightforward changes that don't need deep architectural analysis.
"""

quick_reviewer = create_react_agent(
    llm, 
    tools=[], 
    prompt=quick_reviewer_prompt
)

def quick_review_node(state: ReviewState) -> ReviewState:
    response = quick_reviewer.invoke({
        "messages": [("user", f"Review this code change:\n\n{state['code_changes']}\n\nFocus on style, basic functionality, and clarity.")]
    })
    
    state["review_type"] = "Quick Review"
    state["final_review"] = response["messages"][-1].content
    return state

# ✅ Agent 2: Technical Reviewer (Senior-level focus)
technical_reviewer_prompt = """
You are a Senior Technical Reviewer for complex changes. You focus on:
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
    response = technical_reviewer.invoke({
        "messages": [("user", f"Review this code change:\n\n{state['code_changes']}\n\nProvide thorough technical analysis focusing on architecture, performance, and security.")]
    })
    
    state["review_type"] = "Technical Review"
    state["final_review"] = response["messages"][-1].content
    return state

# ✅ Conditional Edge Logic
def route_to_reviewer(state: ReviewState) -> Literal["quick_review", "technical_review"]:
    """Route based on complexity score"""
    if state["complexity_score"] <= 3:
        return "quick_review"
    else:
        return "technical_review"

# ✅ Build the Graph
workflow = StateGraph(ReviewState)

# Add nodes
workflow.add_node("analyze_complexity", analyze_complexity)
workflow.add_node("quick_review", quick_review_node)
workflow.add_node("technical_review", technical_review_node)

# Set entry point
workflow.set_entry_point("analyze_complexity")

# Add conditional edges
workflow.add_conditional_edges(
    "analyze_complexity",
    route_to_reviewer,
    {
        "quick_review": "quick_review",
        "technical_review": "technical_review"
    }
)

# Both reviewers end the workflow
workflow.add_edge("quick_review", END)
workflow.add_edge("technical_review", END)

# Compile the graph
app = workflow.compile()

# ✅ Test the System
def test_code_review_system():
    # Test Case 1: Simple documentation change
    simple_change = """
    # README.md
    ## Installation
    
    ```
    pip install our-package
    ```
    
    ## Usage
    Updated usage examples with clearer variable names.
    """
    
    print("=== SIMPLE CHANGE TEST ===")
    result = app.invoke({
        "code_changes": simple_change,
        "complexity_score": 0,
        "review_type": "",
        "final_review": ""
    })
    
    print(f"Complexity Score: {result['complexity_score']}")
    print(f"Review Type: {result['review_type']}")
    print(f"Review:\n{result['final_review']}")
    print("\n" + "="*50 + "\n")
    
    # Test Case 2: Complex security change
    complex_change = """
    # auth.py
    import bcrypt
    import jwt
    from database import get_user_by_email
    
    async def authenticate_user(email: str, password: str):
        user = await get_user_by_email(email)
        if not user:
            return None
            
        # New secure password verification
        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            # Generate JWT token with enhanced security
            payload = {
                'user_id': user.id,
                'email': user.email,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }
            return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return None
    """
    
    print("=== COMPLEX CHANGE TEST ===")
    result = app.invoke({
        "code_changes": complex_change,
        "complexity_score": 0,
        "review_type": "",
        "final_review": ""
    })
    
    print(f"Complexity Score: {result['complexity_score']}")
    print(f"Review Type: {result['review_type']}")
    print(f"Review:\n{result['final_review']}")

# Run the test
if __name__ == "__main__":
    test_code_review_system()
