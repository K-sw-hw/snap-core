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
    name = "Riconoscimento Gestuale _ Fetahi",
    options = options,
    version = "0.1",
    description = 'Programma realizzato per gestire un robot usando la propria mano',
    executables = executables
)