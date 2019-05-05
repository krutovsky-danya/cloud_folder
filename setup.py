from cx_Freeze import setup, Executable

executables = [Executable('Project.py',
                          targetName = 'DarlingCloud.exe',
                          base = 'Win32GUI',
                          icon = 'icon1.ico')]

include_files = ['Data', 'Icons', 'Sounds']

options = {
    'build_exe': {
        'include_msvcr' : True,
        'include_files' : include_files
        }
    }

setup(name = 'DarlingCloud',
      executables = executables,
      options = options)
