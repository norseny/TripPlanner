from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, \
    TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from django.utils.translation import gettext as _
import os
from tripcore import settings


class PdfPrint:
    # initialize class
    def __init__(self, buffer, pageSize):
        self.buffer = buffer
        # default format is A4
        if pageSize == 'A4':
            self.pageSize = A4
            self.pageSize = landscape(self.pageSize)
        elif pageSize == 'Letter':
            self.pageSize = letter
        self.width, self.height = self.pageSize

        # pdfmetrics.registerFont(
        #     TTFont('RobotoCondensed-Regular', 'static/libs/font-roboto/RobotoCondensed-Regular.ttf'))
        # pdfmetrics.registerFont(TTFont('RobotoBold', 'static/libs/font-roboto/Roboto-Bold.ttf'))
        # pdfmetrics.registerFont(
        #     TTFont('RobotoCondensed-BoldItalic', 'static/libs/font-roboto/RobotoCondensed-BoldItalic.ttf'))

        roboto_condensed_regular_path = os.path.join(settings.BASE_DIR, 'tripplanner', 'pdf_utils_additional', 'font-roboto', 'RobotoCondensed-Regular.ttf')
        roboto_bold_path = os.path.join(settings.BASE_DIR, 'tripplanner', 'pdf_utils_additional', 'font-roboto', 'Roboto-Bold.ttf')
        roboto_condensed_bold_italic_path = os.path.join(settings.BASE_DIR, 'tripplanner', 'pdf_utils_additional', 'font-roboto', 'RobotoCondensed-BoldItalic.ttf')

        pdfmetrics.registerFont(
            TTFont('RobotoCondensed-Regular', roboto_condensed_regular_path))
        pdfmetrics.registerFont(TTFont('RobotoBold', roboto_bold_path))
        pdfmetrics.registerFont(
            TTFont('RobotoCondensed-BoldItalic', roboto_condensed_bold_italic_path))


    def report(self, context, title):
        # set some characteristics for pdf document
        doc = SimpleDocTemplate(
            self.buffer,
            rightMargin=10,
            leftMargin=10,
            topMargin=20,
            bottomMargin=20,
            pagesize=self.pageSize,
        )

        # a collection of styles offer by the library
        styles = getSampleStyleSheet()

        # add custom paragraph style
        styles.add(ParagraphStyle(
            name="Title_Roboto", fontName='RobotoBold',
            fontSize=20,
            alignment=TA_CENTER,
        ))
        styles.add(ParagraphStyle(
            name="MainInfo", fontName='RobotoBold',
            fontSize=12
        ))
        styles.add(ParagraphStyle(
            name="TableHeader", fontName='RobotoBold',
            fontSize=11, alignment=TA_CENTER,
        ))
        styles.add(ParagraphStyle(
            name="MyNormal", fontName='RobotoCondensed-Regular',
            fontSize=10, leading=12
        ))
        styles.add(ParagraphStyle(  # todo: align to right
            name="MyNormalDecimal", fontName='RobotoCondensed-Regular',
            fontSize=10, aligment=TA_RIGHT,
        ))
        styles.add(ParagraphStyle(
            name="Categories", fontName='RobotoCondensed-BoldItalic',
            fontSize=11, leading=12
        ))

        # list used for elements added into document
        data = []
        data.append(Paragraph(title, styles['Title_Roboto']))
        # insert a blank space
        data.append(Spacer(1, 24))

        (data.append(Paragraph(_('Description') + ': ' + context['trip'].description, styles['MainInfo']))) if context[
            'trip'].description else ''
        data.append(Spacer(1, 4))
        data.append(Paragraph(_('Created by') + ': ' + str(context['trip'].created_by), styles['MainInfo']))
        data.append(Spacer(1, 4))
        data.append(Paragraph(_('Total Cost') + ': ' + str(context['trip'].price), styles['MainInfo']))
        data.append(Spacer(1, 12))

        table_data = []
        # table header
        table_data.append([
            Paragraph(_('Category/ No.'), styles['TableHeader']),
            Paragraph(_('Name'), styles['TableHeader']),
            Paragraph(_('Start time'), styles['TableHeader']),
            Paragraph(_('End time'), styles['TableHeader']),
            Paragraph(_('Start point'), styles['TableHeader']),
            Paragraph(_('End point'), styles['TableHeader']),
            Paragraph(_('Means of transport'), styles['TableHeader']),
            Paragraph(_('Address'), styles['TableHeader']),
            Paragraph(_('Cost'), styles['TableHeader'])
        ])
        table_data.append([Paragraph(_('Journeys'), styles['Categories']), '', '', '', '', '', '', ''])
        for i, journey in enumerate(context['trip'].journey_set.all()):
            if isinstance(journey.start_time, datetime):
                start_time = (journey.start_time).strftime('%d.%m.%Y (%H:%M)')
            else:
                start_time = ''
            if isinstance(journey.end_time, datetime):
                end_time = (journey.end_time).strftime('%d.%m.%Y (%H:%M)')
            else:
                end_time = ''
            table_data.append(
                [
                    Paragraph(str(i + 1), styles['MyNormal']),
                    '',
                    Paragraph(formatTableCellData(start_time), styles['MyNormal']),
                    Paragraph(formatTableCellData(end_time), styles['MyNormal']),
                    Paragraph(formatTableCellData(journey.start_point), styles['MyNormal']),
                    Paragraph(formatTableCellData(journey.end_point), styles['MyNormal']),
                    Paragraph(formatTableCellData(journey.means_of_transport), styles['MyNormal']),
                    '',
                    Paragraph(formatTableCellData(journey.price), styles['MyNormalDecimal']),
                ]
            )
        table_data.append([Paragraph(_('Accommodations'), styles['Categories']), '', '', '', '', '', '', ''])
        for i, accommodation in enumerate(context['trip'].accommodation_set.all()):
            if isinstance(accommodation.start_time, datetime):
                start_time = (accommodation.start_time).strftime('%d.%m.%Y (%H:%M)')
            else:
                start_time = ''
            if isinstance(accommodation.end_time, datetime):
                end_time = (accommodation.end_time).strftime('%d.%m.%Y (%H:%M)')
            else:
                end_time = ''

            table_data.append(
                [
                    Paragraph(str(i + 1), styles['MyNormal']),
                    Paragraph(formatTableCellData(accommodation.name), styles['MyNormal']),
                    Paragraph(formatTableCellData(start_time),
                              styles['MyNormal']),
                    Paragraph(formatTableCellData(end_time),
                              styles['MyNormal']),
                    '',
                    '',
                    '',
                    Paragraph(formatTableCellData(accommodation.address), styles['MyNormal']),
                    Paragraph(formatTableCellData(accommodation.price), styles['MyNormalDecimal']),
                ]
            )
        table_data.append([Paragraph(_('Attractions'), styles['Categories']), '', '', '', '', '', '', ''])
        for i, attraction in enumerate(context['trip'].attraction_set.all()):
            if isinstance(attraction.start_time, datetime):
                start_time = (attraction.start_time).strftime('%d.%m.%Y (%H:%M)')
            else:
                start_time = ''
            table_data.append(
                [
                Paragraph(str(i + 1), styles['MyNormal']),
                Paragraph(formatTableCellData(attraction.name), styles['MyNormal']),
                 Paragraph(formatTableCellData(start_time),
                           styles['MyNormal']),
                 '',
                 '',
                 '',
                 '',
                 Paragraph(formatTableCellData(attraction.address), styles['MyNormal']),
                 Paragraph(formatTableCellData(attraction.price), styles['MyNormalDecimal']),
                 ]
            )
        # create table
        trip_details_table = Table(table_data, colWidths=[doc.width / 9.0] * 9)
        trip_details_table.setStyle(TableStyle(
            [
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.gray)
            ]
        ))
        data.append(trip_details_table)
        data.append(Spacer(1, 12))

        # data.append(Paragraph((_('More info')), styles['MainInfo']))
        data.append(Spacer(1, 4))
        data.append(Paragraph((_('Journeys') + ':'), styles['Categories']))
        for i, journey in enumerate(context['trip'].journey_set.all()):
            if formatTableCellData(journey.more_info) != '':
                data.append(Paragraph((str(i + 1) + '. ' + formatTableCellData(journey.more_info)), styles['MyNormal']))

        data.append(Paragraph((_('Accommodations') + ':'), styles['Categories']))
        for i, accommodation in enumerate(context['trip'].accommodation_set.all()):
            if formatTableCellData(accommodation.more_info) != '':
                data.append(Paragraph((str(i + 1) + '. ' + formatTableCellData(accommodation.more_info)), styles['MyNormal']))

        data.append(Paragraph((_('Attractions') + ':'), styles['Categories']))
        for i, attraction in enumerate(context['trip'].attraction_set.all()):
            if formatTableCellData(attraction.more_info) != '':
                data.append(Paragraph((str(i + 1) + '. ' + formatTableCellData(attraction.more_info)),
                                      styles['MyNormal']))

        # create document
        doc.build(data)
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf


def formatTableCellData(data):
    if not data:
        return ''
    else:
        if isinstance(data, datetime):
            data.strftime("%Y-%m-%d %H:%M:%S")
        return str(data)
