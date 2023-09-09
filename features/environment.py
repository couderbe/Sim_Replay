import os
import sys
from PySide6.QtWidgets import QApplication

def before_all(context):
    context.app = QApplication(sys.argv)

def after_all(context):
    if os.path.exists("build/Test.csv"):
        os.remove("build/Test.csv")
    else:
        print("The file does not exist")