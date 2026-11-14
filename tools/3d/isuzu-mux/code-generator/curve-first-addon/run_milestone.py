# Curves first. Earlier V02 code is archived separately.
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('run_curve.py')),run_name='__main__')
