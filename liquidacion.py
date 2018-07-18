# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta
from trytond.model import Workflow, ModelView, fields
from trytond.pyson import Eval
from decimal import Decimal
from trytond.modules.corseg.tools import auditoria_field, set_auditoria

__all__ = [
        'LiquidacionCia',
        'LiquidacionVendedor',
    ]


def _set_acc_move(liq, type_):
    'Return Move for Liquidacion'
    pool = Pool()
    Move = pool.get('account.move')
    Period = pool.get('account.period')
    Journal = pool.get('account.journal')
    period_id = Period.find(liq.company.id, date=liq.fecha)

    config = pool.get('corseg.configuration')(1)
    journal = getattr(config, 'journal_comision_' + type_)

    move = Move(
        period=period_id,
        journal=journal,
        date=liq.fecha,
        origin=liq,
        company=liq.company,
        description=liq.referencia,
    )

    lines=[]
    if type_ == 'cia':
        lines.append(
            _get_move_line(liq, 'debit', journal, period_id, liq.cia.party))
        lines.append(
            _get_move_line(liq, 'credit', journal, period_id, None))
    else:
        lines.append(
            _get_move_line(liq, 'debit', journal, period_id, None))
        lines.append(
            _get_move_line(liq, 'credit', journal, period_id, liq.vendedor.party))

    move.lines = lines
    move.save()
    return move


def _get_move_line(liq, type_, journal, period, party):
    pool = Pool()
    MoveLine = pool.get('account.move.line')
    Currency = pool.get('currency.currency')
    debit = Decimal('0.0')
    credit = Decimal('0.0')

    with Transaction().set_context(date=liq.fecha):
        amount = Currency.compute(liq.currency,
            liq.total, liq.company.currency)
    if liq.currency != liq.company.currency:
        second_currency = liq.currency
        amount_second_currency = liq.total
    else:
        amount_second_currency = None
        second_currency = None

    if type_ == 'debit':
        account = journal.debit_account
        debit = amount
    else:
        account = journal.credit_account
        credit = amount

    return MoveLine(
        journal=journal,
        period=period,
        party=party,
        debit=debit,
        credit=credit,
        account=account,
        second_currency=second_currency,
        amount_second_currency=amount_second_currency,
        description=liq.referencia,
    )


class LiquidacionCia:
    __metaclass__ = PoolMeta
    __name__ = 'corseg.liquidacion.cia'

    move = fields.Many2One('account.move', 'Move',
        readonly=True, ondelete='RESTRICT',
        domain=[
                ('company', '=', Eval('company', -1)),
            ],
        depends=['company'])

    @classmethod
    @ModelView.button
    @Workflow.transition('confirmado')
    def confirmar(cls, liqs):
        super(LiquidacionCia, cls).confirmar(liqs)
        for liq in liqs:
            move = _set_acc_move(liq, 'cia')
            liq.move = move
            liq.save()


class LiquidacionVendedor:
    __metaclass__ = PoolMeta
    __name__ = 'corseg.liquidacion.vendedor'

    move = fields.Many2One('account.move', 'Move',
        readonly=True, ondelete='RESTRICT',
        domain=[
                ('company', '=', Eval('company', -1)),
            ],
        depends=['company'])

    @classmethod
    @ModelView.button
    @Workflow.transition('confirmado')
    def confirmar(cls, liqs):
        super(LiquidacionVendedor, cls).confirmar(liqs)
        for liq in liqs:
            move = _set_acc_move(liq, 'vendedor')
            liq.move = move
            liq.save()
