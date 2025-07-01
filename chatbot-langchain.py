import streamlit as st
import json
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_ollama import OllamaLLM
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# -------------------------------
# ✅ Streamlit Setup
# -------------------------------
st.title("🛒 Supermarket Chatbot with Smart Preferences & Inventory")

# -------------------------------
# ✅ Fake Shop Inventory
# -------------------------------
shop_inventory = [
    {"name": "Banana", "brand": "FreshFarms", "price": 1.5, "offer": "Buy 1 Get 1 Free"},
    {"name": "Apple", "brand": "OrchardBest", "price": 2.0, "offer": "10% off"},
    {"name": "Orange", "brand": "CitrusGold", "price": 1.8, "offer": "None"},
    {"name": "Milk", "brand": "DairyPure", "price": 3.5, "offer": "Free Cookies with 2L"},
    {"name": "Bread", "brand": "BakersChoice", "price": 2.5, "offer": "5% off"},
    {"name": "Eggs", "brand": "FarmFresh", "price": 2.2, "offer": "None"},
    {"name": "Broccoli", "brand": "GreenLeaf", "price": 1.0, "offer": "None"},
    {"name": "Cabbage", "brand": "GreenLeaf", "price": 1.2, "offer": "5% off"},
    {"name": "Chicken", "brand": "MeatMaster", "price": 5.0, "offer": "20% off weekend only"},
    {"name": "Yogurt", "brand": "DairyPure", "price": 1.5, "offer": "Buy 2 Get 1 Free"},
    # ➕ Add more items here as needed!
]

# -------------------------------
# ✅ User input
# -------------------------------
input_txt = st.text_input("Ask Luna:")

# -------------------------------
# ✅ Session State
# -------------------------------
if "preferences" not in st.session_state:
    st.session_state.preferences = {"likes": [], "dislikes": []}

if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = ConversationBufferMemory(
        memory_key="history",
        input_key="input",
        return_messages=True
    )

# -------------------------------
# ✅ Main Chat Prompt Template
# -------------------------------
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are Luna, a friendly supermarket assistant. 

CRITICAL RULE: You can ONLY talk about general topics, greetings, and customer service.
You must NEVER mention specific product availability, prices, or inventory.
All inventory questions are handled by a separate system.

If someone asks about product availability, just say "Let me check our inventory system for you."

The conversation so far:
{history}"""),
    ("human", "{input}"),
])

# -------------------------------
# ✅ Preference Extractor Prompt Template
# -------------------------------
extractor_prompt = PromptTemplate.from_template("""
Extract the user's liked and disliked supermarket items from this message:
"{text}"

Return only valid JSON in this format:
{{
  "likes": [],
  "dislikes": []
}}

