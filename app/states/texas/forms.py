from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField, DateField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, Length
from app.statelist import statelist
from app.governmentlist import governmentlist
# from states.texas.models 

#TODO create custom validators for things like phone numbers at some point
#TODO add asteriks to required fields
#TODO validators maybe rewrite the data before submitting it to make it consistent

class BaseProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[Length(max=32)])
    middle_name = StringField('Middle Name', validators=[Length(max=32)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=32)])
    suffix = StringField('Suffix (e.g. Jr, Mr, Mrs, etc', validators=[Length(max=8)])
    street_address = StringField('Street Address', validators=[Length(max=32)])
    city = StringField('City', validators=[DataRequired(), Length(max=32)])
    state = SelectField('State', choices=statelist, validate_choice=True)
    zip_code = StringField('Zip Code', validators=[DataRequired(), Length(max=10)])
    phone_number = StringField('Phone Number', validators=[Length(max=12)])
    occupation = StringField('Occupation/Title', validators=[Length(max=32)])
    employer = StringField('Employer/Company', validators=[Length(max=64)])
    industry = StringField('Industry', validators=[Length(max=32)])
    info = TextAreaField('Info', validators=[Length(max=256)])

class ContributionForm(FlaskForm):
    amount = IntegerField('Amount', validators=[DataRequired()])
    contribution_type = SelectField('Contribution Type', choices=[('P', 'PAC'), ('I', 'Individual'), ('L', 'Loan')], validators=[DataRequired()])
    contribution_date = DateField('Contribution Date', format='%m/%d/%Y')
    filing_date = DateField('Filing Date', format='%m/%d/%Y', validators=[DataRequired()])
    election_cycle = StringField('Election Cycle', validators=[DataRequired()])
    contributor = StringField('Contributor', validators=[DataRequired()])
    contributor_hidden = HiddenField(validators=[DataRequired()])
    candidate = StringField('Candidate', validators=[DataRequired()])
    candidate_hidden = HiddenField(validators=[DataRequired()])
    source = StringField('Info Source')
    submit = SubmitField('Add Contribution')

class CandidateForm(BaseProfileForm):
    active = BooleanField('Active')
    registration_date = DateField('Registration Date', format='%m/%d/%Y')
    party = StringField('Party')
    party_hidden = HiddenField()
    office_sought = StringField('Office Sought')
    office_sought_hidden = HiddenField()
    office_held = StringField('Office Held')
    office_held_hidden = HiddenField()
    treasurer = StringField('Treasurer')
    treasurer_hidden = HiddenField()
    submit = SubmitField('Add Candidate')

class ContributorForm(BaseProfileForm):
    contributor_type = SelectField('Contributor Type', choices=[('P', 'PAC'), ('I', 'Individual'), ('C', 'Company')], validators=[DataRequired()])
    pac_id = StringField('PAC ID')
    party = StringField('Party')
    party_hidden = HiddenField()
    submit = SubmitField('Add Contributor')

class PartyForm(FlaskForm):
    name = StringField('Party Name', validators=[DataRequired(), Length(max=64)])
    street_address = StringField('Street Address', validators=[Length(max=64)])
    city = StringField('City', validators=[DataRequired(), Length(max=32)])
    state = SelectField('State', choices=statelist, validate_choice=True, validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired(), Length(max=10)])
    phone_number = StringField('Phone Number', validators=[Length(max=12)])
    point_of_contact = StringField('Point of Contact', validators=[Length(max=32)])
    committee_id = StringField('Committee ID', validators=[Length(max=32)])
    info = TextAreaField('Info', validators=[Length(max=256)])
    submit = SubmitField('Add Party')

class GovernmentForm(FlaskForm):
    name = StringField('Government Name', validators=[DataRequired(), Length(max=64)])
    government_type = SelectField('Government Type', choices=governmentlist, validate_choice=True)
    seat = StringField('Seat of Government', validators=[DataRequired(), Length(max=32)])
    info = TextAreaField('Info', validators=[Length(max=256)])
    submit = SubmitField('Add Government')

class OfficeForm(FlaskForm):
    name = StringField('Office Name', validators=[DataRequired(), Length(max=64)])
    government = StringField('Government', validators=[DataRequired()])
    government_hidden = HiddenField(validators=[DataRequired()])
    held_by = StringField('Current Office Holder', validators=[DataRequired()])
    held_by_hidden = HiddenField(validators=[DataRequired()])
    info = TextAreaField('Info', validators=[Length(max=256)])
    submit = SubmitField('Add Office')

class ContributionSourceForm(FlaskForm):
    name = StringField('Source Title', validators=[DataRequired(), Length(max=64)])
    url = StringField('URL', validators=[Length(max=256)])
    info = TextAreaField('Info', validators=[Length(max=256)])
    submit = SubmitField('Add Contribution Source')

class TreasurerForm(BaseProfileForm):
    submit = SubmitField('Add Treasurer')

class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])
    index = SelectField('', choices=[('all', 'All'), ('contribution', 'Contributions'), ('candidate', 'Candidates'), ('contributor', 'Contributors')])
    submit = SubmitField('Search')
    
    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            # This is where the get arguments like q=search are being passed to the form
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)