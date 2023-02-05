import xlwt
import base64
import pytz
from datetime import *
from io import BytesIO
from odoo.exceptions import UserError
from odoo import models, fields,api

from odoo.tools.misc import xlwt


class StudentRecords(models.TransientModel):
    _name = 'student.records'
    _description = 'Student Records'

    report_type = fields.Selection([('pdf', 'PDF'), ('xls', 'Excel')], string='Report Type', default='pdf')
    data = fields.Binary(string='Data')
    file_name = fields.Char(string='File Name', default='Student Excel Report')

    def print_records(self):
        print("action called......\n" * 5)
        active_record_ids = self.env['custom.student'].browse(self._context.get('active_ids')).ids
        print("-------------------  from wizard selected ids.... -------------", active_record_ids)
        print("-------------------  from wizard selected ids type.... -------------", type(active_record_ids))
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {'record_ids': active_record_ids},
            'res_model': 'student.records',
            'view_id': self.env.ref('student_management.student_records_print').id,
            'target': 'new',
        }
    @api.depends('report_type')
    def print_report(self):
        print("method called.....\n" * 5)
        active_record_ids = self.env.context.get('record_ids')
        print("-------------------  from wizard selected ids.... -------------", active_record_ids)
        print("-------------------  from wizard selected ids type.... -------------", type(active_record_ids))
        search_records = self.env['custom.student'].browse(active_record_ids)
        print("---------------- froom wizard..... search ids ", search_records)
        print("---------------- froom wizard..... search ids ", type(search_records))
        mail_template_id = self.env.ref('student_management.mail_student_record')
        if self.report_type == 'pdf':
            print("report pdf.....\n" * 5)
            template_id = self.env.ref('student_management.student_record_report11')
            pdf = template_id._render_qweb_pdf(search_records.ids)
            print("\n\n\n pdf--->", pdf)
            print("\n\n\n pdf[0]--->", pdf[0])
            values = base64.b64encode(pdf[0])
            print("vals executed...")
            attachment_id = self.env['ir.attachment'].sudo().create(
                {'datas': values, 'name': 'student_records.pdf'})
            print("attachment_ids.....")
            mail_template_id.attachment_ids = attachment_id
            mail_template_id.send_mail(self.id, raise_exception=False, force_send=True)
            print("mail sent.....")
            # return self.env.ref('student_management.student_record_report').report_action(self, data=None)
        elif self.report_type == 'xls':
            print("report excel.....\n" * 5)
            workbook = xlwt.Workbook()
            stylePC = xlwt.XFStyle()
            worksheet = workbook.add_sheet('Student Records')
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
            for i in search_records:
                worksheet.write(row, 1, i.id)
                worksheet.write(row, 2, i.name)
                worksheet.write(row, 3, i.roll_no)
                worksheet.write(row, 4, i.qualification)
                row = row + 1
            row = row + 3
            print("no of rows....", row)
            print("no of rows.... prints row")

            worksheet.write(row, 5, 'Teacher:', bold)
            worksheet.write(row, 6, 'Darpan')
            tz = pytz.timezone('Asia/Kolkata')
            file_data = BytesIO()
            workbook.save(file_data)
            self.write({
                'data': base64.encodebytes(file_data.getvalue()),
                'file_name': 'Student Report - %s' % (datetime.now(tz).strftime('%Y-%m-%d %I:%M:%S')),
            })

            attachment_id = self.env['ir.attachment'].sudo().create(
                {'datas': self.data, 'name': self.file_name})
            print("attachment_ids.....")
            mail_template_id.attachment_ids = attachment_id
            mail_template_id.send_mail(self.id   , raise_exception=False, force_send=True)
            print("mail sent.....")
