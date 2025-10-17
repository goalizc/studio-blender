import bpy

class SkybrushShowMessageOperator(bpy.types.Operator):
    """只显示确认按钮的弹窗"""
    bl_idname = "skybrush.show_message"
    bl_label = "消息提示"
    bl_options = {'REGISTER', 'INTERNAL'}

    message: bpy.props.StringProperty(default="")
    title: bpy.props.StringProperty(default="提示")
    icon: bpy.props.StringProperty(default='INFO')

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text=self.message, icon=self.icon)

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=300)
