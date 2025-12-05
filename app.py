import streamlit as st
import google.generativeai as genai
from PIL import Image

# 页面基础设置
st.set_page_config(page_title="RenderMate", page_icon="🎨", layout="wide")

# 侧边栏配置
with st.sidebar:
    st.header("🔑 密钥配置")
    api_key = st.text_input("输入 Google API Key", type="password")
    st.markdown("---")
    st.header("📂 素材上传")
    uploaded_file = st.file_uploader("拖入你的渲染图", type=["jpg", "png", "jpeg"])
    target_vibe = st.text_input("目标风格 (可选)", placeholder="例如：赛博朋克，高级灰，自然光")
    go_btn = st.button("开始分析 (Analyze)", type="primary", use_container_width=True)

# 主界面
st.title("🎨 RenderMate: AI 美术指导")

col1, col2 = st.columns(2)

with col1:
    st.subheader("原始渲染 (WIP)")
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
    else:
        st.info("👈 请在左侧上传图片")

with col2:
    st.subheader("AI 诊断报告")
    if go_btn and uploaded_file and api_key:
        try:
            # 配置 AI
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            with st.spinner("🧠 正在分析光影与材质..."):
                prompt = f"""
                角色：你是一位资深的 Octane 渲染专家 (TD) 和美术指导。
                任务：分析这张图片。用户想要达到的风格是："{target_vibe}"。
                
                请用 Markdown 格式输出以下三部分建议：
                
                ### 1. 👁 视觉诊断 (Visual Critique)
                * 点评光影 (对比度, 曝光, HDRI)。
                * 点评材质 (真实感, 细节, 瑕疵)。
                * 点评构图。
                
                ### 2. 🛠 OC 技术修正 (Technical Fixes)
                * 给出具体的 C4D/Octane 操作步骤。
                * 必须使用专业术语 (如: **Dirt Node**, **ACES**, **Ray Epsilon**, **Cast Shadows**, **IOR**, **Dispersion**)。
                
                ### 3. 🎨 参考图提示词 (Visual Prompt)
                * 写一段高质量的英文 Prompt，描述这张图的完美状态。
                """
                
                response = model.generate_content([prompt, image])
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"发生错误: {e}")
            st.caption("请检查 API Key 是否正确，或者网络是否通畅。")
    elif go_btn and not api_key:
        st.warning("⚠️ 请先在左侧填入 API Key！")
