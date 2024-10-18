from cx_Freeze import setup, Executable

base = None    

executables = [Executable("main.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Riconoscimento Gestuale _ Fetahi v0.2",
    options = options,
    version = "0.2",
    description = 'Programma realizzato per gestire un robot usando la propria mano',
    executables = executables
)