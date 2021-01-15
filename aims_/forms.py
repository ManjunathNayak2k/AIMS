from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from aims_.models import Broker, Admin,Company
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user

class RoleForm(FlaskForm):
    role = SelectField('Role', choices=['Broker', 'Admin', 'Company'])
    submit = SubmitField('Continue')


class RegistrationUserForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=['Broker', 'Admin'])
    sex = SelectField('Sex',choices = ['Male','Female'])
    street = StringField('Street',
                         validators=[DataRequired()])
    phone = StringField('Phone',
                        validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        role = self.role.data.lower()
        if role == 'broker':
            user = Broker.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username as Broker role is taken. Please choose a different one.')
        elif role == 'admin':
            user = Admin.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username as Admin role is taken. Please choose a different one.')
        else:
            raise ValidationError('Invalid role entered.')

    def validate_email(self, email):
        role = self.role.data.lower()
        if role == 'broker':
            user = Broker.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email as Broker role is taken. Please choose a different one.')
        elif role == 'admin':
            user = Admin.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email as Admin role is taken. Please choose a different one.')
        else:
            raise ValidationError('Invalid role entered.')
    
    def validate_phone(self,phone):
        if len(phone.data) < 10 or len(phone.data) > 10:
            raise ValidationError(
                'Please specify valid phone number.')


class RegistrationCompanyForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    street = StringField('Street',
                        validators=[DataRequired()])
    phone = StringField('Phone',
                        validators=[DataRequired()])
    specialization1 = SelectField(
        'Specialization', choices=['N/A','Electronics', 'Digital Services', 'Hardware','IT','Communication','Aeronautics','Agriculture','Research'])
    specialization2 = SelectField(
        'Specialization', choices=['N/A', 'Electronics', 'Digital Services', 'Hardware', 'IT', 'Communication', 'Aeronautics', 'Agriculture', 'Research'])
    specialization3 = SelectField(
        'Specialization', choices=['N/A','Electronics', 'Digital Services', 'Hardware','IT','Communication','Aeronautics','Agriculture','Research'])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Company.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username as Company role is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Company.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email as Company role is taken. Please choose a different one.')
    
    def validate_phone(self, phone):
        if len(phone.data) < 10 or len(phone.data) > 10:
            raise ValidationError(
                'Please specify valid phone number.')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role',choices = ['Broker','Admin','Company'])
    submit = SubmitField('Login')

class UploadInvoiceForm(FlaskForm):
    invoice_picture = FileField('Upload Invoice', validators=[DataRequired(),FileAllowed(['jpg', 'png','jpeg'])])
    coords_file = FileField('Upload Coordinates File', validators=[DataRequired(),FileAllowed(['csv','xlsx'])])
    submit = SubmitField('Upload')

class SelectBrokerForm(FlaskForm):
    broker = SelectField('Broker',choices = [broker.username for broker in Broker.query.all()])
    submit = SubmitField('Select')

class AssignCommissionForm(FlaskForm):
    newcommission = IntegerField('Commission',validators = [NumberRange(min=1, max=100, message='\nInput between 1 and 100')])
    submit = SubmitField('Done')

class AssignQuantityForm(FlaskForm):
    newquantity = IntegerField('Quantity', validators=[NumberRange(
        min=1, max=100, message='\nInput between 1 and 100')])
    submit = SubmitField('Update')

class ManualProcessForm(FlaskForm):
    compname = StringField('Company Name')
    compaddr = StringField('Company Address')
    invnum = StringField('Invoice Number')
    subt = StringField('Subtotal')
    disc= StringField('Discount')
    tax= StringField('Tax')
    total = StringField('Total')
    submit = SubmitField('Done')
