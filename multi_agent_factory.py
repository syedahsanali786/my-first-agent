import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Load Keys
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY nahi mili!")
    exit()

client = genai.Client(api_key=api_key)

# =====================================================================
# 🔍 AGENT 1: TREND RESEARCHER (Persona & Logic)
# =====================================================================
RESEARCHER_PROMPT = """
You are an expert E-commerce Trend Researcher. Your only job is to analyze a product idea and extract high-performing SEO keywords, search intent, and target audience insights.
Output your findings strictly as a clean bulleted list of keywords and insights. Do not write descriptions or titles.
"""

def run_researcher_agent(product_idea):
    print(f"🕵️‍♂️ [Researcher Agent] Analyzing market trends for: '{product_idea}'...")
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Analyze search trends and keywords for: {product_idea}",
            config=types.GenerateContentConfig(
                system_instruction=RESEARCHER_PROMPT,
                temperature=0.3 # Low temperature for accurate, factual data
            )
        )
        return response.text
    except Exception as e:
        return f"Researcher Error: {str(e)}"

# =====================================================================
# ✍️ AGENT 2: COPYWRITER (Persona & Logic)
# =====================================================================
COPYWRITER_PROMPT = """
You are a High-Converting E-commerce Copywriter and Digital Marketer. 
You will receive raw market research and keywords from the Researcher Agent. Your job is to turn that data into a premium Etsy listing.

Output exactly in this format:
- 🔥 **Premium Title** (packed with the provided keywords)
- 🎯 **13 Target SEO Tags**
- 📈 **Marketing Hook & Description** (written to maximize ROAS and conversions)
"""

def run_copywriter_agent(research_data):
    print("✍️ [Copywriter Agent] Manufacturing final listing using research data...")
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Convert this raw research data into a high-converting listing:\n{research_data}",
            config=types.GenerateContentConfig(
                system_instruction=COPYWRITER_PROMPT,
                temperature=0.7 # High temperature for creativity and marketing hooks
            )
        )
        return response.text
    except Exception as e:
        return f"Copywriter Error: {str(e)}"

# =====================================================================
# 🚀 THE AGENT FACTORY ORCHESTRATION (The Loop)
# =====================================================================
def start_agent_workforce(product_input):
    print("--- 🏭 AGENT FACTORY WORKFORCE ACTIVATED ---")
    
    # Step 1: Researcher apna kaam karega
    raw_research = run_researcher_agent(product_input)
    print("\n💡 [System] Research completed. Passing intelligence to Copywriter...")
    print("-" * 50)
    
    # Step 2: Copywriter Researcher ka data le kar final product banaye ga
    final_listing = run_copywriter_agent(raw_research)
    print("-" * 50)
    
    return final_listing

if __name__ == "__main__":
    # Example Target: Tumhare store ke liye naya product idea
    my_product = "Dark Tech Aesthetic Printable Journal 50 Pages"
    
    final_output = start_agent_workforce(my_product)
    print("\n🏆 Final Enterprise Output:\n")
    print(final_output)