# This file is part of tryton-corseg_account module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from .configuration import *
from .account import *
from .liquidacion import *

def register():
    Pool.register(
        Configuration,
        CorsegJournals,
        LiquidacionCia,
        LiquidacionVendedor,
        Move,
        module='corseg_account', type_='model')
