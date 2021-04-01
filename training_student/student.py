##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be>).
#    Serpent Consulting Services Pvt. Ltd.
#    Copyright (C) 2014-2015 Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warradegreesty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
#    Module: Student Registration Management for College or University
#    Description: Demo Generated for purpose of ODOO 9 Technical Training in Arabic
#    Author: Serpent Consulting Services Pvt. Ltd.
#    Date: November 2015
#
##############################################################################


from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning
from datetime import datetime

STATE = [('draft','Draft'),
         ('med_interview','Medical Interview'),
         ('acad_interview','Academic Interview'),
         ('first_register','First Year Registered'),
         ('second_register','Second Year Registered'),
         ('third_register','Third Year Registered'),
         ('fourth_register','Fourth Year Registered'),
         ('dismiss','Dismissed'),
         ('alumni','Alumni')
         ]
###################################################################################################
class student_student(models.Model):
    _name = "student.student"
    _description= "Student Information"
    
    name = fields.Char(string="Name", required=True, index=True, translate=True)
    active = fields.Boolean(string="Active", default=True)
    image = fields.Binary("Image")
    uni_no = fields.Char(string="Ministry University No.", required=True, copy=False)
    seat_no = fields.Char("Seat No.", copy=False)
    dob = fields.Date(string="Date of Birth", required=True)
    age = fields.Integer(string="Age")
    gender = fields.Selection([("male","Male"),("female","Female")], "Gender", default="male")
    result_ids = fields.One2many("schoolresults.detail", "student_id", "School Results")
    hobbies_ids = fields.Many2many("hobbies.detail", "student_hobbies_rel", "student_id","hobbie_id", "Hobbies Information")
    responsible_id = fields.Many2one("res.partner", "Responsible Person / Next of Kin")
    # NOK - Next of Kin / Responsible Person
    email = fields.Char(related="responsible_id.email", string="NOK Email",)
    phone = fields.Char(related="responsible_id.phone", string="NOK Contact")
    fdate = fields.Date("First Registration Date")
    ldate = fields.Datetime("Last Registration Date", readonly=True)
    degree_id = fields.Many2one("degree.detail", "Degree to Register For")
    regfees = fields.Float("Registration Fees", default="0.0")
    tutfees = fields.Float("Tuition Fees ($)", default="0.0")
    totfees = fields.Float("Total Fees ($)",store=True, readonly=True, compute='_get_total_fees')
    ref = fields.Reference(selection=[("res.partner","Partner"),("res.users","User"),("student.student","Student")],string="Reference")
    ref_link = fields.Char("External Link")
    health_issues = fields.Selection([("yes","Yes"),("no","No")], "Health Issues", default="no")
    health_notes = fields.Text("Health Issue(s) Details", copy=False)
    template = fields.Html("Template")
    # Represents state of student
    state = fields.Selection(STATE, "Status", readonly=True, default="draft")
    
    # This method will generate the sequence on button clicked. with fetch the sequence
    # and append with faculty and department code

    def set_student_sequence(self):
        for student in self:
            next_seq = self.env['ir.sequence'].get('student.seatno.sequence')
            if student.degree_id:
                next_seq += ("/" + student.degree_id.dorf_id.code + "/")
                next_seq += student.degree_id.dord_id.code
            else:
                next_seq = ""
                raise Warning(_("Degree to register for not selected!"))
            student.seat_no =  next_seq
        return next_seq
    
    # Will use to test x2Many

    def test_x2Many(self):
        for student in self:
            # test (0, _, values) creating a new record
            #self.write({'result_ids':[(0,0,{'subject_id':'1', 'result':'85'})]})
            #self.write({'result_ids':[(0,0,{'subject_id':'2', 'result':'95'})]})
            # test (1, id, values) writing / updating a record
            #self.write({'result_ids':[(1,27,{'subject_id':'1', 'result':'90'})]})
            # test (3, id, values) deleting a record from DB keeping relation
            #self.write({'hobbies_ids':[[(5)]]})
            #self.write({'hobbies_ids':[(4,5)]})
            self.write({'hobbies_ids':[(6,0,[4,5])]})

    
    
    # overriding default get
    @ api.model
    def default_get(self, fields):
        res = super(student_student, self).default_get(fields)
        next_seq = self.env['ir.sequence'].get('student.unino.sequence')
        res.update({'uni_no': next_seq})
        return res
    
    # Get degree fees after specifying degree
    # Could have also used related
    # If you have multiple columns are used you separate via ,
    @api.onchange('degree_id')
    def _get_degree_fees(self):
        if self.degree_id:
            self.tutfees = self.degree_id.degfees
    

    @api.depends('regfees', 'tutfees')
    def _get_total_fees(self):
        if self.regfees or self.tutfees:
            self.totfees = self.regfees + self.tutfees
    
    @api.model
    def create(self, vals):
        print ("Values: ", vals)
        res = super(student_student, self).create(vals)
        print ("Result: ", res)
        audit_log_data={"user_id":self._uid, 
                        "date":datetime.today(), 
                        "student_info": self.id and (str(self.uni_no) + " " + str(self.name)),
                        "status": "create"}
        # Create a student.audit.log object
        self.env["student.audit.log"].create(audit_log_data)
        return res
    

    def copy(self):
        # can also used to change default behaviour
        res = super(student_student, self).copy()
        print ("Result: ", res)
        audit_log_data={"user_id":self._uid, 
                        "date":datetime.today(), 
                        "student_info": self.id and (str(self.uni_no) + " " + str(self.name)),
                        "status": "copy"}
        # Create a student.audit.log object
        self.env["student.audit.log"].create(audit_log_data)
        return res
        

    def write(self, vals):
        print ("Values: ", vals)
        res = super(student_student, self).write(vals)
        for student in self:
            audit_log_data={"user_id":self._uid, 
                        "date":datetime.today(), 
                        "student_info": self.id and (str(self.uni_no) + " " + str(self.name)),
                        "status": "write"}
            # Create a student.audit.log object
            self.env["student.audit.log"].create(audit_log_data)
        return res
    

    def unlink(self):
        for student in self:
            if student.state not in ['draft']:
                raise Warning(_("You are not allowed to delete the record!"))
                
        for student in self:
            audit_log_data={"user_id":self._uid,
                        "date":datetime.today(),
                        "student_info": self.id and (str(self.uni_no) + " " + str(self.name)),
                        "status": "delete"}
            # Create a student.audit.log object
            self.env["student.audit.log"].create(audit_log_data)
            
        res = super(student_student, self).unlink()
        return res
    
    # specify a constrain on number of characters entered

    @api.constrains('health_notes')
    def _no_chars(self):
            if self.health_notes:
                if len(self.health_notes) < 20:
                    raise Warning(_("Please enter a detailed description!"))
                
    # register first year

    def reg_first_year(self):
        self.state = 'first_register'
        self.ldate = datetime.now()
        
    # register second year

    def reg_second_year(self):
        self.state = 'second_register'
        self.ldate = datetime.now()
        
    # register third year

    def reg_third_year(self):
        self.state = 'third_register'
        self.ldate = datetime.now()
        
    # register fourth year

    def reg_fourth_year(self):
        self.state = 'fourth_register'
        self.ldate = datetime.now()
