import streamlit as st
from src.langgraph_app import graph, validate_genre_and_get_movies, get_enhanced_movie_response
from src.memory import memory
from src.services.movie_service import get_available_genres, format_movie_recommendations

# Professional UI setup
st.set_page_config(
    page_title="Movie Recommendation Bot",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional styling with proper color contrast
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem 0;
        border-bottom: 2px solid #e5e7eb;
    }
    .conversation-container {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        color: #1f2937;
    }
    .user-message {
        background: #f3f4f6;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #3b82f6;
        color: #1f2937;
    }
    .bot-message {
        background: #f9fafb;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #10b981;
        color: #1f2937;
    }
    .status-box {
        background: #dbeafe;
        border: 1px solid #3b82f6;
        border-radius: 6px;
        padding: 0.75rem;
        margin: 1rem 0;
        color: #1e40af;
    }
    .input-container {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #1f2937;
    }
    .stTextInput > div > div > input {
        color: #1f2937 !important;
        background-color: #ffffff !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #6b7280 !important;
    }
    .stButton > button {
        color: #ffffff !important;
        background-color: #3b82f6 !important;
        border: none !important;
    }
    .stButton > button:hover {
        background-color: #2563eb !important;
    }
    .stMarkdown {
        color: #1f2937 !important;
    }
    .stSubheader {
        color: #1f2937 !important;
    }
    .stCaption {
        color: #6b7280 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<h1 class="main-header">🎬 Movie Recommendation System</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 Quick Actions")
    
    if st.button("🔄 Reset Session", type="primary"):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    st.subheader("🎭 Popular Genres")
    popular_genres = get_available_genres()
    
    for genre in popular_genres:
        if st.button(f"🎬 {genre}", key=f"genre_{genre}"):
            st.session_state.state = {"user_input": "", "message": "", "next": "ask_genre"}
            st.session_state.node = "validate_genre"
            st.session_state.state["user_input"] = genre
            st.rerun()
    
    st.markdown("---")
    st.subheader("ℹ️ System Info")
    st.info("Powered by LangGraph & Groq LLM")
    st.caption("Movie recommendations based on genre preferences")

# Main content area
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Initialize session state
    if "state" not in st.session_state:
        st.session_state.state = {"user_input": "", "message": "", "next": "ask_genre"}
        st.session_state.node = "ask_genre"
        st.session_state.conversation_history = []

    # Conversation container
    with st.container():
        st.markdown('<div class="conversation-container">', unsafe_allow_html=True)
        
        # Display conversation history
        for i, (role, message) in enumerate(st.session_state.conversation_history):
            if role == "user":
                st.markdown(f'<div class="user-message"><strong>You:</strong> {message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message"><strong>Movie Bot:</strong> {message}</div>', unsafe_allow_html=True)
        
        # Current conversation flow
        if st.session_state.node == "ask_genre":
            st.markdown('<div class="input-container">', unsafe_allow_html=True)
            st.subheader("🎭 Enter Movie Genre")
            st.caption("Please provide a movie genre to get personalized recommendations")
            
            available_genres = get_available_genres()
            genre_list = ", ".join(available_genres)
            
            user_input = st.text_input(
                "Movie Genre:",
                placeholder=f"e.g., {genre_list}...",
                key="input_ask",
                label_visibility="collapsed"
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🎬 Get Recommendations", type="primary", use_container_width=True):
                    if user_input:
                        st.session_state.state["user_input"] = user_input
                        st.session_state.node = "validate_genre"
                        st.session_state.conversation_history.append(("user", user_input))
                        st.rerun()
                    else:
                        st.error("Please enter a movie genre")
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.node == "validate_genre":
            genre = st.session_state.state.get("user_input", "").strip()
            is_valid, message = validate_genre_and_get_movies(genre)
            
            if not is_valid:
                st.error(f"❌ {message}")
                st.session_state.node = "retry"
                st.rerun()
            else:
                st.session_state.node = "respond"
                st.rerun()

        elif st.session_state.node == "retry":
            st.markdown('<div class="input-container">', unsafe_allow_html=True)
            st.warning("⚠️ Invalid genre. Please try again.")
            st.subheader("🎭 Enter Movie Genre")
            
            available_genres = get_available_genres()
            genre_list = ", ".join(available_genres)
            
            user_input = st.text_input(
                "Movie Genre:",
                placeholder=f"e.g., {genre_list}...",
                key="input_retry",
                label_visibility="collapsed"
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🎬 Get Recommendations", type="primary", use_container_width=True):
                    if user_input:
                        st.session_state.state["user_input"] = user_input
                        st.session_state.node = "validate_genre"
                        st.session_state.conversation_history.append(("user", user_input))
                        st.rerun()
                    else:
                        st.error("Please enter a movie genre")
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.node == "respond":
            last_genre = memory.get("last_genre", "Unknown")
            last_movies = memory.get("last_movies", [])
            
            # Get enhanced response from LLM
            recommendations = format_movie_recommendations(last_movies)
            enhanced_message = get_enhanced_movie_response(last_genre, recommendations)
            st.session_state.conversation_history.append(("bot", enhanced_message))
            
            # Display the response
            st.markdown(f'<div class="bot-message"><strong>Movie Bot:</strong> {enhanced_message}</div>', unsafe_allow_html=True)
            
            # Status information
            st.markdown('<div class="status-box">', unsafe_allow_html=True)
            st.markdown("**System Status:**")
            st.markdown(f"• 🎭 Last queried genre: **{last_genre}**")
            st.markdown(f"• 🎬 Movies found: **{len(last_movies)}**")
            st.markdown("• 🤖 LLM: **Groq (llama3-8b-8192)**")
            st.markdown("• 🔗 Framework: **LangGraph**")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Reset option
            if st.button("🔄 New Query", type="secondary"):
                st.session_state.node = "ask_genre"
                st.session_state.conversation_history = []
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
