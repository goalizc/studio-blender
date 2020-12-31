from bpy.types import Operator

from sbstudio.plugin.selection import select_only


class FormationOperator(Operator):
    """Operator mixin that allows an operator to be executed if we have a
    selected formation in the current scene.
    """

    @classmethod
    def poll(cls, context):
        return (
            context.scene.skybrush
            and context.scene.skybrush.formations
            and (
                getattr(cls, "works_with_no_selected_formation", False)
                or context.scene.skybrush.formations.selected
            )
        )

    def execute(self, context):
        formation = context.scene.skybrush.formations.selected
        return self.execute_on_formation(formation, context)

    def select_formation(self, formation, context) -> None:
        """Selects the given formation, both in the scene and in the formations
        panel.
        """
        select_only(formation)
        if context.scene.skybrush.formations:
            context.scene.skybrush.formations.selected = formation


class StoryboardOperator(Operator):
    """Operator mixin that allows an operator to be executed if we have a
    storyboard in the current scene.
    """

    @classmethod
    def poll(cls, context):
        return context.scene.skybrush and context.scene.skybrush.storyboard

    def execute(self, context):
        storyboard = context.scene.skybrush.storyboard
        return self.execute_on_storyboard(storyboard, context)
