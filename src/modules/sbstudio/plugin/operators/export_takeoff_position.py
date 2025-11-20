import bpy
import json

from sbstudio.plugin.constants import Collections
from sbstudio.plugin.utils.evaluator import get_position_of_object

class SkybrushExportTakeoffPositionOperator(bpy.types.Operator):
    bl_idname = 'skybrush.export_takeoff_position'
    bl_label = 'Export takeoff position'
    bl_description = 'Export the drone takeoff position as a json file'
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(
        name="文件路径",
        description="要保存的文件路径",
        default="",
        subtype='FILE_PATH'
    )

    def execute(self, context):
        if not self.filepath:
            return {"CANCELLED"}
        context.scene.frame_set(1)
        points = []
        for drone in Collections.find_drones(create=False).objects:
            points.append(get_position_of_object(drone))
        try:
            open(self.filepath, "w").write(json.dumps(points))
        except Exception as ex:
            self.report({"ERROR"}, f"保存文件失败: {ex}")
            return {"CANCELLED"}
        return {"FINISHED"}

    def invoke(self, context, event):
        if not self.filepath:
            self.filepath = "起飞位置.json"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
