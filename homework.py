import datetime as dt


class Record:
    """Here we create records."""
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    """Here we count records."""
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        cnt = 0
        for x in self.records:
            if x.date == dt.datetime.now().date():
                cnt += x.amount
        return cnt

    def today_stats(self):
        return self.limit - self.get_today_stats()

    def get_week_stats(self):
        week_cnt = 0
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        for x in self.records:
            if week_ago <= x.date <= today:
                week_cnt += x.amount
        return week_cnt


class CashCalculator(Calculator):
    """Here we counts money in 3 currencies."""
    USD_RATE = 60.5
    EURO_RATE = 70.1
    RUB_RATE = 1

    def __init__(self, limit):
        super().__init__(limit)
    """Here we count the rest of  money."""
    def get_today_cash_remained(self, currency):
        currencies = {
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE),
            'rub': ('руб', self.RUB_RATE)
        }

        currency_name = currencies[currency][0]
        currency_rate = currencies[currency][1]
        remained_cash = self.limit - self.get_today_stats()
        remained_cash_in_currency = round(remained_cash / currency_rate, 2)

        if remained_cash_in_currency > 0:
            return (f'На сегодня осталось {remained_cash_in_currency}'
                    f' {currency_name}')
        elif remained_cash == 0:
            return 'Денег нет, держись'
        else:
            return (f'Денег нет, держись: твой долг -'
                    f' {abs(remained_cash_in_currency)} {currency_name}')


class CaloriesCalculator(Calculator):
    """Here we calculate calories."""
    def get_calories_remained(self):
        stats = super().today_stats()
        if stats > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с'
                    f' общей калорийностью не более {stats} кКал')
        return 'Хватит есть!'
