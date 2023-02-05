import xlwt
import base64
import pytz
from datetime import *
from io import BytesIO
from odoo.exceptions import UserError
from odoo import models, fields
from odoo.tools.misc import xlwt


class StudentExcelRecord(models.TransientModel):
    _name = 'student.excel.record'
    _description = 'Student Excel Sheet Records'

    data = fields.Binary(string='Data')
    file_name = fields.Char(string='File Name', default='Student Excel Report')

    def print_excel_report(self):
        print('\n\n', 'dpspider....\n' * 5)
        print("////////////////// -------------------------- excel report method called....!!!!")
        active_record_ids = self.env['custom.student'].browse(self._context.get('active_ids'))
        print("-------------------  from wizard selected ids.... -------------", active_record_ids)

        workbook = xlwt.Workbook()
        stylePC = xlwt.XFStyle()
        worksheet = workbook.add_sheet('Student Record')
        bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        stylePC.alignment = alignment
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment_num = xlwt.Alignment()
        alignment_num.horz = xlwt.Alignment.HORZ_RIGHT
        horz_style = xlwt.XFStyle()
        horz_style.alignment = alignment_num
        align_num = xlwt.Alignment()
        align_num.horz = xlwt.Alignment.HORZ_RIGHT
        horz_style_pc = xlwt.XFStyle()
        horz_style_pc.alignment = alignment_num
        style1 = horz_style
        font = xlwt.Font()
        font1 = xlwt.Font()
        borders = xlwt.Borders()
        borders.bottom = xlwt.Borders.THIN
        font.bold = True
        font1.bold = True
        font.height = 500
        stylePC.font = font
        style1.font = font1
        stylePC.alignment = alignment
        pattern = xlwt.Pattern()
        pattern1 = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern1.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
        pattern1.pattern_fore_colour = xlwt.Style.colour_map['gray25']
        stylePC.pattern = pattern
        style1.pattern = pattern
        worksheet.write_merge(0, 1, 2, 6, 'Student Records', style=stylePC)
        worksheet.col(2).width = 5600
        # worksheet.write_merge(3, 3, 0, 2,
        #                       'Non Moving Product in Last Days',
        #                       bold)
        row = 5
        list1 = ['id', 'Name', 'Roll no', 'Qualification']
        worksheet.col(1).width = 5000
        worksheet.write(row, 1, list1[0], style1)
        worksheet.col(2).width = 5000
        worksheet.write(row, 2, list1[1], style1)
        worksheet.col(3).width = 5000
        worksheet.write(row, 3, list1[2], style1)
        worksheet.col(4).width = 5000
        worksheet.write(row, 4, list1[3], style1)
        row = row + 2
        print("active records......", active_record_ids)
        for i in range(len(active_record_ids)):
            worksheet.write(row, 1, active_record_ids[i].id)
            worksheet.write(row, 2, active_record_ids[i].name)
            worksheet.write(row, 3, active_record_ids[i].roll_no)
            worksheet.write(row, 4, active_record_ids[i].qualification)
            row = row + 1
        row = row + 3

        worksheet.write(row, 5, 'Teacher:', bold)
        worksheet.write(row, 6, 'Darpan')
        tz = pytz.timezone('Asia/Kolkata')
        file_data = BytesIO()
        workbook.save(file_data)
        xl_report = self.env['student.excel.record'].create({
            'data': base64.encodebytes(file_data.getvalue()),
            'file_name': 'Student Report - %s' % (datetime.now(tz).strftime('%Y-%m-%d %I:%M:%S')),
        })
        res = {'type': 'ir.actions.act_window',
               'view_mode': 'form',
               'view_type': 'form',
               'res_id': xl_report.id,
               'res_model': 'student.excel.record',
               'view_id': self.env.ref('student_management.student_records_view').id,
               'target': 'new', }

        print('\n\n..............-------------------------.-.-.-.-.-.-. res ----->>> ', res)
        return res
