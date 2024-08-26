import bpy
# {
#     'fr_FR': {
#         ('*', ''): 'Project-Id-Version: Copy Settings 0.1.5 (r0)\nReport-Msgid-Bugs-To: \nPOT-Creation-Date: 2013-04-18 15:27:45.563524\nPO-Revision-Date: 2013-04-18 15:38+0100\nLast-Translator: Bastien Montagne <montagne29@wanadoo.fr>\nLanguage-Team: LANGUAGE <LL@li.org>\nLanguage: __POT__\nMIME-Version: 1.0\nContent-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n',
#         ('Operator', 'Render: Copy Settings'): 'Rendu : copier réglages',
#         ('*', 'Copy render settings from current scene to others'): 'Copier les réglages de rendu depuis la scène courante vers d’autres'
#     }
# }

# "Operator"
# "Armature"
# "Brush"
# "Camera"
# "Text"
# "Mesh"
# "ID"
# "Sound"
# "Action"
# "Curve"
# "Light"
# "ParticleSettings"
# "World"
# "Image"
# "UI_Events_KeyMaps"
# "WindowManager"
# "MovieClip"
# "NodeTree"
# "GPencil"
# "Object"
# "Scene"
# "View3D"
# "Sequence"
# "Screen"
# "Collection"
# "Volume"
# "Plural"
# "Metaball"
# "Material"
# "Texture"
# "Lattice"
# "Speaker"
# "FreestyleLineStyle"
# "WorkSpace"
# "LightProbe"
# "Curves"
# "PointCloud"
# "Simulation"
# "Key"
translation_zh_CN = {
    ("*", "Swarm") : "集群",
    ("*", "Formations") : "编队",
    ("*", "Drones") : "无人机",
    ("*", "Drone") : "模板",
    ("*", "Drone template object to use for all drones. The SPHERE is the default simplest isotropic drone object, the CONE is anisotropic for visualizing yaw control, or use SELECTED for any custom object that is selected right now.") :
        "用于所有无人机的无人机模板对象。球体是默认的最简单的各向同性无人机对象，锥体是各向异性的，用于可视化偏航控制，或者使用当前选择的任何自定义对象。",
    ("Operator", "Takeoff") : "起飞",
    ("Operator", "RTH") : "返航",
    ("Operator", "Land") : "降落",
    ("*", "Drone collection") : "无人机收集",
    ("*", "The collection that contains all the objects that are to be treated as drones") : "包含将被视为无人机的所有对象的集合",
    ("*", "Max acceleration") : "最大加速度",
    ("*", "Maximum acceleration allowed when planning the duration of transitions between fixed points") : "规划固定点之间过渡的持续时间时允许的最大加速度",
    ("*", "Random seed") : "随机种子",
    ("*", "Root random seed value used to generate randomized stuff in this show file") : "根随机种子值，用于在此显示文件中生成随机内容",
    ("*", "Show type") : "显示类型",
    ("*", "Specifies whether the drone show is an outdoor or an indoor show") : "指定无人机表演是室外表演还是室内表演",
    ("*", "Outdoor show, for drones that navigate using a geodetic (GPS) coordinate system") : "户外表演，针对使用大地测量（GPS）坐标系导航的无人机",
    ("*", "Indoor show, for drones that navigate using a local (XYZ) coordinate system") : "室内表演，适用于使用本地（XYZ）坐标系导航的无人机",
    ("*", "Use bloom effect") : "使用绽放效果",
    ("*", "Specifies whether the bloom effect should automatically be enabled on the 3D View when the show is loaded") : "指定加载演出时是否应在三维视图上自动启用绽放效果",
    ("*", "Time markers") : "时间标记",
    ("*", "Outdoor") : "户外",
    ("*", "Indoor") : "室内",
    ("Operator", "Create Takeoff Grid") : "创建起飞网格",
    ("*", "Creates the takeoff grid and the corresponding set of drones") : "创建起飞网格和相应的无人机集",
    ("*", "Rows") : "行",
    ("*", "Number of rows in the takeoff grid") : "起飞网格中的行数",
    ("*", "Columns") : "列",
    ("*", "Number of columns in the takeoff grid") : "起飞网格中的列数",
    ("*", "Drone count") : "无人机数量",
    ("*", "Number of drones in the grid") : "网格中的无人机数量",
    ("*", "Number of slots to leave empty") : "要保留为空的插槽数",
    ("*", "Spacing") : "间距",
    ("*", "Spacing between the drones in the grid") : "网格中无人机之间的间距",
    # ("*", "Takeoff grid") : "起飞网格",
    ("*", "Add a takeoff maneuver to all the drones") : "为所有无人机添加起飞动作",
    ("*", "at frame") : "在帧处",
    ("*", "Start frame of the takeoff maneuver") : "起飞机动的起始帧",
    ("*", "with velocity") : "带速度",
    ("*", "Average vertical velocity during the takeoff maneuver") : "起飞机动过程中的平均垂直速度",
    ("*", "to altitude") : "到海拔高度",
    ("*", "Altitude to take off to") : "起飞高度",
    ("*", "Relative Altitude") : "相对海拔高度",
    ("*", "Specifies whether the takeoff altitude is relative to the current altitude of the drone") : "指定起飞高度是否相对于无人机的当前高度",
    ("*", "Delay") : "延迟",
    ("*", "Delay between takeoffs of consecutive drones in the takeoff sequence") : "起飞序列中连续无人机起飞之间的延迟",
    ("*", "Order") : "顺序",
    ("*", "Order of drones in the takeoff sequence") : "无人机起飞顺序",
    ("*", "Default") : "违约",
    ("*", "Use the order in which the drones appear in the drone collection") : "使用无人机出现在无人机集合中的顺序",
    ("*", "Name") : "名称",
    ("*", "Sort the drones alphabetically") : "按字母顺序对无人机进行排序",
    ("*", "X axis first") : "X轴优先",
    ("*", "Sort the drones by X axis first, then by Y axis") : "先按X轴，然后按Y轴对无人机进行排序",
    ("*", "Y axis first") : "Y轴优先",
    ("*", "Sort the drones by Y axis first, then by X axis") : "先按Y轴，然后按X轴对无人机进行排序",
    ("*", "Reverse ordering") : "反向排序",
    ("*", "Whether to reverse the ordering of the takeoff sequence") : "是否颠倒起飞顺序",
    ("*", "Return Drones to Home Positions") : "将无人机返回原位",
    ("*", "Add a return-to-home maneuver to all the drones") : "为所有无人机添加返航机动",
    ("*", "at frame") : "在帧处",
    ("*", "Start frame of the return-to-home maneuver") : "返航机动的起始帧",
    ("*", "with velocity") : "带速度",
    ("*", "Average velocity during the return-to-home maneuver") : "返航机动过程中的平均速度",
    ("*", "to altitude") : "到海拔高度",
    ("*", "Altitude to return-to-home to") : "返回原点的高度",
    ("*", "Land Drones") : "陆地无人机",
    ("*", "Add a landing maneuver to all the drones") : "为所有无人机添加着陆动作",
    ("*", "at frame") : "在帧处",
    ("*", "Start frame of the landing maneuver") : "着陆机动的起始帧",
    ("*", "with velocity") : "带速度",
    ("*", "Average vertical velocity during the landing maneuver") : "着陆机动过程中的平均垂直速度",
    ("*", "to altitude") : "到海拔高度",
    ("*", "Altitude to land to") : "着陆高度",
    ("Operator", "Stats") : "状态",
    ("Operator", "Append to Storyboard") : "附加到故事板",
    ("Operator", "Update") : "更新",
    ("*", "Reorder") : "重新排序",
    ("*", "Sort by name") : "名称排序",
    ("*", "Shuffle") : "乱序",
    ("*", "Reverse") : "反序",
    ("*", "Sort by X coordinate") : "按X坐标排序",
    ("*", "Sort by Y coordinate") : "按Y坐标排序",
    ("*", "Sort by Z coordinate") : "按Z坐标排序",
    ("*", "Every 2nd") : "每两个",
    ("*", "Every 3rd") : "每三个",
    ("*", "Every 4th") : "每四个",
    ("*", "Ensure safety distance") : "确保安全距离",
    ("*", "Type") : "类型",
    ("*", "Reordering to perform on the formation") : "重新排序以对编队执行",
    ("*", "Reorder Formation Markers") : "重新排列编队标记",
    ("*", "Re-orders individual markers within a formation") : "重新排序编队中的单个标记",
    ("*", "Formation must not contain sub-collections") : "编队不得包含子集合",
    ("*", "Formation markers reordered") : "编队标记重新排序",
    ("*", "Selected formation that the operators in this panel will operate on") : "此面板中的操作员将操作的选定编队",
    ("*", "Show order of markers") : "显示标记的顺序",
    ("*", "Shows the order of the markers of the current formation in the 3D view") : "显示当前编队的标记在三维视图中的顺序",
    ("*", "Select Formation") : "选择编队",
    ("*", "Adds the selected formation to the selection") : "将选定的编组添加到选定编组",
    ("*", "This formation consists of multiple objects; cannot select one for Edit mode") : "这种构造由多个物体组成；无法为编辑模式选择一个",
    ("*", "Deselect Formation") : "取消选择编队",
    ("*", "Removes the selected formation from the selection") : "从选择中删除选定的格式",
    ("*", "Append Selected Formation to Storyboard") : "将选定的队形附加到故事板",
    ("*", "Appends the selected formation to the end of the show, planning the transition between the last formation and the new one") : "将选定的队形附加到表演的结尾，计划上一个队形和新队形之间的转换",
    ("*", "Error while invoking transition planner on the Skybrush Studio online service") : "在Skybrush Studio在线服务上调用转换计划器时出错",
    ("*", "Apply Colors to Selected Drones") : "将颜色应用于选定的无人机",
    ("*", "Applies the current primary or secondary color from the LED control panel to the selected drones, optionally creating a gradient.") : "将LED控制面板中的当前主色或次色应用于选定的无人机，可选择创建渐变。",
    ("*", "Primary color") : "原色",
    ("*", "Primary color to apply on the selected drones") : "应用于选定无人机的原色",
    ("*", "Primary color to set on the selected drones") : "要在所选无人机上设置的原色",
    ("*", "Secondary color") : "次要颜色",
    ("*", "Secondary color to apply on the selected drones; used for gradients only") : "应用于选定无人机的次要颜色；仅用于渐变",
    ("*", "Secondary color to set on the selected drones; used for gradients only") : "在所选无人机上设置的次要颜色；仅用于渐变",
    ("*", "Color to apply") : "要应用的颜色",
    ("*", "Primary (1)") : "初级（1）",
    ("*", "Secondary (2)") : "次要（2）",
    ("*", "Gradient (1 -> 2)") : "渐变（1->2）",
    ("*", "Fade to color") : "渐变为彩色",
    ("*", "Add a keyframe to fade to this color from the previous keyframe instead of stepping to this color abruptly") : "添加一个关键帧，使其从上一关键帧渐变到此颜色，而不是突然渐变到此颜色",
    ("*", "Order in gradient") : "梯度中的顺序",
    ("*", "Default") : "违约",
    ("*", "Random") : "随机的",
    ("*", "X coordinate") : "X坐标",
    ("*", "Y coordinate") : "Y坐标",
    ("*", "Z coordinate") : "Z坐标",
    ("*", "Distance from 3D cursor") : "与三维光标的距离",
    ("*", "Select some drones first to apply colors") : "首先选择一些无人机来应用颜色",
    ("*", "Create Formation") : "创建编队",
    ("*", "Creates a new formation in the Formations collection.") : "在“格式”集合中创建新的格式。",
    ("*", "Name") : "名称",
    ("*", "Name of the new formation") : "新编队名称",
    ("Operator", "Create Light Effect") : "创建灯光效果",
    ("*", "Creates a new light effect at the end of the effect list.") : "在效果列表的末尾创建新的灯光效果。",
    ("Operator", "Create New Storyboard Entry") : "创建新故事板条目",
    ("*", "Creates a new storyboard entry at the end of the storyboard.") : "在故事板的末尾创建一个新的故事板条目。",
    ("*", "LED color of {drone.name}") : "{drone.name}的LED颜色",
    ("*", "Detach Materials from Drone Template") : "从无人机模板中分离材料",
    ("Operator", "Duplicate Light Effect") : "复制灯光效果",
    ("*", "Duplicates the selected light effect in the effect list") : "复制效果列表中的选定灯光效果",
    ("*", "Export Skybrush CSV") : "导出Skybrush CSV",
    ("*", "Export selected drones only") : "仅导出选定的无人机",
    ("*", "Export only the selected drones. Uncheck to export all drones, irrespectively of the selection.") : "仅导出选定的无人机。取消确认导出所有无人机，无论选择如何。",
    ("*", "Frame rate") : "帧速率",
    ("*", "Number of samples to take from trajectories and lights per second") : "每秒从轨迹和灯光中获取的采样数",
    ("*", "Filename must not be empty") : "文件名不能为空",
    ("*", "CSV exporter") : "CSV导出器",
    ("*", "Export successful") : "导出成功",
    ("*", "Export Skybrush PDF") : "导出 Skybrush PDF",
    ("*", "Trajectory FPS") : "轨迹FPS",
    ("*", "Number of samples to take from trajectories per second") : "每秒从轨迹中获取的样本数",
    ("*", "Light FPS") : "轻FPS",
    ("*", "Number of samples to take from light programs per second") : "每秒从灯光程序中获取的样本数",
    ("*", "Plot positions") : "绘图位置",
    ("*", "Include position plot. Uncheck to exclude position plot from the output.") : "包括位置图。取消锁定以从输出中排除位置图。",
    ("*", "Plot velocities") : "绘图速度",
    ("*", "Include velocity plot. Uncheck to exclude velocity plot from the output.") : "包括速度图。取消锁定以从输出中排除速度图。",
    ("*", "Plot nearest neighbor") : "绘制最近的邻居",
    ("*", "Include nearest neighbor plot. Uncheck to exclude nearest neighbor plot from the output.") : "包括最近邻地块。取消选中可从输出中排除最近的邻居绘图。",
    ("*", "Plot all nearest neighbors") : "绘制所有最近的邻居",
    ("*", "Include all nearest neighbors plot. Uncheck to exclude all nearest neighbor plot from the output.") : "包括所有最近的邻居地块。取消选中可从输出中排除所有最近的邻居绘图。",
    ("*", "Create individual drone plots") : "创建单独的无人机绘图",
    ("*", "Include individual drone plots.Uncheck to exclude per-drone plots from the output.") : "包括单独的无人机绘图。取消锁定以从输出中排除每个无人机的绘图。",
    ("*", ".pdf validation plot exporter") : ".pdf验证图导出器",
    ("*", "Export Skybrush SKYC") : "导出 Skybrush SKYC",
    ("*", ".skyc exporter") : ".skyc出口商",
    ("*", "Fix Ordering of Transition Constraints") : "固定转换约束的顺序",
    ("*", "Fixes the ordering of transition constraints in the show") : "修复了节目中转换约束的顺序",
    ("*", "Formation Statistics") : "编队统计学",
    ("*", "Returns useful statistics about the currently selected formation in the Formations collection.") : "返回有关Formations集合中当前选定的编队的有用统计信息。",
    ("*", "Total Size") : "总尺寸",
    ("*", "Total number of targets in the formation, including simple meshes and vertex groups") : "编队中目标的总数，包括简单网格和顶点组",
    ("*", "# Vertices") : "#顶点",
    ("*", "Number of vertices in all the meshes of the formation that are designated as targets") : "指定为目标的编队所有网格中的顶点数",
    ("*", "# Empties") : "#空",
    ("*", "Number of empties in all the meshes of the formation that are designated as targets") : "指定为目标的编队所有网格中的空位数",
    ("*", "# Non-empties") : "#非清空",
    ("*", "Number of non-empties in all the meshes of the formation that are designated as targets") : "指定为目标的编队所有网格中的非空数",
    ("*", "Size") : "大小",
    ("*", "Size of the axis-aligned bounding box of the mesh in the current frame") : "当前帧中网格的轴对齐边界框的大小",
    ("*", "Minimum distance") : "最小距离",
    ("*", "Minimum distance of any pair of points within the formation") : "编队内任意一对点的最小距离",
    ("*", "Land Drones") : "陆地无人机",
    ("*", "Add a landing maneuver to all the drones") : "为所有无人机添加着陆动作",
    ("*", "at frame") : "在帧处",
    ("*", "Start frame of the landing maneuver") : "着陆机动的起始帧",
    ("*", "with velocity") : "带速度",
    ("*", "Average vertical velocity during the landing maneuver") : "着陆机动过程中的平均垂直速度",
    ("*", "to altitude") : "到海拔高度",
    ("*", "Altitude to land to") : "着陆高度",
    ("*", "At least one drone would have to land upwards by {dist}m") : "至少有一架无人机必须向上降落{dist}m",
    ("*", "Landing maneuver must not start before the last entry of the storyboard (frame {last_frame})") : "着陆机动不得在故事板的最后一个条目（帧{last_frame}）之前开始",
    ("Operator", "Move Selected Light Effect Down") : "向下移动选定的灯光效果",
    ("*", "Moves the selected light effect down by one slot in the light effect list") : "在灯光效果列表中将选定的灯光效果向下移动一个槽",
    ("Operator", "Move Selected Light Effect Up") : "向上移动选定的灯光效果",
    ("*", "Moves the selected light effect up by one slot in the light effect list") : "在灯光效果列表中将选定的灯光效果向上移动一个槽",
    ("Operator", "Move Selected Storyboard Entry Down") : "向下移动所选故事板条目",
    ("*", "Moves the selected entry down by one slot in the storyboard") : "将所选条目在故事板中下移一个槽",
    ("Operator", "Move Selected Storyboard Entry Up") : "向上移动所选故事板条目",
    ("*", "Moves the selected entry up by one slot in the storyboard") : "在故事板中将所选条目向上移动一个槽",
    ("*", "Prepare scene for Skybrush") : "为Skybrush准备场景",
    ("*", "mapping function called for storyboard entry with no formation") : "为没有格式的故事板条目调用映射函数",
    ("*", "Vertex {index}") : "顶点{index}",
    ("*", "Not enough time to plan staggered transition to formation {entry.name!r}. Try decreasing departure or arrival delay or allow more time for the transition.") : "没有足够的时间计划交错过渡到编队{entry.name!r}。请尝试减少起飞或抵达延迟，或留出更多时间进行过渡。",
    ("Operator", "Recalculate Transitions") : "重新计算过渡",
    ("*", "Recalculates all transitions in the show based on the current storyboard") : "基于当前故事板重新计算节目中的所有过渡",
    ("*", "Entire storyboard") : "整个故事板",
    ("*", "Current frame") : "当前帧",
    ("*", "To selected formation") : "至选定的编队",
    ("*", "From selected formation") : "从选定的编队",
    ("*", "From selected formation to end") : "从选定的编队到结束",
    ("*", "Scope") : "范围",
    ("*", "Scope of the operator that defines which transitions must be recalculated") : "定义必须重新计算哪些转换的运算符的作用域",
    ("*", "You need to create some drones first") : "你需要先制造一些无人机",
    ("*", "No transitions match the selected scope") : "没有与所选范围匹配的转换",
    ("*", "Remove Selected Formation") : "移除选定的编队",
    ("*", "Remove the selected formation from the show") : "从节目中删除选定的队形",
    ("Operator", "Remove Light Effect") : "移除灯光效果",
    ("*", "Remove the selected light effect from the show") : "从显示中删除选定的灯光效果",
    ("Operator", "Remove Selected Storyboard Entry") : "删除所选故事板条目",
    ("*", "Remove the selected entry from the storyboard") : "从故事板中删除所选条目",
    ("*", "Reorder Formation Markers") : "重新排列编队标记",
    ("*", "Re-orders individual markers within a formation") : "重新排序编队中的单个标记",
    ("*", "{self.type} method not implemented yet") : "{self.type}方法尚未实现",
    ("*", "Return Drones to Home Positions") : "将无人机返回原位",
    ("*", "Add a return-to-home maneuver to all the drones") : "为所有无人机添加返航机动",
    ("*", "Start frame of the return-to-home maneuver") : "返航机动的起始帧",
    ("*", "Average velocity during the return-to-home maneuver") : "返航机动过程中的平均速度",
    ("*", "Altitude to return-to-home to") : "返回原点的高度",
    ("Operator", "Return to home") : "返航",
    ("*", "Return to home maneuver must not start before the last entry of the storyboard (frame {last_frame})") : "不得在故事板的最后一个条目（帧{last_frame}）之前开始返航机动",
    ("Operator", "Select Storyboard Entry for Current Frame") : "为当前帧选择故事板条目",
    ("*", "Select the storyboard entry that contains the current frame. If the current frame falls between storyboard entries, selects the next entry. Clears the selection if the current frame is after the end of the storyboard.") : "选择包含当前帧的故事板条目。如果当前帧位于故事板条目之间，则选择下一个条目。如果当前帧在存储板的末尾之后，则清除所选内容。",
    ("*", "Swap Colors in LED Control Panel") : "交换LED控制面板中的颜色",
    ("*", "Swaps the current primary and secondary colors in the LED control panel.") : "交换LED控制面板中的当前主色和次色。",
    ("Operator", "Takeoff") : "起飞",
    ("*", "Add a takeoff maneuver to all the drones") : "为所有无人机添加起飞动作",
    ("*", "Start frame of the takeoff maneuver") : "起飞机动的起始帧",
    ("*", "Average vertical velocity during the takeoff maneuver") : "起飞机动过程中的平均垂直速度",
    ("*", "Altitude to take off to") : "起飞高度",
    ("*", "Relative Altitude") : "相对海拔高度",
    ("*", "Specifies whether the takeoff altitude is relative to the current altitude of the drone") : "指定起飞高度是否相对于无人机的当前高度",
    ("*", "At least one drone would have to take off downwards by {dist}m") : "至少有一架无人机必须向下起飞{dist}m",
    ("*", "Takeoff maneuver needs at least {takeoff_duration} frames; there is not enough time after the first entry of the storyboard (frame {first_frame})") : "起飞机动至少需要{takefff_duration}帧；在存储板的第一个条目（帧{first_frame}）之后没有足够的时间",
    ("*", "Takeoff maneuver must start after the first (takeoff grid) entry of the storyboard (frame {frame})") : "起飞机动必须在故事板（第{frame}帧）的第一个（起飞网格）条目之后开始",
    ("*", "Takeoff maneuver must start before the second entry of the storyboard (frame {frame})") : "起飞机动必须在故事板第二次进入之前开始（第{frame}）",
    ("*", "Empty") : "空的",
    ("*", "Current positions of drones") : "无人机的当前位置",
    ("*", "Selected objects") : "选定的对象",
    ("*", "Current positions of selected objects") : "选定对象的当前位置",
    ("*", "Current positions of selected vertices") : "选定顶点的当前位置",
    ("*", "Update Selected Formation") : "更新选定的编队",
    ("*", "Update the selected formation from the current selection or from the current positions of the drones") : "根据无人机的当前选择或当前位置更新所选编队",
    ("*", "Update with") : "使用更新",
    ("*", "Update Frame Range from Storyboard") : "从故事板更新帧范围",
    ("*", "Updates the frame range to be synchronized with the storyboard") : "更新要与故事板同步的帧范围",
    ("*", "Update Time Markers from Storyboard") : "从故事板更新时间标记",
    ("*", "Update all time markers to be synchronized with the storyboard") : "更新所有要与故事板同步的时间标记",
    ("*", "Use Selected Vertex Group for Formation") : "使用选定顶点组进行编组",
    ("*", "Sets the current vertex group as the one that should be used as targets when the object is placed in a formation.") : "将当前顶点组设置为将对象放置在队形中时应用作目标的顶点组。",
    ("*", "Exporting show content to {filepath}") : "正在将节目内容导出到{filepath}",
    ("*", "Getting frame range from {}") : "正在从{}获取帧范围",
    ("*", "Selected frame range is empty") : "所选帧范围为空",
    ("*", "No objects were selected; export cancelled") : "未选择任何对象；出口已取消",
    ("*", "There are no objects to export; export cancelled") : "没有要导出的对象；出口已取消",
    ("*", "Getting object trajectories and light programs") : "获取对象轨迹和灯光程序",
    ("*", "Exporting show to .skyc") : "正在将节目导出到.skyc",
    ("*", "Exporting show to CSV") : "将节目导出为CSV",
    ("*", "Exporting validation plots to .pdf") : "将验证图导出为.pdf",
    ("*", "Export finished") : "导出已完成",
    ("Operator", "Validate Trajectories") : "验证轨迹",
    ("*", "Validates the trajectories of the drones in a given frame range.") : "验证无人机在给定帧范围内的轨迹。",
    ("*", "Selection only") : "仅选择",
    ("*", "Validate only the selected drones. Uncheck to export all drones, irrespectively of the selection.") : "仅验证选定的无人机。取消确认导出所有无人机，无论选择如何。",
    ("*", "Error while checking whether Skybrush Viewer is running") : "检查Skybrush Viewer是否正在运行时出错",
    ("*", "Skybrush Viewer is not running; please start it and try again") : "Skybrush Viewer未运行；请启动它，然后再试一次",
    ("*", "Now switch to the Skybrush Viewer window to view the results") : "现在切换到Skybrush Viewer窗口以查看结果",
    ("*", "Error while sending show data to Skybrush Viewer") : "将显示数据发送到Skybrush Viewer时出错",
    ("*", "Clearance") : "清除",
    ("*", "Not implemented yet") : "尚未实施",
    ("*", "API Key") : "API密钥",
    ("*", "API Key that is used when communicating with the Skybrush Studio server") : "与Skybrush Studio服务器通信时使用的API密钥",
    ("*", "Server URL") : "服务器URL",
    ("*", "URL of a dedicated Skybrush Studio server if you are using a dedicated server. Leave it empty to use the server provided for the community for free") : "如果您正在使用专用服务器，则Skybrush Studio专用服务器的URL。将其留空以免费使用为社区提供的服务器",
    ("*", "Restart Blender if you change the settings above.") : "如果您更改了上述设置，请重新启动Blender。",
    ("*", "Enabled") : "启用",
    ("*", "Whether this light effect is enabled") : "是否启用此灯光效果",
    ("*", "Start Frame") : "开始帧",
    ("*", "Frame when this light effect should start in the show") : "该灯光效果应在演出中开始的帧",
    ("*", "Duration") : "期间",
    ("*", "Duration of this light effect") : "此灯光效果的持续时间",
    ("*", "Duration of the fade-in part of this light effect") : "此灯光效果部分的淡入持续时间",
    ("*", "Duration of the fade-out part of this light effect") : "此灯光效果的淡出部分的持续时间",
    ("*", "Duration of this formation") : "形成时间",
    ("*", "Fade in") : "淡入",
    ("*", "Fade out") : "淡出",
    ("*", "Color ramp") : "颜色渐变",
    ("*", "LEDs") : "灯光",
    ("*", "Function") : "函数",
    ("*", "Output X") : "输出",
    ("*", "Output function that determines the value that is passed through the color ramp to obtain the color to assign to a drone") : "输出函数，用于确定通过颜色渐变以获得要分配给无人机的颜色的值",
    ("*", "First color") : "起始颜色",
    ("*", "Last color") : "终止颜色",
    ("*", "Indexed by drones") : "无人机序号",
    ("*", "Indexed by formation") : "编队序号",
    ("*", "Invert target") : "反转目标",
    ("*", "Gradient") : "渐变",
    ("*", "Gradient (XYZ)") : "渐变（XYZ）",
    ("*", "Gradient (XZY)") : "渐变（XZY）",
    ("*", "Gradient (YXZ)") : "渐变（YXZ）",
    ("*", "Gradient (YZX)") : "渐变（YZX）",
    ("*", "Gradient (ZXY)") : "渐变（ZXY）",
    ("*", "Gradient (ZYX)") : "渐变（ZYX）",
    ("*", "Temporal") : "时间",
    ("*", "Distance from mesh") : "与网格的距离",
    ("*", "Custom expression") : "自定义表达式",
    ("*", "Mapping") : "映射",
    ("*", "Specifies how the output value should be mapped to the [0; 1] range of the color ramp") : "指定输出值应如何映射到颜色渐变的[0；1]范围",
    ("*", "Ordered") : "命令",
    ("*", "Proportional") : "相称的",
    ("*", "Influence") : "影响",
    ("*", "Influence of this light effect on the final color of drones") : "这种灯光效果对无人机最终颜色的影响",
    ("*", "Texture") : "纹理",
    ("*", "Texture of the light effect, used for the sole purpose of having a way to create a color ramp") : "灯光效果的纹理，用于创建颜色渐变的唯一目的",
    ("*", "Mesh") : "网格",
    ("*", "Mesh related to the light effect; used when the output is set to \"Distance\" or to limit the light effect to the inside or one side of this mesh when \"Inside the mesh\" or \"Front side of plane\" is checked") : "与灯光效果相关的网格；当输出设置为“距离”时使用，或当选中“网格内部”或“平面前侧”时将灯光效果限制在此网格的内部或一侧",
    ("*", "Target") : "目标",
    ("*", "Specifies whether to apply this light effect to all drones or only to those drones that are inside the given mesh or are in front of the plane of the first face of the mesh") : "指定是将此灯光效果应用于所有无人机，还是仅应用于给定网格内或网格第一面的平面前的无人机",
    ("*", "All drones") : "所有无人机",
    ("*", "Inside the mesh") : "网格内部",
    ("*", "Front side of plane") : "飞机前侧",
    ("*", "Randomness") : "随机性",
    ("*", "Offsets the output value of each drone randomly, wrapped aroundthe edges of the color ramp; this property defines the maximumrange of the offset") : "随机偏移每个无人机的输出值，缠绕在颜色渐变的边缘；该属性定义偏移量的最大范围",
    ("*", "Blend mode") : "混合模式",
    ("*", "Specifies the blending mode of this light effect") : "指定此灯光效果的混合模式",
    ("*", "Selected index") : "选定的索引",
    ("*", "Index of the light effect currently being edited") : "当前正在编辑的灯光效果的索引",
    ("*", "Texture for light effect") : "灯光效果的纹理",
    ("*", "no selected entry in light effect list") : "灯光效果列表中没有选定的条目",
    ("*", "Copy of {active_entry.name}") : "{active_entry.name}的副本",
    ("*", "Formation vertex group") : "编队顶点组",
    ("*", "Name of the vertex group designated for containing the vertices that the drones should occupy when their parent object is placed in the storyboard") : "顶点组的名称，该顶点组指定用于包含无人机在其父对象放置在故事板中时应占据的顶点",
    ("*", "Formation status") : "形成状态",
    ("*", "The string representation of the formation status at the given frame") : "给定帧的编队状态的字符串表示",
    ("*", "Enable safety checks") : "启用安全检查",
    ("*", "Enables real-time safety checks that compare the altitudes, distances and velocities of drones with a safety threshold in every frame. Turn this off if performance suffers during playback") : "实现实时安全检查，将无人机的高度、距离和凸度与每帧中的安全阈值进行比较。如果播放过程中性能受到影响，请关闭此选项",
    ("*", "Min distance") : "最小距离",
    ("*", "Minimum distance along all possible pairs of drones in the current frame, calculated between their centers of mass") : "当前帧中所有可能的无人机对的最小距离，计算它们的质心之间的距离",
    ("*", "Min altitude") : "最低海拔高度",
    ("*", "Minimum altitude of all drones in the current frame") : "当前帧中所有无人机的最小高度",
    ("*", "Max altitude") : "最大海拔高度",
    ("*", "Maximum altitude of all drones in the current frame") : "当前帧中所有无人机的最大高度",
    ("*", "Max XY velocity") : "最大XY速度",
    ("*", "Maximum horizontal velocity of all drones in the current frame") : "当前帧中所有无人机的最大水平速度",
    ("*", "Max Z velocity") : "最大Z速度",
    ("*", "Maximum vertical velocity of all drones in the current frame upwards") : "当前帧中所有无人机的最大垂直速度向上",
    ("*", "Maximum vertical velocity of all drones in the current frame downwards") : "当前帧中所有无人机的最大垂直速度向下",
    ("*", "Show proximity warnings") : "显示接近警告",
    ("*", "Specifies whether Blender should show a warning in this panel when the minimum distance is less than the proximity warning threshold") : "指定当最小距离小于接近警告阈值时，Blender是否应在此面板中显示警告",
    ("*", "Proximity warning threshold") : "接近警告阈值",
    ("*", "Minimum allowed distance between drones without triggering a proximity warning") : "无人机之间不触发接近警告的最小允许距离",
    ("*", "Show altitude warnings") : "显示高度警告",
    ("*", "Specifies whether Blender should show a warning when the altitude of a drone is larger than the altitude warning threshold") : "指定当飞机的高度大于高度警告阈值时，Blender是否应显示警告",
    ("*", "Altitude warning threshold") : "高度警告阈值",
    ("*", "Maximum allowed altitude for a single drone without triggering an altitude warning") : "无人机在不触发高度警告的情况下的最大允许高度",
    ("*", "Show velocity warnings") : "显示速度警告",
    ("*", "Specifies whether Blender should show a warning when the velocity of a drone is larger than the velocity warning threshold") : "指定当龙的速度大于速度警告阈值时，Blender是否应显示警告",
    ("*", "Maximum XY velocity") : "最大XY速度",
    ("*", "Maximum velocity allowed in the horizontal plane") : "水平面内允许的最大速度",
    ("*", "Maximum Z velocity") : "最大Z速度",
    ("*", "Maximum velocity allowed in the vertical direction") : "垂直方向上允许的最大速度",
    ("*", "Use separate Z velocity threshold upwards") : "向上使用单独的Z速度阈值",
    ("*", "When checked, the velocity threshold in the Z direction is allowed to be different upwards and downwards") : "检查时，允许Z方向上的速度阈值向上和向下不同",
    ("*", "Maximum Z velocity (up)") : "最大Z速度（向上）",
    ("*", "Maximum velocity allowed upwards in the vertical direction") : "垂直方向上允许的最大速度",
    ("*", "Names of the timeline markers that were created by the plugin and that may be removed when the 'Update Time Markers' operation is triggered") : "由插件创建的时间线标记的名称，当触发“更新时间标记”操作时，这些标记可能会被删除",
    ("*", "Emission") : "排放",
    ("*", "Specifies the light emission strength of the drone meshes") : "指定无人机网格的发光强度",
    ("*", "Identifier") : "标识符",
    ("*", "Unique identifier for this storyboard entry; must not change throughout the lifetime of the entry.") : "此故事板条目的唯一标识符；在条目的整个生命周期内不得更改。",
    ("*", "Custom Name") : "自定义名称",
    ("*", "Keeps the name of the storyboard entry when the associated formation changes") : "当关联的格式更改时，保留故事板条目的名称",
    ("*", "Formation to use in this storyboard entry. Leave empty to mark this interval in the show as a segment that should not be affected by formation constraints") : "要在此故事板条目中使用的格式。保留为空以将该间隔标记为不受信息约束影响的片段",
    ("*", "Frame when this formation should start in the show") : "该队形应在表演中开始的时间",
    ("*", "Manual") : "手册",
    ("*", "Auto") : "汽车",
    ("*", "Type") : "类型",
    ("*", "Type of transition between the previous formation and this one. Manual transitions map the nth vertex of the initial formation to the nth vertex of the target formation; auto-matched transitions find an optimal mapping between vertices of the initial and the target formation") : "上一个编队和本编队之间的过渡类型。\手动转换将初始编队的第n个顶点映射到目标编队的第n个顶点；自动匹配过渡在初始形态和目标形态的顶点之间找到最优映射",
    ("*", "Synchronized") : "已同步",
    ("*", "Staggered") : "交错的",
    ("*", "Schedule") : "日程",
    ("*", "Time schedule of departures and arrivals during the transition between the previous formation and this one. Note that collision-free trajectories are guaranteed only for synchronized transitions") : "在上一次编队和本次编队之间的过渡期间出发和到达的时间表。请注意，只有同步转换才能保证无冲突的对象",
    ("*", "Departure delay") : "发车延迟",
    ("*", "Number of frames to wait between the start times of drones in a staggered transition") : "交错过渡中无人机开始时间之间等待的帧数",
    ("*", "Arrival delay") : "到达延迟",
    ("*", "Number of frames to wait between the arrival times of drones in a staggered transition") : "交错过渡中无人机到达时间之间等待的帧数",
    ("*", "Index of the storyboard entry currently being edited") : "当前正在编辑的故事板条目的索引",
    ("*", "at least one of the name and the formation must be specified") : "必须至少指定名称和格式中的一个",
    ("*", "Storyboard entry {entry.name!r} at index {index + 1} and frame {next_entry.frame_start} overlaps with next entry {next_entry.name!r}") : "索引{index+1}和帧{next_entry.frame_start}处的故事板条目{entry.name!r}与下一个条目重叠",
    ("*", "you only have {num_drones} drones") : "你只有{num_drones}无人机",
    ("*", "you only have one drone") : "你只有一架无人机",
    ("*", "you have no drones") : "你没有无人机",
    ("*", "Storyboard entry {entry.name!r} contains a formation with {num_markers} drones but {msg}") : "故事板条目{entry.name!r}包含一个包含{num_markers}无人机但包含{msg}的编队",
    ("*", "Min distance: {safety_check.min_distance:.1f} m") : "最小距离：{safety_check.Min_distance:.1f}m",
    ("*", "Altitude: {safety_check.min_altitude:.1f} - {safety_check.max_altitude:.1f} m") : "海拔高度：{safety_check.min_Altitude:.1f}-{safety_check.max_Altitude:.1f}m",
    ("*", "Max velocity XY: {safety_check.max_velocity_xy:.1f} m/s | U: {safety_check.max_velocity_z_up:.1f} m/s | D: {safety_check.max_velocity_z_down:.1f} m/s") : "最大速度XY:{safety_check.Max_velocity_XY:.1f}m/s |U:{afety_check.Max_velocity_z_up:.1f}",
    ("*", "Export") : "导出",
    ("*", "Safety & Export") : "安全与导出",
    ("Operator", "Export to .skyc") : "导出到.skyc",
    ("Operator", "Export to .csv") : "导出到.csv",
    ("Operator", "Export validation report") : "导出验证报告",
    ("*", "Formations") : "编队",
    ("*", "Select") : "选择",
    ("*", "Deselect") : "取消选择",
    ("*", "Stats") : "统计数据",
    ("*", "Append to Storyboard") : "附加到故事板",
    ("*", "Update") : "使现代化",
    ("Operator", "Reorder") : "重新排序",
    ("*", "LED Control") : "LED控制",
    ("*", "Primary") : "主要的，重要的",
    ("*", "Secondary") : "次要的",
    ("*", "Apply") : "申请",
    ("Operator", "Fade to") : "淡入淡出",
    ("*", "Light Effects") : "灯光效果",
    ("*", "Drone Show") : "无人机表演",
    ("*", "Name of Formation Vertex Group:") : "编队顶点组名称：",
    ("*", "Use selected") : "使用选定的",
    ("*", "Safety Check") : "安全检查",
    ("*", "Down") : "向下",
    ("*", "Up") : "向上的",
    ("*", "Storyboard") : "故事板",
    ("Operator", "Update Time Markers") : "更新时间标记",
    ("*", "{duration} frames") : "{duration}帧",
    ("*", "Single-frame transition") : "单帧过渡",
    ("*", "Zero-frame transition") : "零帧转换",
    ("*", "Recalculate") : "重新计算",
    ("*", "Transition from previous") : "从上一个过渡",
    ("*", "Edits the transition into the currently selected formation") : "编辑过渡到当前选定的形状",
    ("*", "Transition to next") : "过渡到下一个",
    ("*", "Edits the transition to the formation that follows the currently selected formation") : "编辑过渡到当前选定形状之后的形状",
    ("*", "Frame range") : "帧范围",
    ("*", "Choose a frame range to use for this operation") : "选择用于此操作的帧范围",
    ("*", "Use the storyboard to define frame range") : "使用序列图像板定义帧范围",
    ("*", "Use global render frame range set by scene") : "使用由场景设置的全局渲染帧范围",
    ("*", "Use global preview frame range set by scene") : "使用由场景设置的全局预览帧范围",
    ("*", "Current formation or transition") : "电流形成或过渡",
    ("*", "Use the formation or transition containing the current frame") : "使用包含当前帧的格式或过渡",
    ("*", "Unknown frame range: {range!r}") : "未知帧范围：{range!r}",
    ("*", "selector must be string or callable") : "选择器必须是字符串或可调用的",
    ("*", "No such object in collection: {0!r}") : "集合中没有这样的对象：{0!r}",
    ("*", "collection needs move(), link() or unlink() methods") : "集合需要move（）、link（）或unlink（）方法",
    ("*", "no screen given") : "没有给出屏幕",
    ("*", "no scene given") : "没有给出场景",
    ("*", "Error while invoking {what} on the Skybrush Studio online service") : "在Skybrush Studio在线服务上调用{what}时出错",
    ("*", "Drones") : "无人机",
    ("*", "Templates") : "模板",
    ("*", "Drone template") : "无人机模板",
    ("*", "Drone template material") : "无人机模板材料",
    ("*", "Cannot set all keyframes") : "无法设置所有关键帧",
    ("*", "no shader node with type {type!r} in material") : "材质中没有类型为{type!r}的着色器节点",
    ("*", "{material.name} Shader Nodetree Action") : "{material.name}着色器节点树操作",
    ("*", "Principled BSDF") : "原理BSDF",
    ("*", "Material does not have a diffuse color shader node") : "材质没有漫反射颜色着色器节点",
    ("*", "{obj.name} Mesh") : "{obj.name}网格",
    ("*", "Invalid response received from Skybrush Viewer") : "从Skybrush Viewer接收到无效响应",
    ("*", "Skybrush Viewer indicated an unexpected error") : "Skybrush Viewer指示出现意外错误",
    ("*", "Skybrush Viewer indicated that the input format is invalid") : "Skybrush Viewer指示输入格式无效",
    ("*", "Formation") : "编队",
    ("*", "Previous Entry") : "前置条目",
    ("*", "HH & Export") : "汉航 & 导出",
    ("*", "HH Plugins") : "汉航插件",
    ("Operator", "Create Frame Data") : "创建真实帧数据",
    ("Operator", "Export HH Frame Data") : "导出汉航帧数据",
    ("*", "Frame data") : "帧数据",
    ("*", "For example: 1-2, 3, 5, 50-100") : "例如：1-2,3,5,50-100",
    ("*", "Path") : "路径",
    ("*", "Path of the imported image") : "导入图片路径",
    ("*", "The minimum distance for imported image") : "导入图片中两点间的最小距离",
    ("*", "Calculate Path Start Frame") : "计算路径开始帧",
    ("*", "Calculate Path End Frame") : "计算路径结束帧",
    ("*", "The minimum distance between the aircraft when calculating the path") : "计算路径时飞机最小间距",
    ("*", "The frames per second (FPS) when calculating the path") : "计算路径时的帧率",
    ("*", "Inserting keyframes at intervals") : "间隔插帧",
    ("*", "Insert a keyframe every X frames") : "插帧时间隔多少帧插一帧",
    ("*", "Max velocity") : "最大速度",
    ("*", "The maximum velocity when calculating the path") : "计算路径时最大速度",
    ("*", "Select image") : "从图片导入",
    ("Operator", "Choose Image") : "导入图片",
    ("Operator", "Select image") : "从图片导入",
    ("*", "Calculate path:") : "计算路径：",
    ("*", "Calculate path (waiting, maximum velocity)") : "计算路径(等待、最大速度)",
    ("*", "Calculate path (average velocity)") : "计算路径(平均速度)",
    ("*", "Clear path") : "清除路径",
    ("*", "Insert path keyframe") : "插入路径帧",
    ("*", "Clear path keyframe") : "清除路径帧",
    ("Operator", "Calculate path (waiting, maximum velocity)") : "计算路径(等待、最大速度)",
    ("Operator", "Calculate path (average velocity)") : "计算路径(平均速度)",
    ("Operator", "Clear path") : "清除路径",
    ("Operator", "Insert path keyframe") : "插入路径帧",
    ("Operator", "Clear path keyframe") : "清除路径帧",
    ("*", "Calculate takeoff and landing path:") : "计算起飞降落路径：",
    ("Operator", "Calculate group takeoff") : "计算分组起飞",
    ("*", "Single color:") : "单一颜色：",
    ("*", "Random Color:") : "随机颜色：",
    ("*", "Channel Filtering:") : "通道过滤：",
    ("Operator", "Red") : "红 色",
    ("Operator", "Blue") : "蓝 色",
    ("Operator", "Yellow") : "黄 色",
    ("Operator", "Green") : "绿 色",
    ("Operator", "White") : "白 色",
    ("Operator", "Black") : "黑 色",
    ("Operator", "Pink") : "粉 红",
    ("Operator", "Sky Blue") : "天 蓝",
    ("Operator", "Purple") : "紫 色",
    ("Operator", "Orange") : "橙 色",
    ("Operator", "Cyan") : "青 色",
    ("Operator", "Blue-Purple") : "蓝紫色",
    ("Operator", "Orange-Yellow") : "橙黄色",
    ("Operator", "Magenta") : "紫红色",
    ("Operator", "Blue-Green") : "蓝绿色",
    ("Operator", "Light Blue") : "浅蓝色",
    ("Operator", "Random Color") : "随机色",
    ("Operator", "Yellow-Lime-Cyan") : "黄兰青",
    ("Operator", "Red-Yellow-Purple") : "红黄紫",
    ("Operator", "Purple-Blue-Cyan") : "紫蓝青",
    ("Operator", "Disable Material Channel") : "关闭材质通道",
    ("Operator", "Enable Material Channel") : "开启材质通道",
    ("Operator", "Disable Transform Channel") : "关闭变换通道",
    ("Operator", "Enable Transform Channel") : "开启变换通道",
    ("*", "Calculate group takeoff path") : "计算分组起飞路径",
    ("*", "Calculate group takeoff path with staggered takeoff for each group") : "计算起飞时的分组路径，使每组都间隔起飞",
    ("*", "Minimum Altitude") : "最低高度",
    ("*", "Minimum Altitude of the Bottom Layer") : "最下面一层的最低高度",
    ("*", "Spacing Between Drones") : "间隔飞机",
    ("*", "Spacing Between Aircraft Takeoff Count") : "间隔飞机起飞个数",
    ("*", "Delete constraints and generate keyframe data for entities") : "删除约束生成实体帧数据",
    ("*", "Minimum Import Distance") : "最小导入距离",
    ("*", "fps") : "帧率",
    ("*", "Schedule overrides") : "计划覆盖",
    ("*", "Schedule overrides enabled") : "已启用计划覆盖",
    ("*", "Whether the schedule overrides associated to the current entry are enabled") : "是否启用与当前条目关联的计划覆盖",
    ("*", "Whether the transition is locked. Locked transitions are never re-calculated") : "过渡是否已锁定，锁定的过渡永远不会重新计算",
    ("*", "Generate Markers") : "生成标记",
    ("Operator", "From static CSV file") : "从静态CSV文件",
    ("Operator", "From zipped CSV files") : "从压缩CSV文件",
    ("Operator", "From SVG file") : "从SVG文件",
    ("Operator", "From QR Code") : "从二维码",
    ("*", "Whether the transition is locked. Locked transitions are never re-calculated") : "过渡是否已锁定，锁定的过渡永远不会重新计算",
    ("Operator", "Refresh file formats") : "刷新文件格式",
    ("*", "Queries the supported file formats from the server") : "从服务器查询支持的文件格式",
    ("*", "Keep lighting effect") : "保留刷光效果",
    ("*", "Framerate") : "帧率",
}


translation_dict = {}


if bpy.app.version[0] < 4: # < 4.0.1
    translation_dict["zh_CN"] = translation_zh_CN
else: # >= 4.0.1
    translation_dict["zh_HANS"] = translation_zh_CN

def register() -> None:
    bpy.app.translations.unregister(__name__)
    bpy.app.translations.register(__name__, translation_dict)

def unregister() -> None:
    bpy.app.translations.unregister(__name__)

def gettext(lstr) -> None:
    return bpy.app.translations.pgettext(lstr)
