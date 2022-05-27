import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Конструкцию нужно оптимизировать.
        # Так же можно использовать dt.date.today()
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Запись можно сократить с помощью list comprehension
        # https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Конструкция не по PEP8, нужно улучшить
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарий не нужен, лучше описать все в docstring
    # https://peps.python.org/pep-0257/
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Скобки не нужны
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Комментарии не нужны, лучше описать все в docstring
    # https://peps.python.org/pep-0257/
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Не нужно передавать курсы в качестве аргументов, т.к. они описаны выше.
    # К ним можно обратиться через self.
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Если у нас будет много валют, например, 100,
        # То для каждой писать отдельное условие - такое себе удовольствие
        # Лучше поместить данные о курсах валют в словарь
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Неверное выражение, необходимо поправить.
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            #f-строки позволяют настроить формат вывода данных,
            # например, количество знаков после запятой.
            # Лучше воспользоваться этой стандартной функциональностью,
            # чем round. Посмотри, как это делается в документации
            # str.format (у format и f-строк общий синтаксис настройки вывода).
            # Скобки тоже не обязательны.
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # тут можно просто else:
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
    # Этот метод тут не нужен, т.к. мы его унаследовали у базового класса Calculator
    # https://docs-python.ru/tutorial/vstroennye-funktsii-interpretatora-python/funktsija-super/
    def get_week_stats(self):
        super().get_week_stats()
