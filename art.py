import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 페이지 설정
st.set_page_config(page_title="미분 입체파 갤러리", layout="wide")

st.title("🎨 Cubism of Derivatives: 미분과 불연속의 예술")
st.markdown("""
이 프로그램은 함수의 **미분 계수(기울기)**를 분석하여 입체파 스타일의 파편으로 재구성합니다. 
- **뾰족한 부분(미분 불능)**이나 **급격한 변화**가 예술적으로 어떻게 표현되는지 관찰해보세요.
""")

# --- 사이드바: 수학적 설정 ---
st.sidebar.header("📐 함수 및 디자인 설정")

# 함수 선택 (미분 불가능한 함수 포함)
func_option = st.sidebar.selectbox(
    "함수 선택",
    ["Symmetric Sine (연속/미분가능)", 
     "Absolute Value (V자 - 미분불능점 존재)", 
     "Step Function (계단 - 불연속)", 
     "Polynomial (3차 함수)",
     "Spiky Wave (복합 함수)"]
)

num_shapes = st.sidebar.slider("파편 밀도", 50, 300, 150)
shape_type = st.sidebar.radio("파편 모양", ["Triangles (삼각형)", "Polygons (다각형)", "Mixed (혼합)"])
color_theme = st.sidebar.selectbox("색상 테마", ["magma", "viridis", "inferno", "coolwarm"])

# --- 수학 연산부 ---
x = np.linspace(-5, 5, num_shapes)
dx = x[1] - x[0]

# 함수 정의 및 수치 미분
if func_option == "Symmetric Sine (연속/미분가능)":
    y = np.sin(x)
elif func_option == "Absolute Value (V자 - 미분불능점 존재)":
    y = np.abs(x)
elif func_option == "Step Function (계단 - 불연속)":
    y = np.sign(x)
elif func_option == "Polynomial (3차 함수)":
    y = 0.1 * x**3 - x
else: # Spiky Wave
    y = np.sin(x) + 0.5 * np.sign(np.sin(2.0 * x))

# 수치적 미분 (중앙 차분법)
y_prime = np.gradient(y, dx)

# --- 시각화 (입체파 스타일) ---
fig, ax = plt.subplots(figsize=(12, 10))
ax.set_facecolor('#1e1e1e') # 어두운 배경으로 예술적 효과 극대화

for i in range(len(x)):
    # 미분 계수에 따른 각도와 색상 계산
    angle = np.degrees(np.arctan(y_prime[i]))
    color_val = np.clip(np.abs(y_prime[i]) / (np.max(np.abs(y_prime)) + 0.5), 0, 1)
    color = plt.get_cmap(color_theme)(color_val)
    
    # 미분 불가능하거나 급변하는 곳(기울기가 매우 큰 곳)에 효과 주기
    size_factor = 1.5 if np.abs(y_prime[i]) > 2 else 1.0
    
    # 도형 생성 (삼각형 또는 다각형)
    if shape_type == "Triangles (삼각형)":
        # 현재 좌표를 기준으로 기울어진 삼각형 생성
        points = np.array([
            [0, 0], 
            [0.5 * size_factor, 0.2], 
            [0.2, 0.8 * size_factor]
        ])
    else: # Polygons 또는 Mixed
        points = np.array([
            [0, 0], [0.4, 0.1], [0.5, 0.5], [0.1, 0.4]
        ]) * size_factor

    # 회전 행렬 적용 (미분 계수 방향으로 회전)
    theta = np.radians(angle)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))
    rotated_points = points @ R.T + [x[i], y[i]]
    
    # 다각형 추가
    poly = patches.Polygon(
        rotated_points, 
        closed=True, 
        color=color, 
        alpha=0.7, 
        edgecolor='white', 
        linewidth=0.3
    )
    ax.add_patch(poly)

# 차트 정리
ax.set_xlim(-6, 6)
ax.set_ylim(min(y)-2, max(y)+2)
ax.axis('off')

# 결과 출력
st.pyplot(fig)

# --- 설명 섹션 ---
st.subheader("🧐 수학적 해석")
if "Absolute" in func_option:
    st.warning("주의: $x=0$ 지점에서 함수는 연속이지만 **미분 불가능**합니다. 파편들의 방향이 급격히 변하는 것을 확인하세요!")
elif "Step" in func_option:
    st.error("주의: 이 함수는 0에서 **불연속**입니다. 미분값이 정의되지 않아 파편이 튀는 현상이 발생합니다.")
else:
    st.success("이 함수는 전 구간에서 매끄럽게 미분 가능합니다. 파편들이 흐름(Flow)을 형성합니다.")

st.write(f"현재 총 {num_shapes}개의 수학적 파편이 생성되었습니다.")
