import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="미분 입체파 아트", layout="wide")

st.title("🎨 수학 x 예술: 미분의 입체파적 재구성")
st.write("함수의 미분 계수(기울기)를 이용해 입체파 스타일의 디지털 아트를 생성합니다.")

# 1. 사이드바 설정 (수학적 파라미터 제어)
st.sidebar.header("수학 설정")
func_type = st.sidebar.selectbox("함수 선택", ["Sine Wave", "Polynomial", "Complex"])
num_fragments = st.sidebar.slider("파편 개수 (입체파 효과)", 20, 200, 100)
noise_level = st.sidebar.slider("추상화 정도", 0.1, 1.0, 0.3)

# 2. 함수 및 미분 정의
x = np.linspace(-5, 5, num_fragments)

if func_type == "Sine Wave":
    y = np.sin(x)
    y_prime = np.cos(x) # 미분값
elif func_type == "Polynomial":
    y = 0.1 * x**3 - 0.2 * x**2
    y_prime = 0.3 * x**2 - 0.4 * x
else:
    y = np.sin(x) * np.exp(-0.1 * x**2)
    y_prime = np.cos(x) * np.exp(-0.1 * x**2) - 0.2 * x * np.sin(x) * np.exp(-0.1 * x**2)

# 3. 입체파 아트 생성 (Matplotlib 활용)
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_facecolor('#f0f0f0')

for i in range(len(x)):
    # 각 지점의 미분값(y_prime)을 기울기로 하는 사각형 파편 생성
    angle = np.degrees(np.arctan(y_prime[i])) # 기울기를 각도로 변환
    
    # 입체파적 무작위성 추가
    width = np.random.uniform(0.5, 1.5)
    height = np.random.uniform(0.1, 0.5)
    
    # 미분값에 따른 색상 변화 (기울기가 클수록 진해짐)
    color_val = np.abs(y_prime[i]) / (np.max(np.abs(y_prime)) + 0.1)
    color = plt.cm.plasma(color_val)
    
    # 사각형 배치
    rect = patches.Rectangle(
        (x[i], y[i]), width, height, 
        angle=angle, 
        color=color, 
        alpha=0.6,
        edgecolor='black',
        linewidth=0.5
    )
    ax.add_patch(rect)

ax.set_xlim(-6, 6)
ax.set_ylim(min(y)-2, max(y)+2)
ax.axis('off')

# 4. 결과 출력
st.pyplot(fig)

st.info(f"💡 원리: 각 사각형의 기울기는 $x={x[0]:.2f}$부터 $x={x[-1]:.2f}$ 사이의 미분 계수 $f'(x)$를 반영합니다.")
