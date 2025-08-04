
import streamlit as st
import speedtest
import plotly.graph_objects as go

st.set_page_config(page_title="WiFi Speed Meter", layout="wide")

def test_speed():
    st.status("Testing speed...", expanded=True)
    st.toast("Starting test...", icon="🔄")

    tester = speedtest.Speedtest()
    tester.get_best_server()
    download = tester.download() / 1_000_000  # Mbps
    upload = tester.upload() / 1_000_000      # Mbps
    ping = tester.results.ping
    return ping, download, upload

def gauge_chart(label, value, max_value, unit, color):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': f"{label} ({unit})"},
        gauge = {
            'axis': {'range': [None, max_value]},
            'bar': {'color': color},
            'steps' : [
                {'range': [0, max_value*0.5], 'color': "#d3f4ff"},
                {'range': [max_value*0.5, max_value], 'color': "#a0e1ff"}
            ],
        }
    ))
    fig.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
    return fig

st.title("📶 WiFi Speed Meter")
st.write("Check your internet speed in a stylish way")

if st.button("Run Speed Test"):
    ping, download, upload = test_speed()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(gauge_chart("Ping", ping, 150, "ms", "orange"), use_container_width=True)
    with col2:
        st.plotly_chart(gauge_chart("Download", download, 100, "Mbps", "green"), use_container_width=True)
    with col3:
        st.plotly_chart(gauge_chart("Upload", upload, 100, "Mbps", "blue"), use_container_width=True)

    st.success("✅ Test complete")
    st.markdown(f"""
        - **Ping**: `{ping:.2f}` ms  
        - **Download**: `{download:.2f}` Mbps  
        - **Upload**: `{upload:.2f}` Mbps  
    """)
