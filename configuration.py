# This file is part of tryton-corseg_account module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import ModelSQL, fields
from trytond.modules.company.model import CompanyValueMixin

__all__ = ['Configuration', 'CorsegJournals']


class Configuration:
    __metaclass__ = PoolMeta
    __name__ = 'corseg.configuration'

    journal_comision_cia = fields.MultiValue(fields.Many2One(
            'account.journal', 'Journal Comision Cia', required=True,
            domain=[('type', '=', 'revenue')]
        ))
    journal_comision_vendedor = fields.MultiValue(fields.Many2One(
            'account.journal', 'Journal Comision Vendedor', required=True,
            domain=[('type', '=', 'expense')]
        ))

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field in {'journal_comision_cia', 'journal_comision_vendedor'}:
            return pool.get('corseg.configuration.journals')
        return super(Configuration, cls).multivalue_model(field)


class CorsegJournals(ModelSQL, CompanyValueMixin):
    "Corseg Journals"
    __name__ = 'corseg.configuration.journals'
    journal_comision_cia = fields.Many2One(
            'account.journal', 'Journal Comision Cia',
            domain=[('type', '=', 'revenue')]
        )
    journal_comision_vendedor = fields.Many2One(
            'account.journal', 'Journal Comision Vendedor',
            domain=[('type', '=', 'expense')]
        )
