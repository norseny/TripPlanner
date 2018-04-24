""" For some additional functions """

from django.utils import timezone
from datetime import datetime
from time import strftime, strptime
from  tripplanner import models


# sd, ed : 2018-04-28 01:00:00
# dr 07/04/2018 (12:00) - 19/05/2018 (11:59)
#'24/04/2018 (12:00) - 24/04/2018 (11:59)'

def format_to_daterange(start_date, end_date):
    n_start_date = start_date.strftime('%d/%m/%Y (%H:%M)')
    n_end_date = end_date.strftime('%d/%m/%Y (%H:%M)')
    return n_start_date + ' - ' + n_end_date


def check_daterange(datetime_range):
    ''' If default daterange not changed, set it to None'''
    now = timezone.now().replace(hour=12, minute=00, second=00)
    now2 = timezone.now().replace(hour=11, minute=59, second=00)
    now = now.strftime('%d%m%Y%H%M')
    now2 = now2.strftime('%d%m%Y%H%M')

    datetime_range = datetime_range.replace(' ','') #todo: optimize
    datetime_range = datetime_range.replace(')','')
    datetime_range = datetime_range.replace('(','')
    datetime_range = datetime_range.replace('/','')
    datetime_range = datetime_range.replace(':','')

    d1, d2 = datetime_range.split('-')
    datetime1 = datetime.strptime(d1, '%d%m%Y%H%M')
    datetime2 = datetime.strptime(d1, '%d%m%Y%H%M')

    b = (datetime1, datetime2)

    if (d1 == now) and ((d2 == now2) or (d2 == now)):

        return None
    else:
        return b


# def handle_journey_daterange(journey_id, el):
#     result = []
#     if el['datetime_range'] != None:
#         journey = models.Journey.objects.get(pk=journey_id)
#
#         journey.start_time = el['datetime_range'][0]
#         journey.end_time = el['datetime_range'][1]
#         journey.save()
#
#         result.append(el['datetime_range'][0])
#         result.append(el['datetime_range'][1])
#
#     return result
