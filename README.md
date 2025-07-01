# 🛒 Supermarket Chatbot with Smart Preferences & Inventory

A conversational AI assistant for supermarkets built with LangChain and Streamlit. This chatbot helps customers check product availability, learn about special offers, and remembers customer preferences for personalized service.

## 🌟 Features

- **Intelligent Product Search**: Quickly find items in the supermarket's inventory
- **Smart Preference Learning**: Remembers your likes and dislikes
- **Real-time Inventory Lookup**: Check product availability and prices
- **Special Offers Highlighting**: Never miss a deal with highlighted promotions
- **Conversational AI**: Natural language processing for human-like interactions
- **Responsive Web Interface**: Built with Streamlit for a smooth user experience

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Ollama with Mistral model installed locally

### Installation

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd supermarket-chatbot
   ```

2. Install the required packages:
   ```bash
   pip install streamlit langchain-core langchain-community langchain
   ```

3. Make sure you have Ollama installed and the Mistral model downloaded:
   ```bash
   ollama pull mistral
   ```

### Running the Application

1. Start the Streamlit application:
   ```bash
   streamlit run chatbot-langchain.py
   ```

2. Open your web browser and navigate to the URL provided in the terminal (usually `http://localhost:8501`)

## 🛠️ How It Works

### Core Components

1. **Chat Interface**
   - Built with Streamlit for a clean, interactive UI
   - Displays conversation history and user input
   - Shows available items and user preferences in the sidebar

2. **Inventory System**
   - In-memory product database with items, brands, prices, and special offers
   - Smart search functionality to find exact and similar matches
   - Real-time inventory status updates

3. **Preference Learning**
   - Tracks user likes and dislikes
   - Updates preferences based on conversation context
   - Persists preferences during the session

4. **Natural Language Processing**
   - Uses Mistral LLM through Ollama for conversation handling
   - Extracts product preferences from natural language
   - Understands various ways to ask about product availability

### Example Queries

- "Do you have bananas?"
- "What's the price of milk?"
- "I like apples and oranges"
- "I don't like broccoli"
- "What items do I like?"
- "Show me your special offers"

## 📚 Technical Details

### Dependencies

- `streamlit`: Web application framework
- `langchain-core`: Core LangChain functionality
- `langchain-community`: Community-maintained LangChain integrations
- `langchain`: LangChain framework for building LLM applications
- `ollama`: Local LLM server (runs Mistral model)

### Project Structure

```
supermarket-chatbot/
├── chatbot-langchain.py  # Main application file
├── README.md            # This file
└── requirements.txt     # Project dependencies
```

## 🛠️ Customization

### Adding New Products

To add new products to the inventory, modify the `shop_inventory` list in the code. Each product should be a dictionary with these keys:

```python
{
    "name": "Product Name",
    "brand": "Brand Name",
    "price": 9.99,
    "offer": "Special offer details or 'None'"
}
```

### Customizing Prompts

The chatbot's behavior can be modified by editing the prompt templates in the code:

1. `chat_prompt`: Controls the assistant's personality and conversation style
2. `extractor_prompt`: Defines how user preferences are extracted from messages

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://python.langchain.com/)
- Powered by [Mistral](https://mistral.ai/) via [Ollama](https://ollama.ai/)
- UI powered by [Streamlit](https://streamlit.io/)

---
