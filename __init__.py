# This file is part of tryton-corseg_account module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from .configuration import *
from .account import *

def register():
    Pool.register(
        Configuration,
        CorsegJournals,
        Move,
        module='corseg_account', type_='model')
