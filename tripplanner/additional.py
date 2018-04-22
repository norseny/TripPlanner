""" For some additional functions """

from time import strftime

# sd, ed : 2018-04-28 01:00:00
# dr 07/04/2018 (12:00) - 19/05/2018 (11:59)


def format_to_daterange(start_date, end_date):
    n_start_date = start_date.strftime('%d/%m/%Y (%H:%M)')
    n_end_date = end_date.strftime('%d/%m/%Y (%H:%M)')
    return (n_start_date + ' - ' + n_end_date)
