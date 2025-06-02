# 🌤️ AI Weatherman Chatbot Workshop

Welcome to the Advanced AI Development Workshop! In this hands-on session, you'll learn how to build, customize, and extend an AI-powered chatbot using Python, Streamlit, and LangChain.

## 🎯 Workshop Goals

By the end of this workshop, you will:
- Understand the architecture of AI chatbot applications
- Learn how to use LangChain for AI agent development
- Build a working chatbot with tool integration
- Create your own custom tools (bonus points for multiple tools!)
- Deploy a chatbot UI with Streamlit

## 📋 Prerequisites

- Basic Python knowledge
- Python 3.9+ installed on your system
- Text editor or IDE (VS Code recommended)
- Internet connection for API access

## 🏗️ Project Architecture

Our chatbot follows a clean, modular architecture:

```
AI Weatherman Chatbot
├── frontend.py          # Streamlit UI and user interaction
├── backend.py           # AI logic, memory, and agent orchestration  
├── tools.py             # Custom tools (weather, and your additions!)
├── prompts.py           # System prompts and conversation templates
├── requirements.txt     # Python dependencies
└── config.env          # Environment variables (API keys)
```

### 🧠 How It Works

1. **Frontend (`frontend.py`)**: Uses [Streamlit](https://docs.streamlit.io/) to create a web interface
2. **Backend (`backend.py`)**: Orchestrates the AI conversation using LangChain
3. **Tools (`tools.py`)**: Extends AI capabilities beyond text (weather lookup, your custom tools!)
4. **Memory System**: Remembers conversation context for natural dialogue
5. **Monitoring**: Tracks AI usage and performance with Langfuse

## 🚀 Quick Start Guide

### Step 1: Clone and Navigate to Project

```bash
git clone https://github.com/mrodriguez2/advanced-ai-development-workshop.git
cd advanced-ai-development-workshop
```

### Step 2: Create Virtual Environment

A virtual environment keeps your project dependencies isolated and prevents conflicts.

#### 🪟 Windows
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

#### 🍎 macOS
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

#### 🐧 Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Copy the template file and add your API keys:

```bash
# Copy the template file
cp config.env.template config.env
```

Then edit `config.env` with your actual API keys:

```env
# Google AI Studio API Key (free tier available)
GOOGLE_AI_STUDIO_API_KEY=your_google_ai_key_here

# Langfuse keys for monitoring
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
```

**Getting API Keys:**
- Google AI Studio: Visit [ai.google.dev](https://ai.google.dev) and create a free API key
- Langfuse: Visit [langfuse.com](https://langfuse.com) for monitoring (optional)

### Step 5: Run the Application

```bash
streamlit run frontend.py
```

Your chatbot will open in your browser at `http://localhost:8501`! 🎉

## 📚 Understanding the Code

### Frontend Architecture (`frontend.py`)

The frontend uses **Streamlit** for the web interface:

```python
# Key Streamlit components:
st.chat_message()      # Chat bubbles
st.chat_input()        # User input field
st.sidebar.button()    # Reset functionality
st.session_state       # Persistent data storage
```

**Learn More**: [Streamlit Documentation](https://docs.streamlit.io/)

### Backend Architecture (`backend.py`)

The backend orchestrates AI conversations:

```python
class ChatBackend:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI()     # AI model
        self.tools = [get_weather]              # Available tools
        self.memory = ConversationBufferMemory() # Context memory
    
    def create_agent_executor(self):
        # Creates an AI agent that can use tools
        return ConversationalChatAgent.from_llm_and_tools(...)
```

### Tool System (`tools.py`)

Tools extend what your AI can do:

```python
@tool
def get_weather(city: str) -> str:
    """Get weather for a city using wttr.in API"""
    # Your tool implementation here
```

### Memory and Context

The chatbot remembers conversation history using LangChain's memory system:
- **ConversationBufferMemory**: Stores full conversation
- **StreamlitChatMessageHistory**: Integrates with Streamlit UI

## 🛠️ Workshop Challenges

### Challenge 1: Create Your Own Tool

Add a new tool to `tools.py`. Here are some ideas using [free APIs](https://free-apis.github.io/#/browse):

**Easy Tools:**
- 🎭 **Jokes**: Get random jokes from JokeAPI
- 🎲 **Random Facts**: Fetch interesting facts
- 🔤 **Word Definitions**: Dictionary API integration

**Medium Tools:**
- 📰 **News Headlines**: Current news from NewsAPI
- 💱 **Currency Converter**: Exchange rate lookup
- 🎬 **Movie Info**: OMDB API for movie details

**Advanced Tools:**
- 🌍 **Location Info**: Geocoding and location data
- 📊 **Stock Prices**: Financial data integration
- 🗺️ **Travel Info**: Distance and route calculation

### Challenge 2: Multi-Tool Integration

**Bonus Points**: Create a chatbot that uses multiple tools together!

Example: A travel assistant that combines:
- Weather for destination
- Currency conversion
- Local news/events
- Flight information

### Tool Template

```python
@tool
def your_custom_tool(parameter: str) -> str:
    """Describe what your tool does.
    
    Args:
        parameter: Describe the input parameter
        
    Returns:
        A string with the tool's response
    """
    try:
        # Your API call here
        response = requests.get(f"https://api.example.com/{parameter}")
        data = response.json()
        
        # Format and return results
        return f"Your formatted response: {data}"
        
    except Exception as e:
        return f"Error: {str(e)}"
```

**Don't forget to:**
1. Import your tool in `backend.py`
2. Add it to the tools list in `_setup_tools()`
3. Test it in the chat interface!

## 🔧 Customization Ideas

### Modify the AI Personality

Edit `prompts.py` to change how your AI behaves:

```python
SYSTEM_PROMPT = """
You are a helpful travel assistant specializing in...
[Your custom personality here]
"""
```

### Enhance the UI

Streamlit offers many customization options:
- Custom themes and styling
- Sidebar widgets and controls
- Charts and data visualization
- File upload capabilities

### Add Error Handling

Improve user experience with better error messages and fallbacks.

## 🌐 Useful Resources

- **[Streamlit Documentation](https://docs.streamlit.io/)**: Complete guide to building web apps
- **[Free APIs List](https://free-apis.github.io/#/browse)**: Hundreds of free APIs for your tools
- **[LangChain Docs](https://python.langchain.com/)**: AI application framework
- **[Google AI Studio](https://ai.google.dev)**: Free AI model access

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

**API key errors:**
- Check your `config.env` file exists
- Verify API keys are correct
- Ensure no extra spaces in the file

**Streamlit won't start:**
```bash
# Check if port is available
streamlit run frontend.py
```

## 📝 Workshop Submission

To showcase your work:

1. Create at least one custom tool
2. Test your chatbot thoroughly
3. Document your additions in this README

---

Happy coding!