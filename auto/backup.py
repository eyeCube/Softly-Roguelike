import shutil
import datetime
import os

pardir=os.path.pardir
now=datetime.datetime.now()
filename="roguepy_" + now.strftime("%m-%d-%Y_%H-%M")
fromdir=os.path.abspath(os.path.join(
    os.path.dirname(__file__), pardir))
print("from dir", fromdir)
todir=os.path.abspath(os.path.join(
    os.path.dirname(__file__), pardir,pardir, 'roguepy_backups', filename))
print("to dir", todir)
print("copying...")
shutil.copytree(fromdir, todir)
print("done.")
