"""
LXP - Advanced AI development Workshop: FBI Chatbot backend
"""

import os
import tools
from typing import List, Dict, Any
from dotenv import load_dotenv

# LangChain imports - these handle the AI conversation logic
from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI

# Langfuse import - this handles AI conversation monitoring and analytics
from langfuse.callback import CallbackHandler

# Local imports - our custom prompts and tools
from prompts import SYSTEM_PROMPT, TOOLS_PROMPT

# Remove single-input tool validation from ConversationalChatAgent
ConversationalChatAgent._validate_tools = lambda *_, **__: ...

class ChatBackend:
    """
    Main backend class that handles all AI-related operations for FBI wanted persons lookup.
    
    This class encapsulates:
    - AI model setup
    - Conversation memory management
    - FBI API tool integration
    - Monitoring and analytics
    
    Why use a class?
    - Keeps related functionality together
    - Makes it easy to maintain state
    - Allows for easy testing and modification
    """
    
    def __init__(self):
        """
        Initialize the FBI chatbot backend with all necessary components.
        
        This method:
        1. Loads environment variables (API keys, etc.)
        2. Sets up monitoring with Langfuse
        3. Initializes the LLM model
        4. Prepares available FBI tools
        """
        # Load environment variables from config.env file
        # This keeps sensitive information like API keys out of the code
        load_dotenv("config.env")
        
        # Get the Google AI API key from environment variables
        # Never hardcode API keys in your code!
        self.api_key = os.getenv("GOOGLE_AI_STUDIO_API_KEY")
        
        # Initialize Langfuse for monitoring AI conversations
        # This helps track usage, costs, and performance
        self.langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
        self.langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
        self.langfuse_handler = self._setup_langfuse()
        
        # Initialize the AI model
        # We use Google's Gemini model here, but this could be swapped for others
        self.llm = self._setup_llm()
        
        # Set up available FBI tools the AI can use
        # Tools extend what the AI can do beyond just text generation
        self.tools = self._setup_tools()
    
    def _setup_langfuse(self) -> CallbackHandler:
        """
        Set up Langfuse monitoring for the AI conversations.
        
        Langfuse helps you:
        - Track conversation quality
        - Monitor API usage and costs
        - Debug issues with AI responses
        - Analyze user interactions
        
        Returns:
            CallbackHandler: Configured Langfuse handler
        """
        return CallbackHandler(
            # These keys allow Langfuse to track your AI usage
            # In production, these should come from environment variables too
            public_key=self.langfuse_public_key,
            secret_key=self.langfuse_secret_key,
            host="https://us.cloud.langfuse.com"
        )
    
    def _setup_llm(self) -> ChatGoogleGenerativeAI:
        """
        Initialize the Large Language Model (LLM).
        
        The LLM is the "brain" of our AI assistant. We're using Google's Gemini,
        but you could easily swap this for OpenAI's GPT, Anthropic's Claude, etc.
        
        Returns:
            ChatGoogleGenerativeAI: Configured AI model
        """
        return ChatGoogleGenerativeAI(
            api_key=self.api_key,
            model="gemini-2.5-flash-preview-05-20"  # Specific model version
        )
    
    def _setup_tools(self) -> List:
        """
        Set up FBI tools that the AI can use during conversations.
        
        Tools extend the AI's capabilities beyond text generation.
        FBI tools include:
        - FBI most wanted list lookup
        - Person search by name
        - Search by criteria (gender, age, race)
        - Person details by ID
        - Terrorism list lookup
        
        To add a new tool:
        1. Create the tool function in tools.py
        2. Import it at the top of this file
        3. Add it to the list returned here
        
        Returns:
            List: Available FBI tools for the AI agent
        """
        return [
            tools.get_fbi_most_wanted,              # Get FBI most wanted list
            tools.search_fbi_person_by_name,        # Search person by name
            tools.search_fbi_by_field_office_tool,  # Search by FBI field office
            tools.search_fbi_by_status_tool,        # Search by status (captured, etc.)
            tools.search_fbi_by_classification_tool, # Search by classification (main, vicap, etc.)
            tools.get_fbi_person_details_tool,      # Get detailed person info by ID
            tools.get_fbi_terrorism_list,           # Get terrorism list
            tools.get_fbi_by_poster_classification, # Search by poster classification
            tools.get_fbi_advanced_search,          # Advanced search with sorting
            # You can include additional tools here as needed:
            # search_by_reward_amount,
            # get_fugitive_alerts,
            # search_by_crime_date,
        ]
    
    def create_agent_executor(self, memory: ConversationBufferMemory) -> AgentExecutor:
        """
        Create the AI agent that can use FBI tools and maintain conversation context.
        
        This is where the magic happens! The agent:
        1. Receives user messages about FBI wanted persons
        2. Decides which FBI tools (if any) to use
        3. Uses tools to gather information from the FBI database
        4. Formulates a response based on FBI data and conversation history
        
        Args:
            memory: Conversation history to maintain context
            
        Returns:
            AgentExecutor: Configured AI agent ready to help with FBI inquiries
        """
        # Create the conversational agent
        # This agent knows how to use FBI tools and maintain conversation context
        chat_agent = ConversationalChatAgent.from_llm_and_tools(
            llm=self.llm,
            tools=self.tools,
            system_message=SYSTEM_PROMPT,  # Defines the AI's personality and behavior
            human_message=TOOLS_PROMPT,    # Instructions for how to use tools
            verbose=True  # Enables detailed logging (helpful for debugging)
        )
        
        # Create the executor that runs the agent
        # The executor handles the conversation flow and FBI tool usage
        executor = AgentExecutor.from_agent_and_tools(
            agent=chat_agent,
            tools=self.tools,
            memory=memory,
            return_intermediate_steps=True,  # Shows FBI tool usage in UI
            handle_parsing_errors=True,      # Gracefully handles AI mistakes
            verbose=True                     # Detailed logging
        )

        return executor
    
    def process_message(self, 
                       message: str, 
                       executor: AgentExecutor, 
                       streamlit_callback=None) -> Dict[str, Any]:
        """
        Process a user message about FBI wanted persons and generate an AI response.
        
        This is the main function that:
        1. Takes user input about FBI inquiries
        2. Runs it through the AI agent with FBI tools
        3. Returns the response and any intermediate steps
        
        Args:
            message: User's input message (FBI-related query)
            executor: The AI agent executor
            streamlit_callback: Optional callback for UI updates
            
        Returns:
            Dict containing the AI response and intermediate FBI tool steps
        """
        # Set up callbacks for monitoring and UI updates
        callbacks = [self.langfuse_handler]
        if streamlit_callback:
            callbacks.append(streamlit_callback)
        
        # Configure the execution
        config = RunnableConfig()
        config["callbacks"] = callbacks
        
        # Process the message through the AI agent
        # This is where the AI thinks, uses FBI tools, and generates a response
        response = executor.invoke(message, config)
        
        return response


def get_backend_instance() -> ChatBackend:
    """
    Factory function to get a ChatBackend instance.
    
    This function provides a clean way for the frontend to get a backend instance
    without needing to understand the initialization details.
    
    Returns:
        ChatBackend: Ready-to-use FBI chatbot backend instance
    """
    return ChatBackend()