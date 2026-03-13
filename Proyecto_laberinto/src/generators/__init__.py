# generators/__init__.py
from generators.recursive_backtracker import RecursiveBacktracker
from generators.prim import PrimGenerator
from generators.wilson import WilsonGenerator

GENERATORS = {
    "recursive": RecursiveBacktracker,
    "prim": PrimGenerator,
    "wilson": WilsonGenerator,
}
