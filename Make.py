import cx_Freeze
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"
executables = [cx_Freeze.Executable("Game.pyw",icon="Burger.ico",base = base)]
cx_Freeze.setup(
    name = "Where's my burger",
    version = "1.0",
    options = {"build_exe" : {"packages": ["pygame"],"include_files":["libvorbis.dll","libvorbisfile.dll","libogg.dll","norwester.otf","GameObjects.py", "Power.py", "Wall.py", "Player.py","clean.txt", "Both.txt", "Enemy.py","Sound/", "Graphics/"]}},
    executables = executables



    )
