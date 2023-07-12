import os

def after_all(context):
    if os.path.exists("build/Test.csv"):
        os.remove("build/Test.csv")
    else:
        print("The file does not exist")