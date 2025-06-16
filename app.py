# # Page config MUST be first
# import streamlit as st
# st.set_page_config(
#     page_title="ElevenLabs Voice Agent",
#     page_icon="🎙️",
#     layout="wide"
# )
 
# import os
# import threading
# import queue
# import time
# from dotenv import load_dotenv
# from elevenlabs.client import ElevenLabs
# from elevenlabs.conversational_ai.conversation import Conversation
# from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
 
# # Load environment variables
# load_dotenv()
# api_key = os.getenv("ELEVENLABS_API_KEY")
# agent_id = os.getenv("AGENT_ID")
 
# # Global resources - persistent across reruns
# @st.cache_resource
# def get_message_queue():
#     return queue.Queue()
 
# @st.cache_resource
# def get_stop_flag():
#     return threading.Event()
 
# @st.cache_resource
# def get_conversation_data():
#     return {
#         'thread': None,
#         'conversation': None,
#         'is_running': False
#     }
 
# # Initialize global resources
# msg_queue = get_message_queue()
# stop_flag = get_stop_flag()
# conv_data = get_conversation_data()
 
# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "ui_is_running" not in st.session_state:
#     st.session_state.ui_is_running = False
 
# # Auto-refresh mechanism
# placeholder = st.empty()
 
# def process_queue_messages():
#     """Process all messages from queue and add to session state"""
#     new_messages = []
#     try:
#         while not msg_queue.empty():
#             role, message = msg_queue.get_nowait()
#             new_messages.append((role, message))
#     except queue.Empty:
#         pass
    
#     if new_messages:
#         st.session_state.messages.extend(new_messages)
#         return True
#     return False
 
# # Conversation handler
# def run_conversation():
#     """Main conversation thread function"""
#     try:
#         elevenlabs = ElevenLabs(api_key=api_key)
        
#         def on_user(text):
#             print(f"[USER] {text}")
#             msg_queue.put(("User", text))
            
#         def on_response(resp):
#             print(f"[AGENT] {resp}")
#             msg_queue.put(("Agent", resp))
            
#         def on_correction(original, corrected):
#             print(f"[CORRECTION] {corrected}")
#             msg_queue.put(("Agent", f"*[Corrected]* {corrected}"))
 
#         # Create conversation
#         conversation = Conversation(
#             elevenlabs,
#             agent_id,
#             requires_auth=bool(api_key),
#             audio_interface=DefaultAudioInterface(),
#             callback_user_transcript=on_user,
#             callback_agent_response=on_response,
#             callback_agent_response_correction=on_correction
#         )
        
#         conv_data['conversation'] = conversation
#         msg_queue.put(("System", " **Starting conversation...** Please wait for confirmation."))
        
#         # Start the session
#         conversation.start_session()
#         msg_queue.put(("System", "**Conversation active!** You can now speak into your microphone."))
        
#         # Keep conversation alive
#         while not stop_flag.is_set():
#             time.sleep(0.1)
            
#         # Clean shutdown
#         print("[SYSTEM] Stopping conversation...")
#         msg_queue.put(("System", "**Ending conversation...**"))
        
#         conversation.end_session()
#         conv_id = conversation.wait_for_session_end()
        
#         msg_queue.put(("System", f"**Conversation ended successfully!** (ID: {conv_id})"))
        
#     except Exception as e:
#         error_msg = f"**Conversation Error:** {str(e)}"
#         print(f"[ERROR] {error_msg}")
#         msg_queue.put(("Error", error_msg))
        
#     finally:
#         conv_data['conversation'] = None
#         conv_data['is_running'] = False
#         conv_data['thread'] = None
 
# # Main UI
# with placeholder.container():
#     st.title("ElevenLabs Voice Agent")
    
#     # Sync UI state with global state
#     if conv_data['is_running'] != st.session_state.ui_is_running:
#         st.session_state.ui_is_running = conv_data['is_running']
    
#     # Control buttons
#     col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
#     with col1:
#         if st.button("Start",
#                     disabled=st.session_state.ui_is_running,
#                     key="start_conv",
#                     help="Start voice conversation"):
#             if not conv_data['is_running']:
#                 stop_flag.clear()
#                 conv_data['is_running'] = True
#                 st.session_state.ui_is_running = True
                
#                 # Start conversation thread
#                 thread = threading.Thread(
#                     target=run_conversation,
#                     daemon=True,
#                     name="ConversationThread"
#                 )
#                 thread.start()
#                 conv_data['thread'] = thread
#                 st.rerun()
    
#     with col2:
#         if st.button("Stop",
#                     disabled=not st.session_state.ui_is_running,
#                     key="stop_conv",
#                     help="Stop voice conversation"):
#             if conv_data['is_running']:
#                 stop_flag.set()
#                 conv_data['is_running'] = False
#                 st.session_state.ui_is_running = False
                
#                 # Wait for thread to finish
#                 if conv_data['thread'] and conv_data['thread'].is_alive():
#                     conv_data['thread'].join(timeout=3)
                
#                 st.rerun()
    
#     with col3:
#         if st.button("Refresh", key="manual_refresh", help="Manually refresh messages"):
#             st.rerun()
    
#     with col4:
#         if st.button("Clear", key="clear_msgs", help="Clear all messages"):
#             st.session_state.messages = []
#             # Clear the queue too
#             while not msg_queue.empty():
#                 try:
#                     msg_queue.get_nowait()
#                 except queue.Empty:
#                     break
#             st.rerun()
    
