from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from tripplanner.models import Accommodation
from django.utils.timezone import make_aware
from datetime import datetime


# def daterange_validator(value):
#     """Validate daterange input"""
#     if 'do' in value:
#         start_date, end_date = value.split(' do ', 2)
#     elif 'to' in value:
#         start_date, end_date = value.split(' to ', 2)
    #todo: finish validation

    # if 1 != 1:
    #     raise ValidationError(
    #         _('%(value)s is not an even number'),
    #         params={'value': value},
    #     )


# def start_end_date_from_daterange(cleaned_data_el):
#     if 'do' in cleaned_data_el['date_range']:
#         start_date, end_date = cleaned_data_el['date_range'].split(' do ', 2)
#     elif 'to' in cleaned_data_el['date_range']:
#         start_date, end_date = cleaned_data_el['date_range'].split(' to ', 2)
#
#     cleaned_data_el['start_time'] = make_aware(datetime.strptime(start_date, '%d/%m/%y'))
#     cleaned_data_el['end_time'] = make_aware(datetime.strptime(end_date, '%d/%m/%y'))

# def update_acc_dates(trip_id, cleaned_data):
#     for el in cleaned_data:
#         if el:
#             if el['date_range']:
#                 if Accommodation.objects.filter(trip_id=trip_id, price = el['price'], name=el['name']).count() == 1:
#                     acc_to_modify = Accommodation.objects.filter(trip_id=trip_id, price = el['price'], name=el['name']).first()
#                     Accommodation.start_end_date_from_daterange(acc_to_modify, el)
#                     if 'do' in el['date_range']:
#                         start_date, end_date = el['date_range'].split(' do ', 2)
#                     elif 'to' in el['date_range']:
#                         start_date, end_date = el['date_range'].split(' to ', 2)
#
#                     el['start_time'] = make_aware(datetime.strptime(start_date, '%d/%m/%y'))
#                     el['end_time'] = make_aware(datetime.strptime(end_date, '%d/%m/%y'))

                    # start_end_date_from_daterange(el)