If there are no likes or dislikes, return empty lists.
""")

# -------------------------------
# ✅ LLM Setup
# -------------------------------
llm = OllamaLLM(model="mistral")

# -------------------------------
# ✅ Chains
# -------------------------------
chat_chain = LLMChain(
    llm=llm,
    prompt=chat_prompt,
    memory=st.session_state.chat_memory
)

extractor_chain = LLMChain(
    llm=llm,
    prompt=extractor_prompt
)

# -------------------------------
# ✅ Helper: Search inventory (improved)
# -------------------------------
def search_inventory(query):
    query = query.lower().strip()
    exact_matches = []
    similar_matches = []
    
    for item in shop_inventory:
        # Check for exact name match
        if query == item["name"].lower() or query in item["name"].lower():
            exact_matches.append(item)
        # Check for brand match
        elif query in item["brand"].lower():
            similar_matches.append(item)
    
    return exact_matches, similar_matches

# -------------------------------
# ✅ Helper: Extract item name from query (completely rewritten)
# -------------------------------
def extract_item_from_query(query):
    query_lower = query.lower().strip()
    
    # First priority: Check if any inventory item names are mentioned
    inventory_items = [item["name"].lower() for item in shop_inventory]
    for item_name in inventory_items:
        if item_name in query_lower:
            return item_name
    
    # Second priority: Check common variations/plurals
    item_variations = {
        "apples": "apple",
        "bananas": "banana", 
        "oranges": "orange",
        "eggs": "eggs",  # already plural in inventory
        "chickens": "chicken",
        "breads": "bread",
        "milks": "milk",
        "yogurts": "yogurt"
    }
    
    for variation, actual in item_variations.items():
        if variation in query_lower:
            return actual
    
    # Third priority: Check for common items not in our inventory
    common_items = [
        "mutton", "lamb", "beef", "pork", "fish", "salmon", "tuna",
        "rice", "pasta", "cheese", "butter", "tomato", "potato", "tomatoes", "potatoes",
        "onion", "carrot", "spinach", "lettuce", "onions", "carrots"
    ]
    
    for item in common_items:
        if item in query_lower:
            return item
    
    # If nothing specific found, return a generic message indicator
    return "item you asked about"

# -------------------------------
# ✅ Helper: Check if it's an inventory query (more precise)
# -------------------------------
def is_inventory_question(text):
    text_lower = text.lower()
    
    # Check for clear inventory question patterns
    inventory_patterns = [
        "do you have", "do you sell", "do you carry", "is there",
        "available", "in stock", "got any", "any ", "have you got",
        "price of", "cost of", "how much", "sell "
    ]
    
    # Only treat as inventory question if it has clear question patterns
    has_inventory_pattern = any(pattern in text_lower for pattern in inventory_patterns)
    
    if has_inventory_pattern:
        return True
    
    # Also check for standalone product names that are clearly asking about availability
    # But only if they seem like questions (have ?, or are very short)
    product_names = [
        "banana", "apple", "orange", "milk", "bread", "eggs", 
        "broccoli", "cabbage", "chicken", "yogurt", "mutton", 
        "lamb", "beef", "pork", "fish", "meat"
    ]
    
    # If it's a short query with just a product name and question mark, treat as inventory
    if "?" in text_lower and len(text_lower.split()) <= 3:
        return any(product in text_lower for product in product_names)
    
    return False

# -------------------------------
# ✅ Run if input provided
# -------------------------------
if input_txt:
    lowered = input_txt.lower()

    # Check for preference queries first
    if "what items do i like" in lowered:
        st.write("✅ You like:", ", ".join(st.session_state.preferences["likes"]) or "None yet.")
    elif "what items do i not like" in lowered or "what items don't i like" in lowered:
        st.write("❌ You don't like:", ", ".join(st.session_state.preferences["dislikes"]) or "None yet.")
    
    # Check if it's an inventory question - HANDLE DIRECTLY, DON'T USE LLM
    elif is_inventory_question(input_txt):
        st.write("🔍 **Checking our inventory system...**")
        
        # Extract the item name from the query
        item_query = extract_item_from_query(input_txt)
        
        if item_query:  # Only search if we extracted something meaningful
            exact, similar = search_inventory(item_query)
            
            if exact:
                st.write(f"✅ **Yes! We have {item_query.title()} available:**")
                for item in exact:
                    st.write(f"• **{item['name']}** ({item['brand']}) - **${item['price']:.2f}**")
                    if item["offer"] and item["offer"].lower() != "none":
                        st.write(f"  🎉 **Special Offer:** {item['offer']}")
            elif similar:
                st.write(f"🤔 **We don't have '{item_query}' exactly, but we have these similar items:**")
                for item in similar:
                    st.write(f"• **{item['name']}** ({item['brand']}) - **${item['price']:.2f}**")
                    if item["offer"] and item["offer"].lower() != "none":
                        st.write(f"  🎉 **Special Offer:** {item['offer']}")
            else:
                st.write(f"❌ **Sorry, we don't have '{item_query}' in our store.**")
                st.write(f"📝 **Here's what we do have:** {', '.join([item['name'] for item in shop_inventory])}")
        else:
            # For unclear inventory questions, still check inventory but be more general
            st.write("❓ **Could you be more specific about what item you're looking for?**")
            st.write(f"📝 **Available items:** {', '.join([item['name'] for item in shop_inventory])}")
        
        # IMPORTANT: Don't let the query reach the LLM for inventory questions
        # We've handled it completely above
    
    else:
        # ✅ Normal chat for everything else - this includes preference extraction
        response = chat_chain.run(input=input_txt)
        st.write("Luna:", response)

        # ✅ Extract likes/dislikes for non-inventory questions
        try:
            extractor_result = extractor_chain.run(text=input_txt)
            extracted = json.loads(extractor_result)
            likes = extracted.get("likes", [])
            dislikes = extracted.get("dislikes", [])

            # Add new preferences and show them if found
            new_likes = []
            new_dislikes = []
            
            for item in likes:
                if item not in st.session_state.preferences["likes"]:
                    st.session_state.preferences["likes"].append(item)
                    new_likes.append(item)

            for item in dislikes:
                if item not in st.session_state.preferences["dislikes"]:
                    st.session_state.preferences["dislikes"].append(item)
                    new_dislikes.append(item)
            
            # Show what preferences were detected
            if new_likes:
                st.info(f"📝 Added to your likes: {', '.join(new_likes)}")
            if new_dislikes:
                st.info(f"📝 Added to your dislikes: {', '.join(new_dislikes)}")

        except Exception as e:
            # Silently handle JSON parsing errors for preference extraction
            pass

# -------------------------------
# ✅ Show stored preferences
# -------------------------------
st.sidebar.header("Your Preferences")
st.sidebar.write("👍 **Likes:**", st.session_state.preferences["likes"] or "None yet")
st.sidebar.write("👎 **Dislikes:**", st.session_state.preferences["dislikes"] or "None yet")

# -------------------------------
# ✅ Show available inventory
# -------------------------------
st.sidebar.header("🛒 Available Items")
with st.sidebar.expander("View All Items"):
    for item in shop_inventory:
        st.write(f"• **{item['name']}** ({item['brand']}) - ${item['price']:.2f}")
        if item["offer"] and item["offer"].lower() != "none":
            st.write(f"  🎉 {item['offer']}")

# -------------------------------
# ✅ Optional: Clear buttons
# -------------------------------
if st.sidebar.button("🔄 Clear Preferences"):
    st.session_state.preferences = {"likes": [], "dislikes": []}
    st.success("Preferences cleared!")

if st.sidebar.button("🧹 Clear Chat Memory"):
    st.session_state.chat_memory.clear()
    st.success("Chat memory cleared!")