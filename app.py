import streamlit as st
import random
import plotly.graph_objects as go

st.set_page_config(page_title="模拟投注系统", layout="wide")

st.title("🎰 模拟投注回测系统")

# =========================
# 登录系统（简化）
# =========================
if "user" not in st.session_state:
    st.session_state.user = ""

if st.session_state.user == "":
    name = st.text_input("请输入用户名")
    if st.button("登录"):
        if name.strip():
            st.session_state.user = name
            st.rerun()
    st.stop()

st.success(f"欢迎：{st.session_state.user}")

# =========================
# 参数设置
# =========================
bankroll = st.number_input("💰 初始资金", value=1000)
win_rate = st.slider("🎯 胜率", 0.0, 1.0, 0.5)
odds = st.number_input("⚖️ 赔率", value=2.0)
rounds = st.number_input("🔁 投注局数", value=100)
base_bet = st.number_input("🔢 初始下注", value=10)

strategy = st.selectbox("策略选择", ["固定", "马丁", "随机"])

# =========================
# 模拟逻辑
# =========================
if st.button("🚀 开始模拟"):

    balance = bankroll
    bet = base_bet
    history = []

    for _ in range(int(rounds)):

        if balance <= 0:
            break

        win = random.random() < win_rate

        # 策略
        if strategy == "固定":
            current_bet = base_bet

        elif strategy == "马丁":
            current_bet = bet

        else:
            current_bet = random.uniform(base_bet * 0.5, base_bet * 1.5)

        current_bet = min(current_bet, balance)

        if win:
            balance += current_bet * odds - current_bet
            if strategy == "马丁":
                bet = base_bet
        else:
            balance -= current_bet
            if strategy == "马丁":
                bet *= 2

        history.append(balance)

    # =========================
    # 曲线图
    # =========================
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=history, name="资金曲线"))
    fig.update_layout(
        title="📊 资金变化曲线",
        xaxis_title="局数",
        yaxis_title="资金"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.success(f"最终资金：{balance:.2f}")