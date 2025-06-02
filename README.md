# 🚨 FBI Information Assistant Chatbot

An AI-powered chatbot that allows you to access official information from the FBI's wanted persons database.

## 🎯 Project Goals

This chatbot allows you to:
- Access the FBI's most wanted persons list
- Search for specific individuals by name
- Filter searches by criteria (gender, age, etc.)
- Get detailed information about wanted persons
- View the most wanted terrorists list
- Interact with FBI data through a natural conversational interface

## 📋 Prerequisites

- Python 3.9+ installed on your system
- Text editor or IDE (VS Code recommended)
- Internet connection for FBI API access
- Google AI Studio API key (free tier available)

## 🏗️ Project Architecture

```
FBI Information Assistant
├── frontend.py          # Streamlit user interface
├── backend.py           # AI logic and agent orchestration
├── tools.py             # Custom tools for FBI API
├── prompts.py           # System prompts and conversation templates
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
└── config.env          # Environment variables (API keys)
```

### 🧠 How It Works

1. **Frontend (`frontend.py`)**: Web interface created with [Streamlit](https://docs.streamlit.io/)
2. **Backend (`backend.py`)**: Orchestrates AI conversation using LangChain
3. **Tools (`tools.py`)**: Extends AI capabilities with FBI API access
4. **Memory System**: Remembers conversation context for natural dialogue
5. **Monitoring**: Tracks AI usage with Langfuse

## 🚀 Quick Start Guide

### Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

Create a `config.env` file and add your API keys:

```env
# Google AI Studio API Key (free tier available)
GOOGLE_AI_STUDIO_API_KEY=your_google_ai_key_here

# Langfuse keys for monitoring (optional)
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
```

**Getting API Keys:**
- Google AI Studio: Visit [ai.google.dev](https://ai.google.dev) to create a free API key
- Langfuse: Visit [langfuse.com](https://langfuse.com) for monitoring (optional)

### Step 3: Launch the Application

```bash
streamlit run frontend.py
```

Your chatbot will open in your browser at `http://localhost:8501`! 🎉

## 🔍 Available Features

### Integrated FBI Tools (Based on Real API Data)

1. **Most Wanted List (`get_fbi_most_wanted`)**
   - Retrieves the top 8 most wanted persons by the FBI
   - Shows status (ACTIVE/CAPTURED), rewards, warnings
   - Detailed information: FBI office, publication date, unique ID

2. **Search by Name (`search_fbi_person_by_name`)**
   - Complete search with detailed physical description
   - Personal information: birth dates, nationality, aliases
   - Physical data: height, weight, eye/hair color
   - Scars, distinctive marks, occupations

3. **Search by FBI Office (`search_fbi_by_field_office`)**
   - Filter by specific FBI office (e.g., "newyork", "losangeles")
   - Shows cases managed by geographic region
   - Information on rewards and status by office

4. **Search by Status (`search_fbi_by_status`)**
   - Filter by official status: "captured" (captured), "na" (active)
   - Track case evolution
   - Publication and update dates

5. **Search by Person Classification (`search_fbi_by_classification`)**
   - `main`: Main most wanted list
   - `vicap`: Violent Criminal Apprehension Program
   - `ecap`: Endangered Child Alert Program
   - `seeking-information`: Cases seeking information

6. **Search by Poster Classification (`get_fbi_by_poster_classification`)**
   - `default`: Standard wanted persons
   - `law-enforcement-assistance`: Law enforcement assistance
   - `missing`: Missing persons
   - `information`: Information seeking

7. **Complete Details (`get_fbi_person_details`)**
   - Comprehensive information by person ID
   - Complete physical description, criminal information
   - Security warnings, investigation details
   - Available resources (images, files)

8. **Terrorism List (`get_fbi_terrorism_list`)**
   - Cases related to terrorism and national security
   - Information on nationality and occupations
   - Special security warnings

9. **Advanced Search (`get_fbi_advanced_search`)**
   - Search with custom sorting options
   - Sort by: publication, title, subjects
   - Title filtering with pagination

### Real Data Exploited

**Complete Personal Information:**
- Full name, aliases, multiple birth dates
- Nationality, place of birth, languages spoken
- Occupations, geographic connections

**Detailed Physical Description:**
- Height (feet/inches), weight, build
- Eye/hair color (raw and formatted data)
- Scars, tattoos, distinctive marks
- Complexion, skin color

**Criminal Information:**
- Specific charges, investigation subjects
- NCIC numbers, arrest warrants
- Specialized security warnings
- Case details with context

**Investigation Data:**
- Responsible FBI offices, publication dates
- Current status (active, captured)
- Possible countries and states of location
- Rewards and specific amounts

### Official Filtering Parameters

The FBI API supports the following criteria:
- **`title`**: Name or part of person's name
- **`field_offices`**: FBI office (e.g., "newyork", "chicago", "miami")
- **`status`**: Case status ("captured", "na")
- **`person_classification`**: Classification type ("main", "vicap", "ecap")
- **`sort_on`**: Sort criteria ("publication", "title", "subjects")
- **`sort_order`**: Sort order ("asc", "desc")
- **`page`** and **`pageSize`**: Result pagination

### Usage Examples (Real Data)

**Basic searches:**
```
"Show me the FBI's most wanted persons list"
"Search for John Smith with all his information"
"Display the terrorism cases list"
```

**Filter by FBI office:**
```
"Search in the Cincinnati FBI office"
"Show me cases from the Miami office"
"Find wanted persons in Little Rock"
```

**Filter by official status:**
```
"Find recently captured suspects"
"Show me all active cases"
"Search for persons with 'captured' status"
```

**Filter by classification:**
```
"Show main list cases"
"Show me VICAP violent crime cases"
"Find Endangered Child Alert Program (ECAP) alerts"
"Search seeking-information cases"
```

**Poster classifications:**
```
"Show law enforcement assistance cases"
"Display missing persons"
"Find information seeking cases"
"Show standard wanted persons"
```

**Advanced searches with real data:**
```
"Advanced search sorted by recent publication date"
"Find 'Dixon' with all his physical information"
"Show results sorted alphabetically by title"
```

**Comprehensive information:**
```
"Give me all details for person ID d79f8572987541d2b4c9e4119b8dd444"
"Show the complete physical description of this person"
"Display security warnings and investigation details"
```

**Types of data retrieved:**
- **Real-time Status**: 🔴 ACTIVE / 🟢 CAPTURED
- **Physical Information**: Height (5'11"), weight (215 lbs), scars
- **Biographical Data**: Birth, nationality, aliases
- **Criminal Details**: Specific charges, security warnings
- **Investigation Context**: Responsible office, dates, rewards

## 🛠️ Understanding the Code

### Frontend Architecture (`frontend.py`)

The frontend uses **Streamlit** for the web interface:

```python
# Key Streamlit components:
st.chat_message()      # Chat bubbles
st.chat_input()        # User input field
st.sidebar.button()    # Reset functionality
st.session_state       # Persistent data storage
```

### Backend Architecture (`backend.py`)

The backend orchestrates AI conversations:

```python
class ChatBackend:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI()     # AI model
        self.tools = [get_fbi_tools]            # Available tools
        self.memory = ConversationBufferMemory() # Context memory
```

### Tool System (`tools.py`)

Tools extend AI capabilities:

```python
@tool
def get_fbi_most_wanted() -> str:
    """Gets the FBI's most wanted persons list"""
    # Your tool implementation here
```

## ⚠️ Important Considerations

### Security and Responsibility

- **Official Source**: Data comes from the official FBI API
- **Responsible Use**: Do not use for harassment or defamation
- **Reporting**: If you have information about a wanted person, contact authorities

### Emergency Contacts

- **FBI**: 1-800-CALL-FBI (1-800-225-5324)
- **Online Tips**: [tips.fbi.gov](https://tips.fbi.gov)
- **Local Emergency**: Contact your local police

### Available FBI Offices

**Main offices:**
- `newyork` - New York
- `losangeles` - Los Angeles
- `chicago` - Chicago
- `miami` - Miami
- `philadelphia` - Philadelphia
- `boston` - Boston
- `detroit` - Detroit
- `houston` - Houston
- `atlanta` - Atlanta
- `phoenix` - Phoenix
- `baltimore` - Baltimore
- `cleveland` - Cleveland

**Special Classifications:**
- `main` - Main most wanted list
- `vicap` - Violent Criminal Apprehension Program
- `ecap` - Endangered Child Alert Program
- `seeking-information` - Cases seeking public information

**Available Statuses:**
- `captured` - Captured persons
- `na` - Not applicable / Active cases

## 📊 **FBI Data Structure Exploited**

The chatbot fully exploits the richness of the official FBI API with **1053+ persons** in the database.

### 🔍 **Complete Personal Data**

**Example of real extracted data:**
```json
{
  "title": "DAVEONTE JAMES DIXON",
  "status": "captured",  // 🟢 CAPTURED or 🔴 ACTIVE
  "reward_text": "Reward of up to $25,000",
  "height_min": 73,     // 6'1"
  "weight": "215 pounds",
  "eyes_raw": "Brown",
  "hair_raw": "Black",
  "race_raw": "Black",
  "warning_message": "SHOULD BE CONSIDERED ARMED AND DANGEROUS",
  "field_offices": ["cincinnati"],
  "scars_and_marks": "Dixon has a tattoo on his left forearm"
}
```

### 📋 **Real Classification Types**

**Poster Classifications:**
- `law-enforcement-assistance`: Law enforcement assistance (Dixon, Hardin)
- `missing`: Missing persons (Fleming, Hatfield)
- `default`: Standard wanted persons (Martinez, Astorga)
- `information`: Information seeking (Pike, Panjaki)

**Person Classifications:**
- `Main`: Main most wanted list
- `Victim`: Victims in cases (Morgan)

### 🏢 **Active FBI Offices**

Offices with ongoing cases:
- `cincinnati`, `littlerock`, `neworleans`
- `miami`, `birmingham`, `sacramento`
- `charlotte`, `indianapolis`, `phoenix`

### ⚠️ **Real Security Warnings**

Official warning messages:
- "SHOULD BE CONSIDERED ARMED AND DANGEROUS"
- "SHOULD BE CONSIDERED ARMED AND DANGEROUS WITH VIOLENT TENDENCIES"
- "SHOULD BE CONSIDERED ARMED AND DANGEROUS AND AN ESCAPE RISK"

### 💰 **Current Rewards**

Real amounts offered by the FBI:
- **$75,000**: Emily Pike (murder)
- **$50,000**: Asha Jaquilla Degree (disappearance)
- **$25,000**: Daveonte James Dixon (attempted murder)
- **$20,000**: Grant Matthew Hardin (escape)

### 📅 **Temporal Data**

- **Publication**: Notice posting dates
- **Modification**: Last file updates
- **Timeline**: Cases from 1986 to 2025

### 🌍 **Geographic Data**

- **Possible Countries**: MEX, USA (Martinez)
- **Possible States**: US-AL, US-FL, US-TX (multi-state cases)
- **Coordinates**: Precise location when available

## 💡 **Complete Integration Benefits**

✅ **100% Official Data** - Direct FBI API source
✅ **Real-Time Information** - Updated status (captured/active)
✅ **Precise Physical Descriptions** - Height, weight, distinctive signs
✅ **Security Warnings** - Official FBI messages
✅ **Geolocation** - Responsible offices, possible states
✅ **Professional Classification** - Case types and priorities
✅ **Complete History** - From 1986 to today
✅ **Multilingual** - Files available in multiple languages

## 🔧 Customization

### Adding New Tools

To create a new FBI tool:

```python
@tool
def your_custom_tool(parameter: str) -> str:
    """Describes what your tool does.
    
    Args:
        parameter: Describes the input parameter
        
    Returns:
        A string with the tool's response
    """
    try:
        # Your API call here
        response = requests.get(f"https://api.fbi.gov/wanted/v1/{parameter}")
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

### Modify AI Personality

Edit `prompts.py` to change your AI's behavior:

```python
SYSTEM_PROMPT = """
You are an assistant specialized in FBI information...
[Your custom personality here]
"""
```

## 🌐 Useful Resources

- **[Streamlit Documentation](https://docs.streamlit.io/)**: Complete guide to building web apps
- **[FBI API](https://www.fbi.gov/wanted/api)**: Official FBI API documentation
- **[LangChain Documentation](https://python.langchain.com/)**: Framework for AI applications
- **[Google AI Studio](https://ai.google.dev)**: Free access to AI models

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**API key errors:**
- Check that your `config.env` file exists
- Verify API keys are correct
- Ensure no extra spaces in the file

**Streamlit won't start:**
```bash
# Check if port is available
streamlit run frontend.py
```

**FBI API errors:**
- The FBI API is public but may have rate limits
- Check your internet connection
- Some queries may take time

## 📝 Ethical Use

This chatbot is designed for:
- ✅ Accessing public FBI information
- ✅ Educating about wanted persons
- ✅ Facilitating information reporting to authorities

Do not use it for:
- ❌ Harassing or defaming individuals
- ❌ Illegal or unethical activities
- ❌ Spreading false information

---

**Legal Note**: This project uses the public FBI API and is intended for educational and informational purposes. Users are responsible for ethical and legal use of the information obtained.