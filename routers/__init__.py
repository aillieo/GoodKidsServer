import glob
from os.path import basename, dirname, join, splitext
from fastapi import APIRouter
from importlib import import_module

router = APIRouter()

dir_path = dirname(__file__)
router_files = glob.glob(join(dir_path, "*.py"))
router_files = [f for f in router_files if not f.endswith('__init__.py')]

modules_and_prefixes = [(splitext(basename(f))[0], splitext(
    basename(f))[0].replace('_', '')) for f in router_files]

for module_name, prefix in modules_and_prefixes:
    module = import_module(f".{module_name}", package=__name__)
    router.include_router(module.router, prefix=f"/{prefix}")
