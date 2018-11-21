class ElementLoaderController(object):
    def __init__(self, view, model, version_combo):
        super(ElementLoaderController, self).__init__()
        self.view = view
        self.model = model
        self.version_combo = version_combo
        self.connect_signal_slot()

    def connect_signal_slot(self):
        self.view.sequence_list.currentIndexChanged.connect(self.update_shot_list)
        self.view.shot_list.currentIndexChanged.connect(self.update_task)

    def set_context(self):
        if self.model.match:
            self.view.set_project(self.model.info['project'])
            sequences = self.model.search_sequences()
            self.view.set_sequence(sequences)
            if self.model.info['sequence'] in sequences:
                self.view.sequence_list.setCurrentIndex(sequences.index(self.model.info['sequence']))
            sequence = str(self.view.sequence_list.currentText())
            shots = self.model.search_shots(sequence)
            self.view.set_shot(shots)
            if self.model.info['shot'] in shots:
                self.view.shot_list.setCurrentIndex(shots.index(self.model.info['shot']))

    def update_shot_list(self):
        sequence = self.view.sequence_list.currentText()
        shots = self.model.search_shots(sequence)
        self.view.set_shot(shots)

    def update_task(self):
        sequence = self.view.sequence_list.currentText()
        shot = self.view.shot_list.currentText()
        tasks = self.model.search_task(sequence, shot)
        self.view.clear_table()
        row_count = 0
        for task in tasks:
            #version_combo = self.version_combo
            #version_combo.set_value(row_count, task)
            #versions = self.model.search_versions(sequence, shot, task)
            # if versions:
            #     version_combo.addItems()
            self.view.set_task(row_count, task)
            row_count += 1
