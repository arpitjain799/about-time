# coding=utf-8
VERSION = (2, 0, 5)

__author__ = 'Rogério Sampaio de Almeida'
__email__ = 'rsalmei@gmail.com'
__version__ = '.'.join(map(str, VERSION))

__all__ = ('__author__', '__version__', 'about_time')

from .core import about_time
