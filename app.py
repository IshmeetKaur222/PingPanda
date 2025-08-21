import streamlit as st
import speedtest
import plotly.graph_objects as go

st.set_page_config(page_title="PingPanda 🐼 WiFi Speed Meter", layout="wide")

# 🐼 Title & Panda Intro
st.title("🐼 PingPanda — WiFi Speed Meter 📶")

st.markdown("""
<div style='display: flex; align-items: center; margin-top: 1rem;'>
    <span style='font-size: 28px; margin-right: 10px;'>🐼</span>
    <div style='background-color: #f1f1f1; padding: 10px 16px; border-radius: 12px; font-size: 16px; max-width: 600px;'>
        Hi! I'm <strong>PingPanda</strong> — let's check how your internet is doing today!
    </div>
</div>
""", unsafe_allow_html=True)

# 🚀 Speed Test Function
def test_speed():
    with st.spinner("Testing your internet speed... 🐾"):
        tester = speedtest.Speedtest()
        tester.get_best_server()
        download = tester.download() / 1_000_000  # Convert to Mbps
        upload = tester.upload() / 1_000_000      # Convert to Mbps
        ping = tester.results.ping
    return ping, download, upload

# 📊 Gauge Chart Function
def gauge_chart(label, value, max_value, unit, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': f"{label} ({unit})"},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, max_value * 0.5], 'color': "#d3f4ff"},
                {'range': [max_value * 0.5, max_value], 'color': "#a0e1ff"}
            ],
        }
    ))
    fig.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
    return fig

# 📏 Dynamic max value for better scale
def get_max_value(speed):
    if speed <= 50:
        return 100
    elif speed <= 500:
        return 1000
    else:
        return 2000

# 🔘 Run Test
if st.button("🐼 Run Speed Test"):
    ping, download, upload = test_speed()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(gauge_chart("Ping", ping, 150, "ms", "orange"), use_container_width=True)
    with col2:
        st.plotly_chart(gauge_chart("Download", download, get_max_value(download), "Mbps", "green"), use_container_width=True)
    with col3:
        st.plotly_chart(gauge_chart("Upload", upload, get_max_value(upload), "Mbps", "blue"), use_container_width=True)

    st.success("✅ Test complete!")
    st.markdown(f"""
    - **Ping**: `{ping:.2f}` ms  
    - **Download**: `{download:.2f}` Mbps  
    - **Upload**: `{upload:.2f}` Mbps  
    """)

# 👣 Footer
st.markdown("""
---
<div style='text-align: center; font-size: 14px; color: gray;'>
    Crafted by <strong>Codemates</strong> — Ishmeet & Aayush 💻🐼
</div>
""", unsafe_allow_html=True)
