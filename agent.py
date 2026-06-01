import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY nahi mili!")
    exit()

client = genai.Client(api_key=api_key)

# --- 🛠️ AGENT KA TOOL (FUNCTION) ---
def save_listing_to_file(filename: str, content: str) -> str:
    """Saves the generated Etsy listing content into a local text file."""
    try:
        # File ka naam safe karne ke liye spaces remove kar dete hain
        safe_filename = filename.replace(" ", "_").lower() + "_listing.txt"
        with open(safe_filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Success: Listing saved successfully to '{safe_filename}'!"
    except Exception as e:
        return f"❌ Failed to save file: {str(e)}"

SYSTEM_PROMPT = """
You are an expert E-commerce Agent. Your job is to create SEO-optimized listings.
CRITICAL RULE: After generating the title, tags, and description, you MUST immediately call the 'save_listing_to_file' tool to save this information for the user. Do not ask for permission, just do it.
"""

def run_smart_agent(product_idea):
    print(f"\n🚀 Agent processing: '{product_idea}'...")
    
    # Tool ko agent ke sath register karna
    my_tools = [save_listing_to_file]
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Generate and automatically save an Etsy listing for: {product_idea}",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=my_tools, # Agent ko tool de diya
            temperature=0.5
        )
    )
    
    # Check if the agent decided to call our tool
    if response.function_calls:
        print("🤖 Agent decided to use a tool!")
        for call in response.function_calls:
            if call.name == "save_listing_to_file":
                # Execute the tool using the arguments provided by Gemini
                args = call.args
                tool_output = save_listing_to_file(filename=args["filename"], content=args["content"])
                print(tool_output)
    else:
        print("📝 Agent Output:\n", response.text)

if __name__ == "__main__":
    print("--- 🤖 Etsy Auto-Save Agent Active ---")
    user_input = "Handmade Flower Sticker Pack for Journals"
    run_smart_agent(user_input)