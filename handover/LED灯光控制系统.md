# HanHang LED 灯光控制 交接文档

## 1. 概述

HanHang LED 灯光控制系统用于在 Blender 中通过 Color Ramp 渐变方式为无人机编队设置 LED 灯光颜色。支持多种空间排序模式，实现复杂的渐变色灯光效果。

**相关文件**:

| 文件   | 类型                               | 路径                                                           |
| ---- | -------------------------------- | ------------------------------------------------------------ |
| 模型   | `model/hhang_led_control.py`     | `src/modules/sbstudio/plugin/model/hhang_led_control.py`     |
| 面板   | `panels/hhang_led_control.py`    | `src/modules/sbstudio/plugin/panels/hhang_led_control.py`    |
| 操作符  | `operators/hhang_led_control.py` | `src/modules/sbstudio/plugin/operators/hhang_led_control.py` |
| 颜色工具 | `colors.py`                      | `src/modules/sbstudio/plugin/colors.py`                      |

***

## 2. 数据模型

### 2.1 [`HHangLEDControlPanelProperties`](file:///e:/hhang/studio-blender/src/modules/sbstudio/plugin/model/hhang_led_control.py)

```python
class HHangLEDControlPanelProperties(PropertyGroup):
    def update(self, context):
        self.color = self.texture.color_ramp.evaluate(self.position)[:3]

    texture = PointerProperty(type=Texture, name="HHangLEDControlTexture")
    position = FloatProperty(name="Color ramp position", default=0, min=0, max=1, update=update)
    color = ColorProperty(name="Selected color")
```

**属性说明**:

| 属性         | 类型                       | 默认值 | 范围   | 说明                             |
| ---------- | ------------------------ | --- | ---- | ------------------------------ |
| `texture`  | PointerProperty(Texture) | -   | -    | 存储 Color Ramp 的纹理对象            |
| `position` | FloatProperty            | 0   | 0\~1 | 当前采样位置，改变时自动更新 `color`         |
| `color`    | ColorProperty            | -   | -    | 根据 position 从 Color Ramp 采样的颜色 |

**联动机制**: 当用户拖动 `position` 滑块时，`update` 回调从 `texture.color_ramp` 采样，自动更新 `color` 显示。

***

## 3. UI 面板

### 3.1 [`HHangLEDControlPanel`](file:///e:/hhang/studio-blender/src/modules/sbstudio/plugin/panels/hhang_led_control.py)

| 属性               | 值                                            |
| ---------------- | -------------------------------------------- |
| `bl_idname`      | `OBJECT_PT_skybrush_hhang_led_control_panel` |
| `bl_label`       | HanHang LED Control                          |
| `bl_space_type`  | VIEW\_3D                                     |
| `bl_region_type` | UI                                           |
| `bl_category`    | LEDs                                         |

### 3.2 界面布局

```
┌─ HanHang LED Control ───────────────┐
│                                     │
│  ┌─ Color Ramp ─────────────────┐   │
│  │  ████░░░░░░░░░░░░░░░░░░░░    │   │
│  └──────────────────────────────┘   │
│                                     │
│  [位置滑块] [当前颜色预览] [应用] [渐变] │
└─────────────────────────────────────┘
```

| 控件         | 功能                  |
| ---------- | ------------------- |
| Color Ramp | 自定义渐变颜色条，可添加/删除颜色节点 |
| 位置滑块       | 0\~1 范围采样，实时预览颜色    |
| 颜色预览       | 显示当前采样颜色            |
| 应用按钮       | 将当前颜色应用到选中无人机       |
| 渐变按钮       | 对选中无人机应用颜色渐变模式      |

***

## 4. 操作符详解

### 4.1 `UseHHangLEDControlOperator` — 启用 HanHang 控制

