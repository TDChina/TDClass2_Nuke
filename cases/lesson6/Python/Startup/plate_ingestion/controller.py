import hiero_utils

class PlateIngestionController(object):
    def __init__(self, view, model, selection):
        super(PlateIngestionController, self).__init__()
        self.view = view
        self.model = model
        self.trackitems = hiero_utils.get_selection(selection)
        self.connect_signal_slot()

    def show_panel(self):
        self.view.show()

    def connect_signal_slot(self):
        self.view.tagButton.clicked.connect(self.generate_tag)

    def generate_tag(self):
        if str(self.view.seqEdit.text()) == "" or str(self.view.fromEdit.text()) == "" or str(self.view.stepEdit.text()) == "":
            self.view.show_message('shot information missing.\n please check edit fields.')
        elif self.view.showTypeList.currentText() == "TV series" and str(self.view.episodeEdit.text()) == "":
            self.view.show_message('shot information missing.\n please check edit fields.')
        else:
            try:
                seq = self.view.seqEdit.text()
                shotnum = int(self.view.fromEdit.text())
                step = int(self.view.stepEdit.text())
                if hiero_utils.generate_tag(self.trackitems, seq, shotnum, step):
                    row_count = self.view.shotCodeForm.rowCount()
                    for row in range(0, row_count):
                        self.view.shotCodeForm.removeRow(0)
                    self.view.set_shotcode_list(self.trackitems)
                    self.view.messageLabel.setText('all tags generated successfully.')
            except:
                self.view.messageLabel.setText('failed to generate tags.')
