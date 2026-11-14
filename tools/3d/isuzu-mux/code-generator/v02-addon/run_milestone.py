# Current runner delegates to V02; never overwrite V01.
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('run_v02.py')),run_name='__main__')
