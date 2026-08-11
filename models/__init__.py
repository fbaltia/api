import importlib
import pkgutil
for _, module_name, _ in pkgutil.walk_packages(__path__):
    module = importlib.import_module(f"{__name__}.{module_name}")
    attrs = [attr for attr in dir(module) if not attr.startswith('_')]
    globals().update({attr: getattr(module, attr) for attr in attrs})