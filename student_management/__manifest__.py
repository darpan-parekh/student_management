# -*- coding: utf-8 -*-
#################################################################################
# Author : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
###########################################################################


{
    'name': "Student Management",
    'website': "https:/google.com.in",
    'sequence': 1,
    'summary': "Managing student details",
    'author': "student",
    'version': '1.0',
    'category': 'Student Management/Student Mangement',
    'description': """ This module contains all the common features of Student Management and Information.
Student Management Systems Overview
===================================
Basic Features:
----------------------------------------------------
     * Student information storage, including grades and attendance
     * Faculty management
     * Report generation
     * Tool-assisted scheduling
     * Access portals for students and parents
     * Enrollment or registration management
     *  Medical and health management
     """,
    'depends': ['base', 'sale', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
        'report/report.xml',
        'report/student_report.xml',
        'data/send_mail_2_student.xml',
        'data/student_share_data.xml',
        'wizard/student_records.xml',
        'wizard/student_reports.xml',
    ],
    'demo': [],
    'installable': True
}
