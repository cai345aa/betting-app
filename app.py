import streamlit as st
import random
from collections import Counter

st.set_page_config(page_title="PC28专业预测平台", layout="wide")

st.title("🧠 PC28专业预测平台（纯分析版）")

# =========================
# 模拟历史数据（替代真实数据）
# =========================
def generate_history(n=100):
    data = []
    for _ in range(n):
        nums = [random.randint(0, 9) for _ in range(3)]
        total = sum(nums)

        size = "大" if total >= 14 else "小"
        odd = "单" if total % 2 == 1 else "双"

        data.append((total, size, odd))
    return data

history = generate_history(200)

# =========================
# AI预测核心
# =========================
def predict(history):

    last = history[-20:]

    size_count = Counter([x[1] for x in last])
    odd_count = Counter([x[2] for x in last])

    # 大小预测
    if size_count["大"] > size_count["小"]:
        size_pred = "大"
        size_conf = size_count["大"] / 20
    else:
        size_pred = "小"
        size_conf = size_count["小"] / 20

    # 单双预测
    if odd_count["单"] > odd_count["双"]:
        odd_pred = "单"
        odd_conf = odd_count["单"] / 20
    else:
        odd_pred = "双"
        odd_conf = odd_count["双"] / 20

    return size_pred, round(size_conf, 2), odd_pred, round(odd_conf, 2)

# =========================
# 页面展示
# =========================

st.subheader("📊 最近20期走势")

for h in history[-20:]:
    st.write(f"和:{h[0]} | {h[1]} | {h[2]}")

# =========================
# AI预测
# =========================
size_pred, size_conf, odd_pred, odd_conf = predict(history)

st.subheader("🧠 AI预测结果")

st.write(f"🎯 大小预测：{size_pred}（概率 {size_conf}）")
st.write(f"🎯 单双预测：{odd_pred}（概率 {odd_conf}）")

# =========================
# 趋势分析
# =========================
last_10 = history[-10:]

big = sum(1 for x in last_10 if x[1] == "大")
small = 10 - big

st.subheader("📈 趋势分析（最近10期）")

st.write(f"大：{big} 次")
st.write(f"小：{small} 次")

if big > small:
    st.success("当前偏向：大走势")
else:
    st.success("当前偏向：小走势")

# =========================
# 连续性判断
# =========================
st.subheader("📉 连续性分析")

last_result = history[-1][1]

st.write(f"当前连出：{last_result}")

st.info("提示：若连续≥5次同一方向，可能出现反转概率上升")