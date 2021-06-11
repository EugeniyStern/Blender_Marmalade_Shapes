import shutil
import os.path
from fileinput import close
import subprocess

#debug_file = "install_package.py"

debug_file = "lesson_mathutils_vectors.py"
debug_file = "klumba_walls.py"
# debug_file ="tower.py"
debug_file = "shining_object.py"



blender_exe = "c:\\eclipse\\blender2.80_alfa\\blender.exe"
blender_exe = "c:\\eclipse\\blender292\\blender.exe"
argument = " -v -P \"%s\""

shutil.copy("C:\\ws3_ox\\Blender_Marmalade_Shapes\\" + debug_file, "C:\\ws3_ox\\Blender_Marmalade_Shapes\\__copied.py")

abs_copied = os.path.abspath("C:\\ws3_ox\\Blender_Marmalade_Shapes\\__copied.py")

subprocess.run([blender_exe, "-P", abs_copied])