**文件**: [hhang\_led\_control.py:17-28](file:///e:/hhang/studio-blender/src/modules/sbstudio/plugin/operators/hhang_led_control.py#L17-L28)

| 属性          | 值                                |
| ----------- | -------------------------------- |
| `bl_idname` | `skybrush.use_hhang_led_control` |
| `bl_label`  | Generate                         |

**执行流程**:

```python
def execute(self, context):
    bpy.ops.skybrush.hhang_led_control_generate()     # 1. 初始化 Color Ramp
    unregister_panel(LightEffectsPanel)               # 2. 注销灯光效果面板
    register_panel(HHangLEDControlPanel)              # 3. 注册 HHang 面板
    register_panel(LightEffectsPanel)                 # 4. 重新注册灯光效果面板
    bpy.types.Scene.used_hhang_led_control = True     # 5. 标记已切换
    return {"FINISHED"}
```

**面板重注册原理**: `LightEffectsPanel` 的显示内容依赖于 `used_hhang_led_control` 标志。先注销再注册，使其 UI 更新。

### 4.2 `HHangLEDControlGenerateOperator` — 初始化 Color Ramp

**文件**: [hhang\_led\_control.py:30-41](file:///e:/hhang/studio-blender/src/modules/sbstudio/plugin/operators/hhang_led_control.py#L30-L41)

| 属性          | 值                                     |
| ----------- | ------------------------------------- |
| `bl_idname` | `skybrush.hhang_led_control_generate` |
| `bl_label`  | Generate                              |

**执行逻辑**:

```python
def execute(self, context):
    hhang_led_control = context.scene.skybrush.hhang_led_control
    if not hhang_led_control.texture:
        hhang_led_control.texture = bpy.data.textures.new(name="HHangLedControl", type="IMAGE")
        hhang_led_control.texture.use_color_ramp = True
        hhang_led_control.texture.image = None
    return {'FINISHED'}
```

创建新的 Image 类型 Texture 并启用 Color Ramp，如果已存在则不重复创建。

### 4.3 `HHangLEDControlApplyOperator` — 应用单色

**文件**: [hhang\_led\_control.py:43-52](file:///e:/hhang/studio-blender/src/modules/sbstudio/plugin/operators/hhang_led_control.py#L43-L52)

| 属性          | 值                                  |
| ----------- | ---------------------------------- |
| `bl_idname` | `skybrush.hhang_led_control_apply` |
| `bl_label`  | Apply                              |

**执行逻辑**:

```python
def execute(self, context):
    color = context.scene.skybrush.hhang_led_control.color
    for drone in get_selected_drones():
        create_keyframe_for_color_of_drone(drone, color)
    return {'FINISHED'}
```

将当前 `color`（从 Color Ramp 采样得到）应用到所有选中的无人机。

### 4.4 `HHangLEDControlGradientOperator` — 渐变颜色

**文件**: [hhang\_led\_control.py:54-117](file:///e:/hhang/studio-blender/src/modules/sbstudio/plugin/operators/hhang_led_control.py#L54-L117)

| 属性          | 值                                     |
| ----------- | ------------------------------------- |
| `bl_idname` | `skybrush.hhang_led_control_gradient` |
| `bl_label`  | Gradient                              |

#### 渐变模式

| 模式        | 枚举值        | 排序方式            |
| --------- | ---------- | --------------- |
| 默认        | `DEFAULT`  | 保持选择顺序          |
| 随机        | `RANDOM`   | 随机打乱            |
| X 坐标      | `X`        | 按 X 坐标升序        |
| Y 坐标      | `Y`        | 按 Y 坐标升序        |
| Z 坐标      | `Z`        | 按 Z 坐标升序        |
| 距 3D 光标距离 | `DISTANCE` | 按距离 3D 光标升序（默认） |

#### 执行流程

```python
def execute(self, context):
    color_ramp = context.scene.skybrush.hhang_led_control.texture.color_ramp
    selection = get_selected_drones()
    num_selected = len(selection)
    if not num_selected:
        self.report({"INFO"}, "Select some drones first to apply colors")
        return {"CANCELLED"}

    for index, drone in enumerate(self._sort_selection(selection, context)):
        ratio = index / (num_selected - 1) if num_selected > 1 else 0.5
        color = color_ramp.evaluate(ratio)[:3]
        create_keyframe_for_color_of_drone(drone, color)
    return {"FINISHED"}
```

**颜色分配公式**:

- 单个无人机: `ratio = 0.5`（中间值）
- 多个无人机: `ratio = index / (n - 1)`，从 0.0 到 1.0 均匀分布

#### 排序算法 [`_sort_selection`](file:///e:/hhang/studio-blender/src/modules/sbstudio/plugin/operators/hhang_led_control.py#L87-L117)

```python
def _sort_selection(self, selection, context):
    if self.gradient_mode == "DEFAULT":
        return selection
    if self.gradient_mode == "RANDOM":
        shuffle(selection)
        return selection

    # 需要位置信息时
    for obj in selection:
        obj.update_tag(refresh={'OBJECT', 'DATA'})
    bpy.context.view_layer.update()

    with create_position_evaluator() as get_positions_of:
        positions = get_positions_of(selection)

    # 根据模式提取优先级值
    if self.gradient_mode == "X":
        priorities = [point[0] for point in positions]
    elif self.gradient_mode == "Y":
        priorities = [point[1] for point in positions]
    elif self.gradient_mode == "Z":
        priorities = [point[2] for point in positions]
    elif self.gradient_mode == "DISTANCE":
        cl = tuple(context.scene.cursor.location)
        priorities = [(cl[0]-p[0])**2 + (cl[1]-p[1])**2 + (cl[2]-p[2])**2 for p in positions]

    order = list(range(len(selection)))
    order.sort(key=priorities.__getitem__)
    return [selection[i] for i in order]
```

**位置缓存机制**: 使用 `create_position_evaluator()` 上下文管理器批量获取位置，避免逐帧跳转。

***

## 5. 颜色应用核心

### 5.1 `create_keyframe_for_color_of_drone` [`colors.py`](file:///e:/hhang/studio-blender/src/modules/sbstudio/plugin/colors.py)

```python
def create_keyframe_for_color_of_drone(drone, color, *, frame=None):
    # 为无人机在当前帧（或指定帧）插入颜色关键帧
```

**功能**:

1. 获取无人机的灯光对象
2. 设置灯光颜色
3. 在当前帧插入颜色关键帧

***

## 6. 数据结构

### 6.1 场景属性

| 属性                                 | 类型            | 位置                           | 说明               |
| ---------------------------------- | ------------- | ---------------------------- | ---------------- |
| `scene.skybrush.hhang_led_control` | PropertyGroup | `model/hhang_led_control.py` | HHang LED 控制属性   |
| `scene.used_hhang_led_control`     | bool (动态)     | -                            | 标记是否已启用 HHang 控制 |

### 6.2 Color Ramp 结构

```
Texture (IMAGE 类型)
└── color_ramp
    ├── elements[0] = (位置: 0.0, 颜色: RGBA)
    ├── elements[1] = (位置: 1.0, 颜色: RGBA)
    └── ...
```

默认创建后包含两个元素（起点和终点），用户可添加更多颜色节点。

***

## 7. 依赖关系

### 7.1 外部依赖

| 模块               | 用途                 |
| ---------------- | ------------------ |
| `bpy`            | Blender Python API |
| `random.shuffle` | 随机排序               |

### 7.2 内部依赖

| 模块                                | 用途               |
| --------------------------------- | ---------------- |
| `sbstudio.plugin.selection`       | 获取选中的无人机         |
| `sbstudio.plugin.colors`          | 创建颜色关键帧          |
| `sbstudio.plugin.utils.evaluator` | 批量获取无人机位置        |
| `sbstudio.plugin.props`           | ColorProperty 定义 |
| `sbstudio.plugin.plugin_helpers`  | 面板注册/注销          |

***

## 8. 调试与日志

### 8.1 信息提示

```python
self.report({"INFO"}, "Select some drones first to apply colors")
```

当没有选中无人机时执行渐变操作会提示。

### 8.2 调试验证方法

1. 在 3D 视图中选中若干无人机
2. 打开侧边栏（N 键）→ "LEDs" 标签 → "HanHang LED Control" 面板
3. 在 Color Ramp 中设置渐变颜色
4. 拖动位置滑块预览颜色
5. 点击 "应用" 将当前颜色应用到选中无人机，或点击 "渐变" 生成分布渐变
6. 在时间线中查看颜色关键帧
7. 播放动画观察颜色变化

### 8.3 常见问题排查

| 问题             | 可能原因                                           |
| -------------- | ---------------------------------------------- |
| 颜色不显示          | 未插入关键帧，检查 `create_keyframe_for_color_of_drone` |
| Color Ramp 不出现 | 未调用 `hhang_led_control_generate` 初始化           |
| 面板不显示          | 检查 `used_hhang_led_control` 标志是否已设置            |

***

## 9. 常见问题 FAQ

### Q1: Color Ramp 采样原理是什么？

`color_ramp.evaluate(ratio)` 在 0\~1 范围内采样：

- `ratio = 0` → 返回第一个颜色节点的颜色
- `ratio = 1` → 返回最后一个颜色节点的颜色
- `0 < ratio < 1` → 在相邻节点间插值

### Q2: 渐变模式如何选择？

| 场景       | 推荐模式     |
| -------- | -------- |
| 保持原有编队顺序 | DEFAULT  |
| 创意效果     | RANDOM   |
| 从左到右渐变   | X        |
| 从近到远渐变   | Y        |
| 从低到高渐变   | Z        |
| 从中心向外扩散  | DISTANCE |

### Q3: 如何自定义颜色节点？

在 HanHang LED 控制面板的 Color Ramp 中：

1. 点击渐变条下方的 "+" 按钮添加节点
2. 点击节点选择颜色
3. 拖动节点调整位置

### Q4: 切换到 HHang 后能切回基础控制吗？

不能直接切换。一旦设置 `scene.used_hhang_led_control = True`，基础面板中的切换按钮会隐藏。需要手动重置该属性。

### Q5: 如何为整个编队设置统一颜色？

选中所有无人机，在 Color Ramp 中选择一个颜色，点击 "应用" 按钮即可。

### Q6: 位置滑块的作用是什么？

位置滑块用于预览 Color Ramp 中特定位置的颜色。拖动滑块时，`color` 属性自动更新，方便用户在选择颜色前预览效果。
