import datetime as dt


class Record:

    FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, self.FORMAT).date()


class Calculator:

    WEEK_DELTA = dt.timedelta(days=7)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - self.WEEK_DELTA
        return sum(record.amount for record in self.records
                   if week_ago < record.date <= today)


class CashCalculator(Calculator):

    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1

    CURRENCIES = {
        'usd': ('USD', USD_RATE),
        'eur': ('Euro', EURO_RATE),
        'rub': ('руб', RUB_RATE)
    }
    MONEY_LEFT = ('На сегодня осталось {balance} {currency_name}')
    OWES_MONEY = ('Денег нет, держись: твой долг - {amount_debt} '
                  '{currency_name}')
    NO_MONEY_LEFT = 'Денег нет, держись'
    INCORRECT_CURRENCY_ENTERED = ('Введена некорректная валюта. Программа'
                                  ' принимает только валюты:{currency}')

    def get_today_cash_remained(self, currency):
        try:
            name, rate = self.CURRENCIES[currency]
        except KeyError:
            raise ValueError(self.INCORRECT_CURRENCY_ENTERED.format(
                             currency=self.CURRENCIES.keys()))
        remained_cash = self.limit - self.get_today_stats()
        if remained_cash == 0:
            return self.NO_MONEY_LEFT
        remained_cash_in_currency = round(remained_cash / rate, 2)
        if remained_cash_in_currency > 0:
            return self.MONEY_LEFT.format(balance=remained_cash_in_currency,
                                          currency_name=name)
        return self.OWES_MONEY.format(
            amount_debt=abs(remained_cash_in_currency), currency_name=name)


class CaloriesCalculator(Calculator):

    CAN_EAT = ('Сегодня можно съесть что-нибудь ещё, но с'
               ' общей калорийностью не более {sum} кКал')
    CANT_EAT = 'Хватит есть!'

    def get_calories_remained(self):
        stats = self.limit - self.get_today_stats()
        if stats > 0:
            return self.CAN_EAT.format(sum=stats)
        return self.CANT_EAT
