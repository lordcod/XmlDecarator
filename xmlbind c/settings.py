from typing import Optional, Type
from xmlbind.compiler import XmlCompiler


compilers = {}


def add_compiler(compiler: XmlCompiler):
    compilers[compiler.validate_type] = compiler


def remove_compiler(compiler: XmlCompiler):
    compilers.pop(compiler.validate_type)


def get_compiler(t: Type) -> Optional[XmlCompiler]:
    return compilers.get(t)
