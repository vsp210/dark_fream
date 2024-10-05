import os
import sys

def get_settings(item):
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    try:
        from settings import settings # type: ignore
        return getattr(settings, item)
    except ModuleNotFoundError:
        return []
    except AttributeError:
        # raise f"Not found - '{item}'!"
        pass
