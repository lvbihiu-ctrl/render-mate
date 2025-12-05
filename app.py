import streamlit as st
import os
import subprocess
import sys

# --- 架构师的暴力安装脚本 Start ---
# 如果系统里找不到 AI 库，就当场强行安装，不再依赖 requirements.txt
try:
    import google.generativeai as genai
except ImportError:
    st.toast("正在初始化 AI 引擎，请稍候...", icon="⚙️")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generative-ai"])
    import google.generativeai as genai
# --- 架构师的暴力安装脚本 End ---

from PIL import Image

# 页面配置
st.set_page_config(page_title="RenderMate: AI Art Director", layout="wide", page_icon="🎨")

# 侧边栏
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Google API Key", type="password", help="Get yours at aistudio.google.com")
    
    st.divider()
    
    uploaded_file = st.file_uploader("Upload WIP Render", type=["jpg", "png", "jpeg"])
    target_vibe = st.text_input("Target Vibe / Style", placeholder="e.g. Cyberpunk, Moody, Clean Product Shot")
    
    analyze_btn = st.button("Analyze & Optimize", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("Designed by **RenderMate Architect**")

# 主界面
st.title("🎨 RenderMate: C4D & Octane Art Director")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Your Render (WIP)")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
    else:
        st.info("👈 Please upload an image from the sidebar.")

with col2:
    st.subheader("AI Director's Feedback")
    
    if analyze_btn and uploaded_file and api_key:
        try:
            # 配置 API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            # 构建 Prompt
            system_prompt = f"""
            You are a Senior 3D Technical Director specializing in Cinema 4D and Octane Render.
            Analyze the uploaded image. The user wants to achieve this style: "{target_vibe}".
            
            Provide output in 3 distinct Markdown sections:
            
            ### 1. 👁 Visual Critique (犀利点评)
            * Analyze Lighting (Contrast, Ratios, HDRI).
            * Analyze Materials (Realism, Imperfections, Index of Refraction).
            * Analyze Composition.
            
            ### 2. 🛠 Technical Fixes (OC 参数修正)
            * Provide specific, actionable steps. 
            * USE BOLD for specific Octane nodes/terms (e.g. **Dirt Node**, **ACES**, **Ray Epsilon**, **Cast Shadows**).
            * Be very technical and precise.
            
            ### 3. 🎨 Visual Reference Prompt (视觉参考)
            * Write a high-quality prompt that describes the PERFECT version of this image.
            """
            
            with st.spinner("🤖 AI Director is analyzing your render..."):
                response = model.generate_content([system_prompt, image])
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.warning("Please check your API Key and try again.")
            
    elif analyze_btn and not api_key:
        st.warning("Please enter your Google API Key in the sidebar first.")
