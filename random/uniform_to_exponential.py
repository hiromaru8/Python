import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# 一様乱数を生成し、指数分布に変換して可視化する
# ------------------------------

# サンプル数（乱数の個数）
n = 100

# [0, 100) の一様乱数を生成（均等なランダム）
uniform_rands = np.random.uniform(0, 100, n)

# 指数分布のレートパラメータ λ（平均は 1/λ）
lambda_val = 1.0

# 一様乱数を指数分布に変換（逆関数法を使用）
exponential_rands = -np.log(uniform_rands) / lambda_val
print("Generated Uniform Random Numbers:", uniform_rands)  # 一様乱数の表示
print("Converted Exponential Random Numbers:", exponential_rands)  # 指数分布の

print(np.log(1.8524691) )
# ------------------------------
# ヒストグラムによる視覚化
# ------------------------------

# 図のサイズを設定（横長で2つ並べる）
plt.figure(figsize=(12, 5))

# --- 左：一様分布のヒストグラム ---
plt.subplot(1, 2, 1)  # 1行2列の1つ目
plt.hist(uniform_rands, bins=50, color='skyblue', edgecolor='black', density=True)
plt.title("Uniform Distribution [0,1]")  # グラフタイトル
plt.xlabel("Value")  # x軸ラベル
plt.ylabel("Frequency")  # y軸ラベル

# --- 右：指数分布のヒストグラム ---
plt.subplot(1, 2, 2)  # 1行2列の2つ目
plt.hist(exponential_rands, bins=50, color='salmon', edgecolor='black', density=True)

# 理論的な指数分布のPDF（確率密度関数）を重ねて描画
x = np.linspace(0, 8, 200)  # x軸の値（0〜8）
plt.plot(x, lambda_val * np.exp(-lambda_val * x), 'k--', label='Theoretical PDF')  # 点線で理論曲線

plt.title(f"Exponential Distribution (λ = {lambda_val})")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.legend()  # 凡例を表示

# 図全体のレイアウト調整（重なり防止）
plt.tight_layout()

# グラフを表示
plt.show()
