# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import PoolMeta
from trytond.model import fields

__all__ = [
        'LiquidacionCia',
        'LiquidacionVendedor',
    ]

    
class LiquidacionCia:
    __metaclass__ = PoolMeta
    __name__ = 'corseg.liquidacion.cia'

    move = fields.Many2One('account.move', 'Move', readonly=True,
        domain=[
                ('company', '=', Eval('company', -1)),
            ],
        depends=['company'])

    @classmethod
    def __setup__(cls):
        super(LiquidacionCia, cls).__setup__()
        cls.state.selection += [
                ('posted', 'Posteado'),
            ]

    def set_acc_move(self):
        'Return Move for Liquidacion'
        pool = Pool()
        Move = pool.get('account.move')
        Period = pool.get('account.period')
        Journal = pool.get('account.journal')
        period_id = Period.find(self.company.id, date=self.fecha)

        config = pool.get('corseg.configuration')(1)
        journal = config.journal_comision_cia

        move = Move(
            period=period_id,
            journal=journal,
            date=self.fecha,
            origin=self,
            company=self.company,
            description=self.referencia,
        )

        lines=[]
        lines.append(
            self._get_move_line('debit', journal, period))
        lines.append(
            self._get_move_line('credit', journal, period))

        move.lines = lines
        move.save()

    def _get_move_line(self, type_, journal period):
        pool = Pool()
        MoveLine = pool.get('account.move.line')
        Currency = pool.get('currency.currency')
        debit = Decimal('0.0')
        credit = Decimal('0.0')

        with Transaction().set_context(date=self.fecha):
            amount = Currency.compute(self.currency,
                self.total, self.company.currency)
        if self.currency != self.company.currency:
            second_currency = self.currency
            amount_second_currency = self.total
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
            debit=debit,
            credit=credit,
            account=account,
            second_currency=second_currency,
            amount_second_currency=amount_second_currency,
            description=self.referencia,
        )

    @classmethod
    @ModelView.button
    @Workflow.transition('confirmado')
    def confirmar(cls, liqs):
        super(LiquidacionCia, cls).confirmar(liqs)
        for liq in liqs:
            liq.set_acc_move()
            

class LiquidacionVendedor:
    __metaclass__ = PoolMeta
    __name__ = 'corseg.liquidacion.vendedor'

    move = fields.Many2One('account.move', 'Move', readonly=True,
        domain=[
                ('company', '=', Eval('company', -1)),
            ],
        depends=['company'])

    @classmethod
    def __setup__(cls):
        super(LiquidacionCia, cls).__setup__()
        cls.state.selection += [
                ('posted', 'Posteado'),
            ]
