import os
import sys


ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tests/test_project"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")

import django


django.setup()