#     # Status indicator
#     if st.session_state.ui_is_running:
#         st.success("**LIVE CONVERSATION** - Speak into your microphone!")
#         # st.info("Messages will appear below in real-time")
#     else:
#         st.info("**Ready** - Click 'Start' to begin voice conversation")
    
#     # Process new messages from queue
#     has_new_messages = process_queue_messages()
    
 
 
# if st.session_state.ui_is_running:
#     time.sleep(0.5)
#     st.rerun()
# elif msg_queue.qsize() > 0:
#     time.sleep(0.1)
#     st.rerun()













# Page config MUST be first
import streamlit as st
import logging

st.set_page_config(
    page_title="ElevenLabs Voice Agent",
    page_icon="🎙️",
    layout="wide"
)

import os
import threading
import queue
import time
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

# Configure detailed logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")
agent_id = os.getenv("AGENT_ID")
logger.info("Environment variables loaded.")

# Global resources
@st.cache_resource
def get_message_queue():
    logger.info("Initializing message queue.")
    return queue.Queue()

@st.cache_resource
def get_stop_flag():
    logger.info("Initializing stop flag.")
    return threading.Event()

@st.cache_resource
def get_conversation_data():
    logger.info("Initializing conversation data.")
    return {'thread': None, 'conversation': None, 'is_running': False}

# Initialize global resources
msg_queue = get_message_queue()
stop_flag = get_stop_flag()
conv_data = get_conversation_data()

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ui_is_running" not in st.session_state:
    st.session_state.ui_is_running = False

placeholder = st.empty()

def process_queue_messages():
    logger.info("Processing messages from queue.")
    new_messages = []
    try:
        while not msg_queue.empty():
            role, message = msg_queue.get_nowait()
            new_messages.append((role, message))
            logger.info(f"Queue message processed: [{role}] {message}")
    except queue.Empty:
        logger.info("Message queue empty.")

    if new_messages:
        st.session_state.messages.extend(new_messages)
        return True
    return False

def run_conversation():
    logger.info("Starting conversation thread.")
    try:
        elevenlabs = ElevenLabs(api_key=api_key)

        def on_user(text):
            logger.info(f"User input: {text}")
            msg_queue.put(("User", text))

        def on_response(resp):
            logger.info(f"Agent response: {resp}")
            msg_queue.put(("Agent", resp))

        def on_correction(original, corrected):
            logger.info(f"Correction from agent: {corrected}")
            msg_queue.put(("Agent", f"*[Corrected]* {corrected}"))

        conversation = Conversation(
            elevenlabs,
            agent_id,
            requires_auth=bool(api_key),
            audio_interface=DefaultAudioInterface(),
            callback_user_transcript=on_user,
            callback_agent_response=on_response,
            callback_agent_response_correction=on_correction
        )

        conv_data['conversation'] = conversation
        msg_queue.put(("System", " **Starting conversation...**"))
        logger.info("Conversation session initiating.")

        conversation.start_session()
        msg_queue.put(("System", "**Conversation active!**"))
        logger.info("Conversation session started successfully.")

        while not stop_flag.is_set():
            time.sleep(0.1)

        logger.info("Stopping conversation thread.")
        msg_queue.put(("System", "**Ending conversation...**"))

        conversation.end_session()
        conv_id = conversation.wait_for_session_end()
        logger.info(f"Conversation ended successfully with ID: {conv_id}")
        msg_queue.put(("System", f"**Conversation ended successfully!** (ID: {conv_id})"))

    except Exception as e:
        logger.error(f"Error during conversation: {e}")
        msg_queue.put(("Error", f"**Conversation Error:** {str(e)}"))

    finally:
        conv_data['conversation'] = None
        conv_data['is_running'] = False
        conv_data['thread'] = None
        logger.info("Conversation thread cleaned up.")

# Main UI
with placeholder.container():
    st.title("ElevenLabs Voice Agent")

    if conv_data['is_running'] != st.session_state.ui_is_running:
        st.session_state.ui_is_running = conv_data['is_running']
        logger.info(f"UI running state synchronized: {conv_data['is_running']}")

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        if st.button("Start", disabled=st.session_state.ui_is_running):
            if not conv_data['is_running']:
                stop_flag.clear()
                conv_data['is_running'] = True
                st.session_state.ui_is_running = True

                thread = threading.Thread(target=run_conversation, daemon=True)
                thread.start()
                conv_data['thread'] = thread
                logger.info("Start button clicked, conversation thread initiated.")
                st.rerun()

    with col2:
        if st.button("Stop", disabled=not st.session_state.ui_is_running):
            if conv_data['is_running']:
                stop_flag.set()
                conv_data['is_running'] = False
                st.session_state.ui_is_running = False

                if conv_data['thread'] and conv_data['thread'].is_alive():
                    conv_data['thread'].join(timeout=3)
                logger.info("Stop button clicked, conversation thread stopped.")
                st.rerun()

    with col3:
        if st.button("Refresh"):
            logger.info("Manual refresh triggered.")
            st.rerun()

    with col4:
        if st.button("Clear"):
            st.session_state.messages.clear()
            while not msg_queue.empty():
                msg_queue.get_nowait()
            logger.info("Messages cleared by user.")
            st.rerun()

    if st.session_state.ui_is_running:
        st.success("**LIVE CONVERSATION** - Speak into your microphone!")
    else:
        st.info("**Ready** - Click 'Start' to begin")

    process_queue_messages()

if st.session_state.ui_is_running or msg_queue.qsize() > 0:
    time.sleep(0.5)
    st.rerun()
 
 
 
    
 
