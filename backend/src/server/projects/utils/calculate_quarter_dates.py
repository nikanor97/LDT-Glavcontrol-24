from datetime import datetime, timedelta


def calculate_quarter_dates(year: int, quarter: int):
    if quarter not in [1, 2, 3, 4]:
        raise ValueError("Quarter must be between 1 and 4")

    # Определяем начальные и конечные месяцы каждого квартала
    quarters = {
        1: (1, 3),  # Январь - Март
        2: (4, 6),  # Апрель - Июнь
        3: (7, 9),  # Июль - Сентябрь
        4: (10, 12)  # Октябрь - Декабрь
    }

    start_month, end_month = quarters[quarter]

    # Начальная дата - первый день стартового месяца
    start_date = datetime(year, start_month, 1)

    # Конечная дата - последний день конечного месяца
    if end_month == 12:
        end_date = datetime(year, end_month, 31)
    else:
        end_date = datetime(year, end_month + 1, 1) - timedelta(days=1)

    return start_date, end_date
