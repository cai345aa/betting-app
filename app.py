import streamlit as st
import random
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="PC28 AI V4", layout="wide")

st.title("🚀 PC28 AI专业分析系统 V4")

# =========================
# PC28生成
# =========================
def gen():
    nums = [random.randint(0,9) for _ in range(3)]
    total = sum(nums)

    size = "大" if total >= 14 else "小"
    odd = "单" if total % 2 == 1 else "双"

    combo = size + odd
    return total, size, odd, combo

# =========================
# AI预测（升级版）
# =========================
def ai_predict(history):
    if len(history) < 10:
        return "大", 0.5

    last = history[-20:]

    big = sum(1 for x in last if x[1] == "大")
    small = len(last) - big

    odd = sum(1 for x in last if x[2] == "单")
    even = len(last) - odd

    # 趋势判断
    if big > small:
        pred = "大"
        conf = big / len(last)
    else:
        pred = "小"
        conf = small / len(last)

    return pred, round(conf, 2)

# =========================
# 参数
# =========================
balance = st.number_input("💰 初始资金", value=1000)
bet = st.number_input("🔢 每次下注", value=10)
rounds = st.number_input("🔁 模拟局数", value=100)

# =========================
# 启动
# =========================
if st.button("🚀 开始V4分析"):

    history = []
    money = balance
    curve = []

    for _ in range(int(rounds)):

        total, size, odd, combo = gen()
        history.append((total, size, odd, combo))

        # 简单下注逻辑（AI）
        pred, _ = ai_predict(history)

        win = (pred == size)

        if win:
            money += bet
        else:
            money -= bet

        curve.append(money)

    # =========================
    # AI预测
    # =========================
    pred, conf = ai_predict(history)

    st.subheader("🧠 AI预测结果")
    st.write(f"预测方向：{pred}")
    st.write(f"置信度：{conf}")

    # =========================
    # 最近记录
    # =========================
    st.subheader("📊 最近20期")

    for h in history[-20:]:
        st.write(f"和:{h[0]} | {h[1]} | {h[2]} | {h[3]}")

    # =========================
    # 资金曲线
    # =========================
    st.subheader("📈 资金曲线")

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=curve, name="资金"))
    st.plotly_chart(fig, use_container_width=True)

    st.success(f"最终资金：{money:.2f}")