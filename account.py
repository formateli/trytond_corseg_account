# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields

__all__ = ['Move', 'Line']


class Move:
    __metaclass__ = PoolMeta
    __name__ = 'account.move'

    @classmethod
    def _get_origin(cls):
        corseg = ['corseg.liquidacion.cia', 'corseg.liquidacion.vendedor']
        return super(Move, cls)._get_origin() + corseg


class Line:
    __metaclass__ = PoolMeta
    __name__ = 'account.move.line'

    liq_cia = fields.Many2One('corseg.liquidacion.cia',
        'Liq Cia', readonly=True)
    liq_vendedor = fields.Many2One('corseg.liquidacion.vendedor',
        'Liq Vendedor', readonly=True)
