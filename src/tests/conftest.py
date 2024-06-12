import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests/test_project'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')

import django


django.setup()
