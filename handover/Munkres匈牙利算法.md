# Munkres 匈牙利算法 交接文档

## 1. 概述

**文件路径**: `src/modules/sbstudio/api/munkres.py`

**功能**: 这是 [匈牙利算法](https://en.wikipedia.org/wiki/Hungarian_algorithm)（也称 Kuhn-Munkres 算法或 Munkres 算法）的纯 Python 实现，用于解决**分配问题**（Assignment Problem）。在本项目中，当 `scipy` 不可用时，作为 `linear_sum_assignment` 的降级后备方案。

---

## 2. 算法原理

### 2.1 分配问题

给定一个 N×N 的成本矩阵，找到一种一对一的分配方式（每行匹配一列），使得总成本最小。

**示例**:
```
成本矩阵:           最优分配:
     0   1   2           0   1   2
  0 [400 150 400]   →   0 [ .   ★   . ]   (0,1)=150
  1 [400 450 600]       1 [ .   .   . ]   (2,0)=300
  2 [300 225 300]       2 [ ★   .   . ]   (1,2)=600
                            总成本 = 1050
```

### 2.2 时间复杂度

| 算法 | 时间复杂度 | 空间复杂度 |
|------|-----------|-----------|
| Munkres | O(n³) | O(n²) |

---

## 3. 核心类

### 3.1 `Munkres` 类

```python
class Munkres:
    def compute(self, cost_matrix: Matrix) -> Sequence[Tuple[int, int]]:
        # 返回 [(行索引, 列索引), ...] 的最优配对列表
```

**返回值格式**: `([行索引列表], [列索引列表])`，例如 `([0, 1, 2], [1, 2, 0])` 表示第0行配第1列、第1行配第2列、第2行配第0列。

---

## 4. 算法步骤详解

### 4.1 整体流程

```
compute() 入口
    ↓
步骤1: 行归约 → 每行减去该行最小值
    ↓
步骤2: 星号标记 → 找独立零元素并标记为★
    ↓
步骤3: 检查完成 → 如果★覆盖所有列，算法结束
    ↓
步骤4: 寻找增广路 → 找未覆盖零，标记为'
    ↓
步骤5: 增广路径反转 → 沿路径翻转★和'
    ↓
步骤6: 调整矩阵 → 修改未覆盖元素，返回步骤4
    ↓
完成: 返回★标记的位置
```

### 4.2 步骤1: 行归约 [`__step1`](file:///e:/hhang/studio-blender/src/modules/sbstudio/api/munkres.py#L184-L205)

```python
def __step1(self) -> int:
    for i in range(n):
        minval = min(x for x in self.C[i] if x is not DISALLOWED)
        for j in range(n):
            if self.C[i][j] is not DISALLOWED:
                self.C[i][j] -= minval
    return 2
```

**原理**: 每行减去该行最小值，确保每行至少有一个零元素。这一步不改变最优解，因为所有分配方案的成本都减少了相同的值。

**示例**:
```
原始矩阵:         行归约后:
[400 150 400]     [250   0 250]   ← 减去 150
[400 450 600]  →  [  0  50 200]   ← 减去 400
[300 225 300]     [ 75   0  75]   ← 减去 225
```

### 4.3 步骤2: 星号标记 [`__step2`](file:///e:/hhang/studio-blender/src/modules/sbstudio/api/munkres.py#L207-L225)

```python
def __step2(self) -> int:
    for i in range(n):
        for j in range(n):
            if (self.C[i][j] == 0) and \
                    (not self.col_covered[j]) and \
                    (not self.row_covered[i]):
                self.marked[i][j] = 1    # ★ 标记
                self.col_covered[j] = True
                self.row_covered[i] = True
                break
    self.__clear_covers()
    return 3
```

**原理**: 遍历矩阵，找到零元素，如果其行和列都没有被★覆盖，则标记为★。这保证了每行每列最多只有一个★。

**标记类型**: `marked[i][j]` 的值含义：
- `0`: 未标记
- `1`: ★（Starred）— 表示最优分配
- `2`: '（Primed）— 表示增广路径候选

### 4.4 步骤3: 检查完成 [`__step3`](file:///e:/hhang/studio-blender/src/modules/sbstudio/api/munkres.py#L227-L246)

```python
def __step3(self) -> int:
    count = 0
    for i in range(n):
        for j in range(n):
            if self.marked[i][j] == 1 and not self.col_covered[j]:
                self.col_covered[j] = True
                count += 1
    if count >= n:
        step = 7  # 完成
    else:
        step = 4
    return step
```

**原理**: 覆盖所有包含★的列。如果覆盖的列数等于 n，说明找到了完整的分配方案，算法结束。

### 4.5 步骤4: 寻找增广路 [`__step4`](file:///e:/hhang/studio-blender/src/modules/sbstudio/api/munkres.py#L248-L279)

```python
def __step4(self) -> int:
    while not done:
        (row, col) = self.__find_a_zero(row, col)  # 找未覆盖的零
        if row < 0:
            done = True
            step = 6  # 没有未覆盖零，进入步骤6调整矩阵
        else:
            self.marked[row][col] = 2  # ' 标记
            star_col = self.__find_star_in_row(row)
            if star_col >= 0:
                # 该行有★，覆盖此行，取消该★所在列的覆盖
                col = star_col
                self.row_covered[row] = True
                self.col_covered[col] = False
            else:
                done = True
                self.Z0_r = row
                self.Z0_c = col
                step = 5  # 找到增广路起点
    return step
```

**原理**: 
1. 找一个未被行/列覆盖的零元素
2. 标记为 '（Prime）
3. 如果该行有★，则覆盖该行，取消该★所在列的覆盖，继续寻找
4. 如果该行没有★，找到了一条增广路径，进入步骤5

### 4.6 步骤5: 增广路径反转 [`__step5`](file:///e:/hhang/studio-blender/src/modules/sbstudio/api/munkres.py#L281-L315)

```python
def __step5(self) -> int:
    count = 0
    path[count][0] = self.Z0_r
    path[count][1] = self.Z0_c
    while not done:
        row = self.__find_star_in_col(path[count][1])
        if row >= 0:
            count += 1
            path[count][0] = row
            path[count][1] = path[count-1][1]
        else:
            done = True
        if not done:
            col = self.__find_prime_in_row(path[count][0])
            count += 1
            path[count][0] = path[count-1][0]
            path[count][1] = col
    self.__convert_path(path, count)  # 翻转路径上的★和'
    self.__clear_covers()
    self.__erase_primes()
    return 3
```

**原理**: 构造一条交替的★-'路径，然后将路径上的★变为未标记，将'变为★。这增加了★的数量。

**示例**:
```
增广路径:  (2,0)' → (0,0)★ → (0,1)' → (1,1)★ → (1,2)'
翻转后:    (2,0)★ → (0,0)  → (0,1)★ → (1,1)  → (1,2)★
```

### 4.7 步骤6: 调整矩阵 [`__step6`](file:///e:/hhang/studio-blender/src/modules/sbstudio/api/munkres.py#L317-L340)

```python
def __step6(self) -> int:
    minval = self.__find_smallest()  # 找未覆盖的最小值
    for i in range(n):
        for j in range(n):
            if self.row_covered[i]:
                self.C[i][j] += minval  # 覆盖行加 minval
            if not self.col_covered[j]:
                self.C[i][j] -= minval  # 未覆盖列减 minval
    return 4
```

**原理**: 
- 覆盖行中的元素加上最小值
- 未覆盖列中的元素减去最小值
- 被双重覆盖的元素（覆盖行 + 未覆盖列）的值不变

这样操作后，会产生新的零元素，同时保持已有★的有效性。

---

## 5. 辅助方法

### 5.1 `pad_matrix` — 矩阵填充

```python
def pad_matrix(self, matrix, pad_value=0):
    # 将非方阵填充为方阵
```

**用途**: 匈牙利算法要求输入为方阵。当行数≠列数时，用 `pad_value`（默认0）填充成方阵。

### 5.2 `__find_a_zero` — 查找零元素

```python
def __find_a_zero(self, i0=0, j0=0):
    # 使用环形遍历查找未覆盖的零元素
    # 从上次位置继续搜索，避免重复扫描
```

**优化**: 从上一次搜索的下一个位置开始，而不是每次都从头开始。使用环形索引 `(i+1) % n` 实现循环遍历。

### 5.3 `__convert_path` — 路径转换

```python
def __convert_path(self, path, count):
    for i in range(count+1):
        if self.marked[path[i][0]][path[i][1]] == 1:
            self.marked[path[i][0]][path[i][1]] = 0  # ★ → 未标记
        else:
            self.marked[path[i][0]][path[i][1]] = 1  # ' → ★
```

### 5.4 `DISALLOWED` 常量

```python
DISALLOWED = DISALLOWED_OBJ()
```

**用途**: 标记不允许的分配。当矩阵中某个位置为 `DISALLOWED` 时，算法会跳过该位置，不将其作为零元素处理。

---

## 6. 导出接口

### 6.1 `make_cost_matrix`

```python
def make_cost_matrix(profit_matrix, inversion_function=None):
    # 将利润矩阵转换为成本矩阵
```

**用途**: 匈牙利算法求解最小成本问题。如果原始问题是最大化利润，需要先将利润转换为成本。

**默认转换**: `cost = max(profit_matrix) - profit`

### 6.2 `print_matrix`

```python
def print_matrix(matrix, msg=None):
    # 格式化打印矩阵内容，用于调试
```

---

## 7. 在项目中的使用

### 7.1 降级方案 [`algorithm.py`](file:///e:/hhang/studio-blender/src/modules/sbstudio/api/algorithm.py#L9-L12)

```python
try:
    from scipy.optimize import linear_sum_assignment
except:
    from sbstudio.api.munkres import Munkres
    linear_sum_assignment = lambda M: np.asarray(Munkres().compute(M))
```

当 `scipy` 不可用时，使用 `Munkres` 类作为后备方案。接口保持一致：输入成本矩阵，返回 `(行索引数组, 列索引数组)`。

### 7.2 调用位置

| 位置 | 文件 | 行号 | 功能 |
|------|------|------|------|
| 匈牙利算法初始化 | `sbstudio/api/algorithm.py` | 45 | 计算初始匹配方案 |
| 数量不等处理 | `sbstudio/api/algorithm.py` | 82 | 为较少点集选择最优子集 |

---

## 8. 数据结构

### 8.1 核心状态

| 属性 | 类型 | 说明 |
|------|------|------|
| `C` | Matrix | 成本矩阵的副本（归约后的） |
| `marked` | Matrix | 标记矩阵：0=无，1=★，2=' |
| `row_covered` | list[bool] | 行覆盖状态 |
| `col_covered` | list[bool] | 列覆盖状态 |
| `path` | Matrix | 增广路径存储 |
| `Z0_r`, `Z0_c` | int | 增广路径起点的行列索引 |

### 8.2 输入输出

**输入**:
```python
cost_matrix = [
    [400, 150, 400],
    [400, 450, 600],
    [300, 225, 300]
]
```

**输出**:
```python
([0, 1, 2], [1, 2, 0])  # 行索引列表, 列索引列表
# 等价于: [(0,1), (1,2), (2,0)]
# 总成本: 150 + 600 + 300 = 1050
```

---

## 9. 依赖关系

| 模块 | 用途 |
|------|------|
| `copy` | 深拷贝矩阵 |
| `sys` | `sys.maxsize` 作为无穷大值 |
| `typing` | 类型注解 |

---

## 10. 调试与日志

### 10.1 测试用例

文件末尾包含 10 个测试用例，覆盖：

| 用例类型 | 数量 | 说明 |
|----------|------|------|
| 方阵（整数） | 2 | 3×3 矩阵 |
| 矩形矩阵 | 2 | 3×4 矩阵 |
| 浮点数值 | 3 | 带小数的矩阵 |
| DISALLOWED 标记 | 3 | 包含不允许分配的矩阵 |

运行测试:
```bash
python src/modules/sbstudio/api/munkres.py
```

### 10.2 调试方法

1. 使用 `print_matrix()` 打印中间状态矩阵
2. 检查 `marked` 矩阵的★分布
3. 验证总成本是否符合预期

### 10.3 常见问题排查

| 问题 | 可能原因 |
|------|----------|
| `UnsolvableMatrix` | 某行全部为 `DISALLOWED`，无法分配 |
| 结果不正确 | 成本矩阵包含负数（算法要求非负） |
| 性能差 | 矩阵过大（>500×500），建议使用 scipy |

---

## 11. 算法特点

### 11.1 优势

| 特点 | 说明 |
|------|------|
| **纯 Python 实现** | 无外部依赖，可在受限环境中使用 |
| **支持非方阵** | 自动填充为方阵 |
| **支持 DISALLOWED** | 可标记不允许的分配 |
| **精确最优解** | 保证找到全局最优解，非近似 |

### 11.2 局限性

| 局限 | 说明 |
|------|------|
| **O(n³) 时间复杂度** | 大规模矩阵（>1000）时较慢 |
| **纯 Python 性能** | 比 scipy 的 C 实现慢 10-100 倍 |
| **不支持稀疏矩阵** | 所有元素都需要存储和遍历 |
| **要求非负成本** | 负数可能导致算法行为异常 |

---

## 12. 常见问题 FAQ

### Q1: 匈牙利算法为什么叫 Munkres？

Munkres 算法由 James Munkres 在 1957 年提出，是对 Hungarian method 的改进版本。它的时间复杂度为 O(n³)，比原始算法更高效。

### Q2: `DISALLOWED` 的使用场景是什么？

当某些分配在物理上不可行时使用。例如：某架无人机不能飞到某个位置，可以将该位置标记为 `DISALLOWED`，算法会自动选择其他可行分配。

### Q3: 矩形矩阵如何处理？

`pad_matrix()` 方法用 0 填充成方阵。多余的行或列会被分配到填充位置（成本为0），实际结果中会被忽略。

### Q4: 与 scipy 的性能差距有多大？

| 矩阵大小 | Munkres (Python) | scipy (C) | 差距 |
|----------|-----------------|-----------|------|
| 50×50 | ~0.1s | ~0.001s | 100x |
| 200×200 | ~2s | ~0.01s | 200x |
| 1000×1000 | ~200s | ~0.5s | 400x |

因此项目中优先使用 scipy，仅在 scipy 不可用时降级到 Munkres。

### Q5: 步骤6中为什么要"覆盖行加，未覆盖列减"？

这保证了：
1. 已有★所在行/列的值不变（被双重覆盖）
2. 未覆盖区域产生新的零元素
3. 已覆盖列中的零元素不被破坏

### Q6: 为什么固定随机种子 `20181213` 不在这里？

Munkres 是**确定性算法**，不涉及随机性。每次运行相同输入都会得到相同结果（如果有多个最优解，返回第一个找到的）。
