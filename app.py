from mcedit import *
from PyQt5.QtWidgets import *

from signeditpanel import *
from options import *

class SignApp(QApplication):

    current_panel : EditPanel
    options : Options


    def __init__(self, argv):
        super(SignApp, self).__init__(argv)

    def currentEditPanel(self) -> EditPanel:
        return self.current_panel

    def setCurrentPanel(self, editor: EditPanel):
        self.current_panel = editor

    def options(self):
        return self.options

    def setOptions(self, options):
        self.options = options