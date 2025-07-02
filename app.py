from mcedit import *
from PyQt5.QtWidgets import *

from signeditpanel import *


class SignApp(QApplication):

    current_editor : EditPanel

    def __init__(self, argv):
        super(SignApp, self).__init__(argv)

    def getCurrentEditor(self) -> EditPanel:
        return self.current_editor

    def setCurrentEditor(self, editor: EditPanel):
        self.current_editor = editor