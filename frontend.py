"""
LXP - Advanced AI development Workshop: FBI Information Assistant frontend
"""

import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

# Import our backend logic
from backend import get_backend_instance
from prompts import INITIAL_MESSAGE, CHAT_INPUT_PLACEHOLDER

def setup_page():
    """
    Configure the Streamlit page with FBI theme.
    """
    st.set_page_config(
        page_title="FBI Information Assistant",
        page_icon="🚨",
        layout="wide"
    )
    
    # Header with FBI theme
    st.title("🚨 FBI Information Assistant")
    st.subheader("Access Official FBI Wanted Persons Database")
    
    # Add FBI info boxes using columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🔍 **Search Database**\nFind wanted persons by name or criteria")
    
    with col2:
        st.info("📋 **Most Wanted Lists**\nAccess FBI's most wanted and terrorism lists")
    
    with col3:
        st.info("📄 **Detailed Information**\nGet comprehensive person details and alerts")
    

def setup_sidebar():
    """
    Create an FBI-themed sidebar with information and controls.
    """
    st.sidebar.header("🏛️ FBI Database Access")
    
    # FBI service info
    with st.sidebar.expander("🔍 What can I do?"):
        st.write("""
        I can help you access official FBI information:
        
        **Available searches:**
        - FBI Most Wanted list
        - Most Wanted Terrorists
        - Search by person name
        - Filter by FBI field office
        - Filter by status (captured, etc.)
        - Filter by classification type
        - Advanced search with sorting
        - Get detailed person information
        
        **Official Criteria Available:**
        - Field offices, Status, Classifications
        - Title search, Sorting options
        
        **Data Source:** Official FBI API
        """)
    
    # Quick examples
    with st.sidebar.expander("💡 Try These Examples"):
        st.write("""
        **Basic Searches:**
        - "Show me the FBI most wanted list"
        - "Search for John Smith"
        - "Show me the terrorism list"
        
        **Advanced Filtering:**
        - "Search by New York field office"
        - "Find captured suspects"
        - "Show main classification cases"
        - "Get law enforcement assistance cases"
        - "Find missing persons cases"
        - "Search with advanced options sorted by publication date"
        
        **Detailed Info:**
        - "Get details for person ID 12345"
        """)
    
    # Available field offices info
    with st.sidebar.expander("🏢 FBI Field Offices"):
        st.write("""
        **Major Field Offices:**
        - newyork, losangeles, chicago
        - miami, philadelphia, boston
        - detroit, houston, atlanta
        - phoenix, baltimore, cleveland
        
        **Special Cases:**
        - Missing persons cases
        - Law enforcement assistance
        - Seeking information cases
        """)
    
    # Classifications info  
    with st.sidebar.expander("📌 Case Classifications"):
        st.write("""
        **Poster Classifications:**
        - default: Standard wanted persons
        - law-enforcement-assistance: LE assistance cases
        - missing: Missing persons
        - information: Seeking information
        
        **Person Classifications:**
        - main: Most Wanted list
        - vicap: Violent crimes
        - ecap: Endangered children
        """)
    
    # Important notice
    with st.sidebar.expander("⚠️ Important Notice"):
        st.warning("""
        **If you have information about any wanted person:**
        
        🚨 Contact local law enforcement immediately
        📞 Call FBI: 1-800-CALL-FBI (1-800-225-5324)
        🌐 Submit tips: tips.fbi.gov
        
        This information is from official FBI sources.
        """)
    

def setup_chat_memory():
    """
    Set up conversation memory and history.
    """
    msgs = StreamlitChatMessageHistory()
    memory = ConversationBufferMemory(
        chat_memory=msgs, 
        return_messages=True, 
        memory_key="chat_history", 
        output_key="output"
    )
    return msgs, memory


def initialize_chat_if_needed(msgs):
    """
    Initialize the chat with a welcome message if needed.
    """
    if len(msgs.messages) == 0:
        msgs.add_ai_message(INITIAL_MESSAGE)
        st.session_state.steps = {}


def add_reset_button(msgs):
    """
    Add a reset button in the sidebar.
    """
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🔄 Reset Chat", help="Start a new conversation"):
        msgs.clear()
        msgs.add_ai_message(INITIAL_MESSAGE)
        st.session_state.steps = {}
        st.rerun()
    

def display_chat_messages(msgs):
    """
    Display chat messages with FBI-themed avatars.
    """
    avatars = {"human": "👤", "ai": "🚨"}
    
    for idx, msg in enumerate(msgs.messages):
        with st.chat_message(msg.type, avatar=avatars[msg.type]):
            # Show tool usage for AI messages
            if msg.type == "ai":
                display_intermediate_steps(idx)
            
            # Display the message content
            st.write(msg.content)


def display_intermediate_steps(message_index):
    """
    Display FBI tool usage with appropriate icons.
    """
    steps = st.session_state.steps.get(str(message_index), [])
    
    for step in steps:
        if step[0].tool == "_Exception":
            continue
        
        # FBI tool icons
        tool_icons = {
            "get_fbi_most_wanted": "📋",
            "search_fbi_person_by_name": "🔍", 
            "search_fbi_by_field_office": "🏢",
            "search_fbi_by_status": "📊",
            "search_fbi_by_classification": "🏷️",
            "get_fbi_person_details": "📄",
            "get_fbi_terrorism_list": "🔴",
            "get_fbi_by_poster_classification": "📌",
            "get_fbi_advanced_search": "🎯"
        }
        
        tool_name = step[0].tool
        icon = tool_icons.get(tool_name, "🔧")
        display_name = tool_name.replace('_', ' ').title().replace('Fbi', 'FBI')
        
        with st.status(f"{icon} {display_name}: {step[0].tool_input}", state="complete"):
            st.write("**Reasoning:**", step[0].log)
            st.write("**Result:**", step[1])


def handle_user_input(msgs, memory, backend):
    """
    Handle user input and generate AI response.
    """
    if prompt := st.chat_input(placeholder=CHAT_INPUT_PLACEHOLDER):
        # Display user message
        st.chat_message("human", avatar="👤").write(prompt)
        
        # Process through AI
        with st.chat_message("ai", avatar="🚨"):
            with st.spinner("🔍 Searching FBI database..."):
                st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
                executor = backend.create_agent_executor(memory)
                response = backend.process_message(prompt, executor, st_cb)
            
            # Display response
            st.write(response["output"])
            
            # Store tool usage steps
            st.session_state.steps[str(len(msgs.messages) - 1)] = response["intermediate_steps"]


def main():
    """
    Main function that runs the FBI Information Assistant app.
    """
    # Setup page
    setup_page()
    
    # Setup sidebar
    setup_sidebar()
    
    # Initialize backend and memory
    backend = get_backend_instance()
    msgs, memory = setup_chat_memory()
    
    # Initialize chat
    initialize_chat_if_needed(msgs)
    
    # Add controls
    add_reset_button(msgs)
    
    # Display conversation
    display_chat_messages(msgs)
    
    # Handle new input
    handle_user_input(msgs, memory, backend)


if __name__ == "__main__":
    main()