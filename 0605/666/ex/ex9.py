import numpy as np

# 3次元配列の定義 (形状は 3 x 2 x 5)
arr = np.array([
    [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]],
    [[11, 12, 13, 14, 15], [16, 17, 18, 19, 20]],
    [[21, 22, 23, 24, 25], [26, 27, 28, 29, 30]]
])

print("--- 全要素の統計値 ---")
print(f"全要素の平均値: {np.mean(arr)}")
print(f"全要素の合計値: {np.sum(arr)}")
print(f"全要素の最大値: {np.max(arr)}")
print(f"全要素の最小値: {np.min(arr)}")
print()

print("--- 次元ごとの統計値 (axis別) ---")
# axis=0: 最も外側の次元（3つのブロック間での集計）
# axis=1: 2番目の次元（各ブロック内の2つの行間での集計）
# axis=2: 最も内側の次元（各行内の5つの要素間での集計）

for axis in range(arr.ndim):
    print(f"[軸 axis={axis} での集計]")
    print(f"  平均値:\n{np.mean(arr, axis=axis)}")
    print(f"  合計値:\n{np.sum(arr, axis=axis)}")
    print(f"  最大値:\n{np.max(arr, axis=axis)}")
    print(f"  最小値:\n{np.min(arr, axis=axis)}")
    print("-" * 30)