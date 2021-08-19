import datetime as dt


class Record:
    """Here we create records."""
    FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, self.FORMAT).date()


class Calculator:
    """Here we count records."""
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        return sum(record.amount for record in self.records
                   if record.date == dt.date.today())

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                   if week_ago < record.date <= today)


class CashCalculator(Calculator):
    """Here we counts money in 3 currencies."""
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1

    CURRENCIES = {
        'usd': ('USD', USD_RATE),
        'eur': ('Euro', EURO_RATE),
        'rub': ('руб', RUB_RATE)
    }
    ANSWER_ONE = ('На сегодня осталось {key_insert} {key_name}')
    ANSWER_TWO = ('Денег нет, держись: твой долг - {key_insert} {key_name}')
    ANSWER_THREE = 'Денег нет, держись'
    """Here we count the rest of  money."""
    def get_today_cash_remained(self, currency):
        name, rate = self.CURRENCIES[currency]
        remained_cash = self.limit - self.get_today_stats()
        remained_cash_in_currency = round(remained_cash / rate, 2)

        if remained_cash_in_currency > 0:
            return self.ANSWER_ONE.format(key_insert=remained_cash_in_currency,
                                          key_name=name)
        elif remained_cash_in_currency < 0:
            return self.ANSWER_TWO.format(
                key_insert=abs(remained_cash_in_currency), key_name=name)
        elif currency not in self.CURRENCIES:
            return 'Error'
        else:
            return self.ANSWER_THREE


class CaloriesCalculator(Calculator):

    ANSWER_ONE = ('Сегодня можно съесть что-нибудь ещё, но с'
                  ' общей калорийностью не более {key_to_insert} кКал')
    ANSWER_TWO = 'Хватит есть!'
    """Here we calculate calories."""
    def get_calories_remained(self):
        stats = self.limit - self.get_today_stats()
        if stats > 0:
            return self.ANSWER_ONE.format(key_to_insert=stats)
        return self.ANSWER_TWO
