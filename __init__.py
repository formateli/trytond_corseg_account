# This file is part of tryton-corseg_account module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import configuration
from . import account
from . import liquidacion

def register():
    Pool.register(
        configuration.Configuration,
        configuration.CorsegJournals,
        liquidacion.LiquidacionCia,
        liquidacion.LiquidacionVendedor,
        account.Move,
        account.Line,
        module='corseg_account', type_='model')
