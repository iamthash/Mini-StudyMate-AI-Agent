
import re
import torch
from transformers import pipeline


# --------------------------------------------------
# Load AI Model
# --------------------------------------------------

generator = pipeline(
    "text-generation",
    model="HuggingFaceTB/SmolLM2-1.7B-Instruct",
    device_map="auto",
    dtype="auto"
)


# --------------------------------------------------
# Calculator
# --------------------------------------------------

def calculator(expression):
    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return f"Calculator Result: {result}"

    except Exception:
        return "Sorry, I could not calculate that."


# --------------------------------------------------
# Concept Explainer
# --------------------------------------------------

def concept_explainer(topic):

    prompt = f"""
You are StudyMate, a helpful AI tutor.

Explain this topic to a beginner:

Topic: {topic}

Use this structure:

1. Simple definition
2. Easy explanation
3. Real-world example
4. Small technical example

Keep the explanation clear and beginner-friendly.
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = generator(
        messages,
        max_new_tokens=250
    )

    generated = response[0]["generated_text"]

    if isinstance(generated, list):
        return generated[-1]["content"]

    return generated


# --------------------------------------------------
# Study Planner
# --------------------------------------------------

def study_planner(subject):

    prompt = f"""
You are StudyMate, a helpful study planning assistant.

Create a simple 3-day study plan for:

Subject: {subject}

Use this structure:

Day 1:
- Learn the basic concepts

Day 2:
- Learn important concepts
- Practice

Day 3:
- Revise
- Practice questions
- Take a mini test

Keep the plan realistic and beginner-friendly.
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = generator(
        messages,
        max_new_tokens=250
    )

    generated = response[0]["generated_text"]

    if isinstance(generated, list):
        return generated[-1]["content"]

    return generated


# --------------------------------------------------
# Extract Calculation
# --------------------------------------------------

def extract_calculation(text):

    text = text.lower()

    for word in [
        "calculate",
        "solve",
        "what is",
        "what's",
        "please",
        "compute"
    ]:
        text = text.replace(word, "")

    expression = re.sub(
        r"[^0-9+\-*/().% ]",
        "",
        text
    )

    return expression.strip()


# --------------------------------------------------
# Choose Tool
# --------------------------------------------------

def choose_tool(user_input):

    text = user_input.lower()

    if any(word in text for word in [
        "study plan",
        "study schedule",
        "study timetable",
        "learning plan",
        "revision plan",
        "study planner"
    ]):
        return "PLANNER"

    if any(word in text for word in [
        "calculate",
        "solve",
        "compute",
        "add",
        "subtract",
        "multiply",
        "divide"
    ]):
        return "CALCULATOR"

    return "EXPLAINER"


# --------------------------------------------------
# Main StudyMate Agent
# --------------------------------------------------

def studymate_agent(user_input):

    tool = choose_tool(user_input)

    if tool == "CALCULATOR":

        expression = extract_calculation(user_input)

        if not expression:
            return "Please provide a mathematical expression."

        return calculator(expression)

    elif tool == "PLANNER":

        subject = user_input

        for phrase in [
            "create a study plan for",
            "make a study plan for",
            "give me a study plan for",
            "create a study schedule for",
            "make a study schedule for",
            "study plan for"
        ]:

            if phrase in subject.lower():

                subject = subject.lower().split(
                    phrase,
                    1
                )[1].strip()

                break

        return study_planner(subject)

    else:

        return concept_explainer(user_input)


# --------------------------------------------------
# Run Application
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 50)
    print("🤖 MINI STUDYMATE AI AGENT")
    print("=" * 50)

    print("""
I can help you with:

🧮 Mathematical calculations
📚 Technical concept explanations
📅 Study planning

Type 'exit' to stop.
""")

    while True:

        user_input = input("You: ").strip()

        if user_input.lower() == "exit":

            print("\nStudyMate: Goodbye! 👋")
            break

        if not user_input:

            print("\nStudyMate: Please enter a question.")
            continue

        result = studymate_agent(user_input)

        print("\nStudyMate:")
        print(result)

        print("\n" + "-" * 50)
