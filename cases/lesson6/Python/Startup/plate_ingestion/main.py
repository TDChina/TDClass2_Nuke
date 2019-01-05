import hiero.core as hcore


import view
import model
import controller

reload(view)
reload(model)
reload(controller)

class NukeStudioMenu(object):
    def __init__(self):
        super(NukeStudioMenu, self).__init__()
        hcore.events.registerInterest("kShowContextMenu/kTimeline", self.create_menu)

    def create_menu(self, event):
        event.menu.addAction('Plate Ingestion', self.show_tool_panel)
        self.selection = event.sender.selection()

    def show_tool_panel(self):
        self.view = view.PlateIngestionUI()
        self.model = model.PlateIngestionModel()
        self.tool = controller.PlateIngestionController(self.view, self.model, self.selection)
        self.tool.show_panel()
