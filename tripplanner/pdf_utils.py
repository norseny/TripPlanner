from reportlab.graphics.charts.textlabels import Label
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table,\
    TableStyle

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

    def pageNumber(self, canvas, doc):
        number = canvas.getPageNumber()
        canvas.drawCentredString(100*mm, 15*mm, str(number))

    def title_draw(self, x, y, text):
        chart_title = Label()
        chart_title.x = x
        chart_title.y = y
        chart_title.fontSize = 16
        chart_title.textAnchor = 'middle'
        chart_title.setText(text)
        return chart_title

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
            name="TableHeader",
            fontSize=11, alignment=TA_CENTER,
        ))
        styles.add(ParagraphStyle(
            name="ParagraphTitle", fontSize=11, alignment=TA_JUSTIFY,
        ))
        styles.add(ParagraphStyle(
            name="Justify", alignment=TA_JUSTIFY,
        ))

        # list used for elements added into document
        data = []
        data.append(Paragraph(title, styles['Title']))
        # insert a blank space
        data.append(Spacer(1, 12))

        data.append(Paragraph(_('Description') + ': ' + context['trip'].description, styles['Normal']))
        data.append(Spacer(1, 12))
        data.append(Paragraph(_('Created by') + ': ' + str(context['trip'].created_by), styles['Normal']))
        data.append(Spacer(1, 12))
        data.append(Paragraph(_('Price (PLN)') + ': ' + str(context['trip'].price), styles['Normal']))
        data.append(Spacer(1, 12))

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
        table_data.append([Paragraph(_('Journeys'), styles['Italic']),'','','','','','',''])
        for journey in context['trip'].journey_set.all():
            table_data.append(
                [Paragraph(formatTableCellData(journey.name), styles['Normal']),
                 Paragraph(formatTableCellData(journey.start_time), styles['Normal']),
                 Paragraph(formatTableCellData(journey.end_time), styles['Normal']),
                 Paragraph(formatTableCellData(journey.start_point), styles['Normal']),
                 Paragraph(formatTableCellData(journey.end_point), styles['Normal']),
                 Paragraph(formatTableCellData(journey.means_of_transport), styles['Normal']),
                 '',
                 Paragraph(formatTableCellData(journey.price), styles['Normal']),
                 ]
            )
        table_data.append([Paragraph(_('Accommodations'), styles['Italic']),'','','','','','',''])
        for accommodation in context['trip'].accommodation_set.all():
            table_data.append(
                [
                Paragraph(formatTableCellData(accommodation.name), styles['Normal']),
                Paragraph(formatTableCellData(accommodation.start_time), styles['Normal']),
                Paragraph(formatTableCellData(accommodation.end_time), styles['Normal']),
                '',
                '',
                '',
                Paragraph(formatTableCellData(accommodation.address), styles['Normal']),
                Paragraph(formatTableCellData(accommodation.price), styles['Normal']),
                ]
            )
        table_data.append([Paragraph(_('Attractions'), styles['Italic']),'','','','','','',''])
        for attraction in context['trip'].attraction_set.all():
            table_data.append(
                [Paragraph(formatTableCellData(attraction.name), styles['Normal']),
                 Paragraph(formatTableCellData(attraction.start_time), styles['Normal']),
                 Paragraph(formatTableCellData(attraction.end_time), styles['Normal']),
                 '',
                 '',
                 '',
                 '',
                 Paragraph(formatTableCellData(attraction.price), styles['Normal']),
                 ]
            )
        # create table
        wh_table = Table(table_data, colWidths=[doc.width/8.0]*8)
        wh_table.hAlign = 'LEFT'
        wh_table.setStyle(TableStyle(
            [
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.gray)
            ]
        ))
        data.append(wh_table)
        data.append(Spacer(1, 48))

        # # add line chart
        # temperatures, days = get_temperatures(weather_history)
        # line_chart = self.line_chart_draw(temperatures, days)
        # data.append(line_chart)
        # data.append(Spacer(1, 48))
        # data.append(Spacer(1, 48))
        # # add bar chart
        # wind_speed, towns = get_wind_speed(weather_history)
        # days = get_str_days()
        # bar_chart = self.vertical_bar_chart_draw(wind_speed, days, towns)
        # data.append(bar_chart)
        # data.append(Spacer(1, 48))
        # data.append(Spacer(1, 48))
        # # add pie chart
        # prec_percentage = precip_prob_sum(weather_history)
        # llabels = ['0-20 %', '21-40 %', '41-60 %', '61-80 %', '81-100 %']
        # pie_chart = self.pie_chart_draw(prec_percentage, llabels)
        # data.append(pie_chart)

        # create document
        doc.build(data
                  # ,
                  # onFirstPage=self.pageNumber,
                  # onLaterPages=self.pageNumber
                  )
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf


def formatTableCellData(data):
    if data == None:
        return ''
    else:
        return str(data)