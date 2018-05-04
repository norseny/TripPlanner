from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table,\
    TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from django.utils.translation import gettext as _


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
        a =9

        pdfmetrics.registerFont(TTFont('RobotoCondensed-Regular', 'static/libs/font-roboto/RobotoCondensed-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('RobotoBold', 'static/libs/font-roboto/Roboto-Bold.ttf'))
        pdfmetrics.registerFont(TTFont('RobotoCondensed-BoldItalic', 'static/libs/font-roboto/RobotoCondensed-BoldItalic.ttf'))

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
            name="MainInfo",fontName='RobotoBold',
            fontSize=12
        ))
        styles.add(ParagraphStyle(
            name="TableHeader",fontName='RobotoBold',
            fontSize=11, alignment=TA_CENTER,
        ))
        styles.add(ParagraphStyle(
            name="MyNormal",fontName='RobotoCondensed-Regular',
            fontSize=10,leading=12
        ))
        styles.add(ParagraphStyle( #todo: align to right
            name="MyNormalDecimal",fontName='RobotoCondensed-Regular',
            fontSize=10, aligment=TA_RIGHT,
        ))
        styles.add(ParagraphStyle(
            name="Categories",fontName='RobotoCondensed-BoldItalic',
            fontSize=11,leading=12
        ))

        # list used for elements added into document
        data = []
        data.append(Spacer(1, 12))
        data.append(Paragraph(title, styles['Title']))
        # insert a blank space
        data.append(Spacer(1, 24))

        data.append(Paragraph(_('Description') + ': ' + context['trip'].description, styles['MainInfo']))
        data.append(Spacer(1, 12))
        data.append(Paragraph(_('Created by') + ': ' + str(context['trip'].created_by), styles['MainInfo']))
        data.append(Spacer(1, 12))
        data.append(Paragraph(_('Total Cost (PLN)') + ': ' + str(context['trip'].price), styles['MainInfo']))
        data.append(Spacer(1, 24))

        table_data = []
        # table header
        table_data.append([
            Paragraph(_('Name'), styles['TableHeader']),
            Paragraph(_('Start time'), styles['TableHeader']),
            Paragraph(_('End time'), styles['TableHeader']),
            Paragraph(_('Start point'), styles['TableHeader']),
            Paragraph(_('End point'), styles['TableHeader']),
            Paragraph(_('Means of transport'), styles['TableHeader']),
            Paragraph(_('Address'), styles['TableHeader']),
            Paragraph(_('Price (PLN)'), styles['TableHeader'])
        ])
        table_data.append([Paragraph(_('Journeys'), styles['Categories']),'','','','','','',''])
        for journey in context['trip'].journey_set.all():
            table_data.append(
                [Paragraph(formatTableCellData(journey.name), styles['MyNormal']),
                 Paragraph(formatTableCellData(journey.start_time), styles['MyNormal']),
                 Paragraph(formatTableCellData(journey.end_time), styles['MyNormal']),
                 Paragraph(formatTableCellData(journey.start_point), styles['MyNormal']),
                 Paragraph(formatTableCellData(journey.end_point), styles['MyNormal']),
                 Paragraph(formatTableCellData(journey.means_of_transport), styles['MyNormal']),
                 '',
                 Paragraph(formatTableCellData(journey.price), styles['MyNormalDecimal']),
                 ]
            )
        table_data.append([Paragraph(_('Accommodations'), styles['Categories']),'','','','','','',''])
        for accommodation in context['trip'].accommodation_set.all():
            table_data.append(
                [
                Paragraph(formatTableCellData(accommodation.name), styles['MyNormal']),
                Paragraph(formatTableCellData(accommodation.start_time), styles['MyNormal']),
                Paragraph(formatTableCellData(accommodation.end_time), styles['MyNormal']),
                '',
                '',
                '',
                Paragraph(formatTableCellData(accommodation.address), styles['MyNormal']),
                Paragraph(formatTableCellData(accommodation.price), styles['MyNormalDecimal']),
                ]
            )
        table_data.append([Paragraph(_('Attractions'), styles['Categories']),'','','','','','',''])
        for attraction in context['trip'].attraction_set.all():
            table_data.append(
                [Paragraph(formatTableCellData(attraction.name), styles['MyNormal']),
                 Paragraph(formatTableCellData(attraction.start_time), styles['MyNormal']),
                 '',
                 '',
                 '',
                 '',
                 Paragraph(formatTableCellData(attraction.address), styles['MyNormal']),
                 Paragraph(formatTableCellData(attraction.price), styles['MyNormalDecimal']),
                 ]
            )
        # create table
        trip_details_table = Table(table_data, colWidths=[doc.width/8.0]*8)
        trip_details_table.setStyle(TableStyle(
            [
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.gray)
            ]
        ))
        data.append(trip_details_table)
        data.append(Spacer(1, 48))

        # create document
        doc.build(data)
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf


def formatTableCellData(data):
    if data == None:
        return ''
    else:
        if isinstance(data, datetime):
            data.strftime("%Y-%m-%d %H:%M:%S")
        return str(data)