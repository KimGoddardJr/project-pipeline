from PySide2 import QtCore, QtGui
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import *
import os
import sys
import re
import configparser
from glob import glob
import subprocess

from img_utils import *
from draw_items import *


class PatxiMenu(QMenu):
    def __init__(self, software_files: str, parent=None):
        super(PatxiMenu, self).__init__(parent)
        self.software_files = software_files
        self.applications = {}
        self.icons = {}
        self.DictOfParse()

    def BuildMenu(self):

        for category, apps in sorted(self.applications.items()):
            cat_menu = QMenu(category.upper())
            cat_menu.setIcon(iconFromBase64(self.icons[category]))
            self.addMenu(cat_menu)

            for name, app in sorted(apps.items()):
                soft_ico = iconFromBase64(app["icon"])
                action = QAction(soft_ico, name)
                action.triggered.connect(self.RunLauncher(app["launch"]))

    def Sections(self):
        glob_pattern = os.path.join(self.software_files, "*")
        software_files = sorted(glob(glob_pattern))
        parser = configparser.ConfigParser()
        parser.read(software_files)

        return parser.sections()

    def DictOfParse(self):
        parser = self.Sections()
        for section_name in parser:
            category = parser.get(section_name, "family")
            family = parser.get(section_name, "family")

            if not self.applications.get(category):
                self.applications[category] = {}

            if not self.icons.get(category):
                self.icons[category] = ""

            if not self.applications[category].get(section_name):
                self.applications[category][section_name] = {}

            for name, value in parser.items(section_name):
                self.applications[category][section_name][name] = value
                if name == "categoryicon" or (
                    name == "icon" and self.icons[category] == ""
                ):
                    self.icons[category] = value

    def RunLauncher(self, launch_cmd):
        subprocess.run([launch_cmd])