###################################################################################################               
class schoolresults_detail(models.Model):
    _name = "schoolresults.detail"
    _description = "Student's student secondary education results."
    
    student_id = fields.Many2one("student.student", "Student", ondelete="cascade")
    subject_id = fields.Many2one("schoolresults.subject", "Subject")
    result = fields.Float("Result")
################################################################################################### 
class schoolresults_subject(models.Model):
    _name = "schoolresults.subject"
    _description = "Student's student secondary education subjects."
    
    name = fields.Char("Subject")
###################################################################################################       
class hobbies_detail(models.Model):
    _name = "hobbies.detail"
    _description = "Student Hobbies"

    name = fields.Char("Name", required=True)
###################################################################################################
class degree_detail(models.Model):
    _name = "degree.detail"
    _description = "A registry of all possible degrees offered by university / college"
    
    name = fields.Char("Name", required=True)
    # Department or faculty
    dorf_id = fields.Many2one("dorf.information", "Department or Faculty", required=True)
    # Department or division
    dord_id = fields.Many2one("dord.information", "Division or Department")
    degfees = fields.Float("Fees per Year ($)")
    

    def name_get(self):
        """ Override get_name method to get combination in different format . """
         
        new_format = []
        for degree in self:
            new_info = ""
            new_info += degree.dorf_id.code or ""
            new_info += "-> "
            new_info +=  degree.dord_id.code or ""
            new_info += "-> "
            new_info += degree.name
            new_format.append((degree.id, new_info))
        return new_format   
###################################################################################################
class dorf_information(models.Model):
    _name = "dorf.information"
    _description = "A registry of all departments or faculties"
    _rec_name = 'code'

    code = fields.Char("Code", required=True)
    name = fields.Char("Name", required=True)
    
    # Make faculty name unique
    _sql_constraints = [
        ('dorf_code_unique',
         'UNIQUE(code)',
         "Faculty name must be unique!"),
    ]
###################################################################################################
class dord_information(models.Model):
    _name = "dord.information"
    _description = "A registry of all divisions or departments"
    _rec_name = 'code'

    code = fields.Char("Code", required=True)
    name = fields.Char("Name", required=True)
    # A division / department is owned by a department / faculty
    dorf_id = fields.Many2one("dorf.information", "Department or Faculty", required=True)
###################################################################################################  
#inheritance
class resPartner(models.Model):
    _inherit = 'res.partner'
    
    national_id = fields.Char(string='National ID')

