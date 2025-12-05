import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="RenderMate: C4D & Octane Art Director",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling for Dark Mode & UI Polish ---
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    h1, h2, h3 {
        color: #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Controls ---
with st.sidebar:
    st.title("🎛️ RenderMate Control")
    st.markdown("---")
    
    # 1. API Key Input
    api_key = st.text_input(
        "Enter Google API Key", 
        type="password", 
        help="Get your key at aistudio.google.com"
    )
    
    # 2. File Uploader
    uploaded_file = st.file_uploader(
        "Upload WIP Render", 
        type=["jpg", "jpeg", "png"]
    )
    
    # 3. Target Vibe
    target_vibe = st.text_input(
        "Target Vibe / Style",
        placeholder="e.g., Cyberpunk, Photorealistic Interior, Ghibli Style..."
    )
    
    st.markdown("---")
    
    # 4. Action Button
    analyze_btn = st.button("🚀 Analyze & Optimize")

    st.markdown("### About")
    st.info(
        "This tool acts as a Senior Octane Render TD. "
        "It uses Gemini 1.5 Pro to critique lighting, composition, "
        "and suggests specific Octane/C4D settings."
    )

# --- Main App Logic ---
st.title("RenderMate: C4D & Octane Art Director")

# Layout Columns
col1, col2 = st.columns([1, 1])

if uploaded_file is not None:
    # Load Image
    image = Image.open(uploaded_file)
    
    # Display in Left Column
    with col1:
        st.subheader("🖼️ Your Render")
        st.image(image, use_container_width=True, caption="Current WIP")

    # Analysis Logic
    if analyze_btn:
        if not api_key:
            st.sidebar.error("⚠️ Please enter your Google API Key to proceed.")
        else:
            with col2:
                st.subheader("🤖 AI Art Director Feedback")
                status_placeholder = st.empty()
                status_placeholder.markdown("Validating credentials...")

                try:
                    # 1. Configure API
                    genai.configure(api_key=api_key)
                    
                    # 2. Set up the Model
                    model = genai.GenerativeModel('gemini-1.5-pro')

                    # 3. Construct System Prompt
                    style_context = f"The user is aiming for this style: '{target_vibe}'." if target_vibe else "The user has not specified a specific style, aim for photorealism or high-end artistic composition."
                    
                    prompt = f"""
                    You are a world-class Senior 3D Art Director and Octane Render Technical Director (TD). 
                    You are an expert in Cinema 4D, Octane Node Editor, ACES workflow, lighting theory, and photographic composition.

                    {style_context}

                    Analyze the provided image and output a critique in the following strict Markdown format:

                    ### 1. 👁️ Visual Critique
                    *   **Lighting:** Analyze contrast, hierarchy, exposure, and mood.
                    *   **Composition:** Rule of thirds, guiding lines, focal point clarity.
                    *   **Materials/Textures:** Realism, surface imperfections, scale.

                    ### 2. ⚙️ Technical Fixes (C4D & Octane)
                    *   Provide specific technical instructions. 
                    *   Mention specific Octane features (e.g., "Increase Specular Depth," "Use Octane Dirt Node for crevices," "Adjust Camera Imager Response," "Check Index of Refraction," "Enable ACES tone mapping").
                    *   Suggest lighting setups (e.g., "Add an HDRI with high contrast," "Use a Rim Light area light").

                    ### 3. 🎨 Prompt for Ref
                    *   Write a high-quality Midjourney/Stable Diffusion prompt that describes the *perfect* version of this scene. The user can use this to generate reference images for inspiration.
                    """

                    status_placeholder.markdown("🧠 Analyzing image pixels and lighting data...")
                    
                    # 4. Send to API
                    response = model.generate_content([prompt, image])
                    
                    # 5. Display Result
                    status_placeholder.empty() # Clear loading text
                    st.markdown(response.text)
                    st.success("Analysis Complete!")

                except Exception as e:
                    status_placeholder.empty()
                    st.error(f"An error occurred: {str(e)}")
                    st.warning("Please check your API Key and internet connection.")

else:
    # Empty State
    with col1:
        st.info("👈 Please upload an image in the sidebar to begin.")
    with col2:
        pass
