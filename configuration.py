# This file is part of tryton-corseg_account module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import ModelSQL, fields
from trytond.pyson import Eval
from trytond.modules.company.model import CompanyValueMixin

__all__ = [
        'Configuration',
        'CorsegJournals',
        'CorsegAccounts'
    ]


class Configuration(metaclass=PoolMeta):
    __name__ = 'corseg.configuration'

    journal_comision_cia = fields.MultiValue(fields.Many2One(
            'account.journal', 'Journal Comision Cia', required=True,
            domain=[('type', '=', 'revenue')]
        ))
    journal_comision_vendedor = fields.MultiValue(fields.Many2One(
            'account.journal', 'Journal Comision Vendedor', required=True,
            domain=[('type', '=', 'expense')]
        ))
    debit_account_comision_cia = fields.MultiValue(fields.Many2One('account.account',
        'Debit Account Comision Cia', required=True,
        domain=[
            ('company', '=', Eval('context', {}).get('company', -1)),
        ]))
    credit_account_comision_cia = fields.MultiValue(fields.Many2One('account.account',
        'Credit Account Comision Cia', required=True,
        domain=[
            ('company', '=', Eval('context', {}).get('company', -1)),
        ]))
    debit_account_comision_vendedor = fields.MultiValue(fields.Many2One('account.account',
        'Debit Account Comision Vendedor', required=True,
        domain=[
            ('company', '=', Eval('context', {}).get('company', -1)),
        ]))
    credit_account_comision_vendedor = fields.MultiValue(fields.Many2One('account.account',
        'Credit Account Comision Vendedor', required=True,
        domain=[
            ('company', '=', Eval('context', {}).get('company', -1)),
        ]))

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()

        if field in {'journal_comision_cia', 'journal_comision_vendedor'}:
            return pool.get('corseg.configuration.journals')

        accounts=[
            'debit_account_comision_cia',
            'credit_account_comision_cia',
            'debit_account_comision_vendedor',
            'credit_account_comision_vendedor',
        ]
        if field in accounts:
            return pool.get('corseg.configuration.accounts')

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


class CorsegAccounts(ModelSQL, CompanyValueMixin):
    "Corseg Accounts"
    __name__ = 'corseg.configuration.accounts'

    debit_account_comision_cia = fields.Many2One('account.account',
        'Debit Account Comision Cia',
        domain=[
            ('company', '=', Eval('context', {}).get('company', -1)),
        ])
    credit_account_comision_cia = fields.Many2One('account.account',
        'Credit Account Comision Cia',
        domain=[
            ('company', '=', Eval('context', {}).get('company', -1)),
        ])
    debit_account_comision_vendedor = fields.Many2One('account.account',
        'Debit Account Comision Vendedor',
        domain=[
            ('company', '=', Eval('context', {}).get('company', -1)),
        ])
    credit_account_comision_vendedor = fields.Many2One('account.account',
        'Credit Account Comision Vendedor',
        domain=[
            ('company', '=', Eval('context', {}).get('company', -1)),
        ])
