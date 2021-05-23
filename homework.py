import datetime as dt
from typing import Optional


class Calculator:
    """Базовый класс для создания калькулятора,
    принимает переменную - дневной лимит.
    """

    def __init__(self, limit):

        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Метод для добавления записей."""
        self.records.append(record)

    def get_today_stats(self):
        """Метод для подсчета статистики за сегодня."""
        today_stats = 0
        today_date = dt.datetime.now().date()

        for record in self.records:
            date = record.date

            if date == today_date:
                today_stats += record.amount

        return today_stats

    def get_week_stats(self):
        """Метод для подсчета статистики за последнюю неделю."""
        week_stats = 0
        today_date = dt.datetime.now().date()

        last_week_date = today_date - dt.timedelta(days=7)

        for record in self.records:
            date = record.date

            if date > last_week_date and date <= today_date:
                week_stats += record.amount

        return week_stats


class Record:
    """Класс для создания записей."""

    def __init__(self, amount, comment, date: Optional[str] = None):

        self.amount = amount

        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()

        self.comment = comment


class CaloriesCalculator(Calculator):
    """Класс для создания калькулятора калорий."""

    def get_calories_remained(self):
        """Метод для расчета оставшихся для сегодня доступных калорий."""
        calories_remained = self.limit - self.get_today_stats()

        if calories_remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {calories_remained} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """Класс для создания калькулятора денег."""

    USD_RATE = 70.21
    EURO_RATE = 90.34

    def get_today_cash_remained(self, currency):
        """Метод для расчета оставшихся для сегодня доступных денег."""

        today_cash_remained = self.limit - self.get_today_stats()

        if currency == 'rub':
            currency_description = 'руб'
            today_cash_remained_conv = round(abs(today_cash_remained), 2)

        elif currency == 'usd':
            currency_description = 'USD'
            today_cash_remained_conv = round(abs(today_cash_remained)
                                             / self.USD_RATE, 2)

        elif currency == 'eur':
            currency_description = 'Euro'
            today_cash_remained_conv = round(abs(today_cash_remained)
                                             / self.EURO_RATE, 2)

        if today_cash_remained > 0:
            return ('На сегодня осталось '
                    f'{today_cash_remained_conv:.2f} {currency_description}')
        elif today_cash_remained == 0:
            return 'Денег нет, держись'
        else:
            return ('Денег нет, держись: твой долг - '
                    f'{today_cash_remained_conv:.2f} {currency_description}')
