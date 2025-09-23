import bpy
import math
from bpy.props import StringProperty

class OBJECT_OT_calculate_distance(bpy.types.Operator):
    """计算选中的两个物体之间的距离"""
    bl_idname = "object.calculate_distance"
    bl_label = "计算物体距离"
    bl_options = {'REGISTER', 'UNDO'}

    # 用于在信息窗口显示结果的属性
    result_message: StringProperty()

    def execute(self, context):
        # 获取当前选中的物体
        selected_objects = context.selected_objects

        # 检查是否选中了恰好两个物体
        if len(selected_objects) != 2:
            self.report({'ERROR'}, "请确保只选中了两个物体")
            return {'CANCELLED'}

        # 获取两个物体
        obj1, obj2 = selected_objects[0], selected_objects[1]

        # 获取物体的位置（世界坐标系）
        loc1 = obj1.location
        loc2 = obj2.location

        # 计算三维空间中的距离
        distance = math.sqrt(
            (loc2.x - loc1.x)**2 +
            (loc2.y - loc1.y)** 2 +
            (loc2.z - loc1.z)**2
        )

        # 准备结果消息
        result = f"物体 '{obj1.name}' 和 '{obj2.name}' 之间的距离为: {distance:.4f} 单位"
        self.result_message = result

        # 显示结果
        self.report({'INFO'}, result)
        print(result)
        print(f"坐标1: ({loc1.x:.4f}, {loc1.y:.4f}, {loc1.z:.4f})")
        print(f"坐标2: ({loc2.x:.4f}, {loc2.y:.4f}, {loc2.z:.4f})")

        return {'FINISHED'}

# 注册快捷键
addon_keymaps = []

def register_keymaps():
    wm = bpy.context.window_manager
    # 检查是否已存在keymap
    km = wm.keyconfigs.addon.keymaps.get("3D View Generic")
    if not km:
        km = wm.keyconfigs.addon.keymaps.new(name="3D View Generic", space_type='VIEW_3D')

    # 添加快捷键: Ctrl+Shift+D
    kmi = km.keymap_items.new(
        OBJECT_OT_calculate_distance.bl_idname,
        'D', 'PRESS',
        ctrl=True, shift=True
    )

    addon_keymaps.append((km, kmi))

def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

# 注册和注销函数
def register():
    bpy.utils.register_class(OBJECT_OT_calculate_distance)
    register_keymaps()

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_calculate_distance)
    unregister_keymaps()

if __name__ == "__main__":
    register()
