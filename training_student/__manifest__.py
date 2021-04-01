##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Serpent Consulting Services Pvt. Ltd.
#    Copyright (C) 2014-2015 Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
'name':'Student Registration Management',
'author':'Serpent Consulting Services Pvt. Ltd.',
'website':'http://www.serpentcs.com',
'category': 'Student',
'description': "A student registration management module",
'depends':['base','sale'],
'data':[
      'security/security_view.xml',
      'security/ir.model.access.csv',
      'wizard/wiz_calc_age_view.xml',
      'views/student_view.xml',
      'views/configuration_view.xml',
      'views/student_audit_log_view.xml',
      #'views/report_saleorder.xml',
      'sequence.xml',
      #'workflow/workflow.xml',
      'report/student_profile.xml',
      'report/student_report.xml'
],
'installable':True,
'auto_install':False,
'application':True,
}