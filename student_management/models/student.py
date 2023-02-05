from odoo import fields, models, api
from odoo.osv import expression
import base64
import xlwt
from odoo.tools.misc import xlwt
import pytz
from datetime import *
from io import BytesIO
from odoo.exceptions import UserError


class StudentManagement(models.Model):
    _name = "custom.student"
    _description = 'Student Record'

    name = fields.Char(string='Student Name', required=True)
    roll_no = fields.Char(string='Student Roll.No')
    qualification = fields.Char(string='Student Qualification', required=True, default="Bachelor")
    total_exp = fields.Float(string='Total Experience', default=0.00)
    sale_order_details = fields.One2many('sale.order', 'student_sale', string="Sale Order Details")
    sale_order_ids = fields.Many2many('sale.order', string='Sale Order Options')
    dob = fields.Date(string='Date of Birth')
    Exp_state = fields.Selection(
        [('fresher', 'Fresher'), ('trainee', 'Trainee'), ('employee', 'Employed'), ('unemployee', 'Unemployed')])
    Emp_state = fields.Selection([('exp', 'Experience'), ('unexp', 'Unexperienced')])

    @api.onchange('Emp_state', 'total_exp')
    def change_experience(self):
        print("///////////////////////------------------ sale-order many 2 many ..... ", self.sale_order_ids)
        if self.Emp_state == 'exp':
            pass

    def unlink(self):
        print('//////////////////// ------- in delete function')
        if self.name != 'meet':
            res = super(StudentManagement, self).unlink()
            print("/////////////////////// ------------------- delete res ", res)
            return res
        else:
            print("/////////////////// ------------------ else part....")
            raise Exception("you cannot delete meet..!!!!")

    def name_get(self):
        res = []
        for student in self:
            name = str(student.id) + " , " + student.name
            res.append((student.id, name))
        print("//////////////////////-------------- name_get res", res)
        return res

    @api.model
    def _name_search(self, name, args=None, operator='in', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('id', operator, name)]
        res = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        print("////////////////////////------------- name_search res", res)
        return res

    def send_student_mail(self):
        template = self.env.ref('student_management.mail_student_record')
        template.send_mail(self.id, force_send=True)

    def print_excel_report(self):
        print('\n\n', 'darpan\n' * 5)
        print("////////////////// --------------------------from base excel report method called....!!!!")
        active_record_ids = self.env['custom.student'].search([('id', '=', self.id)])
        print("------------------- selected ids.... -------------", active_record_ids)
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
        print("/////////////------------- ---------------- res executed from base  ...!!!!!")
        print('\n\n..............-------------------------.-.-.-.-.-.-. res from base ----->>> ', res)
        return res

    # @api.model
    # def action_share(self):
    #     action = self.env["ir.actions.actions"]._for_xml_id("student_management.student_records_view")
    #     # action['context'] = {'active_id': self.env.context['active_id'],
    #     #                      'active_model': self.env.context['active_model']}
    #     print("/////////////// -------------------- action share called ...!!!!")
    #     if action:
    #         print("action found...!!!!!")
    #         return action
    #     else:
    #         print("action not found....!!!!")
