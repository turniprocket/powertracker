from flask import render_template, redirect, url_for, current_app, flash
import random, string
from datetime import datetime
from app import db
from app.states.texas.models import Contribution, Candidate, Contributor, Party, Office, Treasurer, Government, Office, ContributionSource, Treasurer
from app.states.texas.forms import ContributionForm, CandidateForm, ContributorForm, PartyForm, GovernmentForm, OfficeForm, ContributionSourceForm, TreasurerForm
#TODO redo forms to add functions that add to association tables

def contribution_submission():
    form = ContributionForm()   

    if form.submit.data and form.validate_on_submit:
        new_contribution = Contribution(amount=form.amount.data, contribution_type=form.contribution_type.data, contribution_date=form.contribution_date.data, filing_date=form.filing_date.data, election_cycle=form.election_cycle.data,
                                        date_added=datetime.utcnow())
        random.seed(datetime.utcnow())
        new_contribution.public_id = ''.join(random.choice(string.ascii_letters) for i in range(10))
        db.session.add(new_contribution)
        db.session.commit()

        contribution = Contribution.query.filter_by(public_id=new_contribution.public_id).first()
        candidate = Candidate.query.filter_by(public_id=form.candidate_hidden.data).first()
        contributor = Contributor.query.filter_by(public_id=form.contributor_hidden.data).first()
        contribution.set_candidate(candidate)
        contribution.set_contributor(contributor)
        db.session.commit()

        flash('Contribution added')
        return redirect(url_for('texas.new'))

    return render_template('states/texas/new.html', Title='Add new contribution', form=form, record_type='contribution')

def candidate_submission():
    form = CandidateForm()

    if form.submit.data and form.validate_on_submit:
        new_candidate = Candidate(first_name=form.first_name.data, middle_name=form.middle_name.data, last_name=form.last_name.data, suffix=form.suffix.data, street_address=form.street_address.data,
                                    city=form.city.data, state=form.state.data, zip_code=form.zip_code.data, phone_number=form.phone_number.data, occupation=form.occupation.data, employer=form.employer.data,
                                    industry=form.industry.data, info=form.info.data, active=form.active.data, registration_date=form.registration_date.data, date_added=datetime.utcnow())
        random.seed(datetime.utcnow())
        new_candidate.public_id = ''.join(random.choice(string.ascii_letters) for i in range(10))
        db.session.add(new_candidate)
        db.session.commit()

        #candidate = Candidate.query.filter_by(public_id=new_candidate.public_id).first()
        #party = Party.query.filter_by(public_id=form.party_hidden.data).first()
        #office_sought = Office.query.filter_by(public_id=form.office_sought_hidden.data).first()
        #office_held = Office.query.filter_by(public_id=form.office_held_hidden.data).first()
        #treasurer = Treasurer.query.filter_by(public_id=form.treasurer_hidden.data).first()

        #party.add_candidate_member(candidate)
        #candidate.set_office_held(office_held)
        #candidate.set_office_sought(office_sought)
        #candidate.set_treasurer(treasurer)
        #db.session.commit()

        flash('Candidate added')
        return redirect(url_for('texas.new'))

    return render_template('states/texas/new.html', Title='Add new candidate', form=form, record_type='candidate')

def contributor_submission():
    form = ContributorForm()

    if form.submit.data and form.validate_on_submit:
        new_contributor = Contributor(first_name=form.first_name.data, middle_name=form.middle_name.data, last_name=form.last_name.data, suffix=form.suffix.data, street_address=form.street_address.data,
                                    city=form.city.data, state=form.state.data, zip_code=form.zip_code.data, phone_number=form.phone_number.data, occupation=form.occupation.data, employer=form.employer.data,
                                    industry=form.industry.data, info=form.info.data, contributor_type=form.contributor_type.data, pac_id=form.pac_id.data, date_added=datetime.utcnow())
        random.seed(datetime.utcnow())
        new_contributor.public_id = ''.join(random.choice(string.ascii_letters) for i in range(10))
        db.session.add(new_contributor)
        db.session.commit()

        #contributor = Contributor.query.filter_by(public_id=new_contributor.public_id.data).first()
        #party = Party.query.filter_by(public_id=form.party_hidden.data).first()

        #party.add_contributor_member(contributor)
        #db.session.commit()

        flash('Contributor added')
        return redirect(url_for('texas.new'))

    return render_template('states/texas/new.html', Title='Add new contributor', form=form, record_type='contributor')

def party_submission():
    form = PartyForm()

    if form.submit.data and form.validate_on_submit:
        new_party = Party(party_name=form.party_name.data, street_address=form.street_address.data, city=form.city.data, zip_code=form.zip_code.data, phone_number=form.phone_number.data, point_of_contact=form.point_of_contact.data,
                        committee_id=form.committee_id.data, info=form.info.data, date_added=datetime.utcnow())
        random.seed(datetime.utcnow())
        new_party.public_id = ''.join(random.choice(string.ascii_letters) for i in range(10))
        db.session.add(new_party)
        db.session.commit()

        flash('Party added')
        return redirect(url_for('texas.new'))        

    return render_template('states/texas/new.html', Title='Add new party', form=form, record_type='party')

def government_submission():
    form = GovernmentForm()

    if form.submit.data and form.validate_on_submit:
        new_government = Government(government_name=form.government_name.data, government_type=form.government_type.data, seat=form.seat.data, info=form.info.data, date_added=datetime.utcnow())
        random.seed(datetime.utcnow())
        new_government.public_id = ''.join(random.choice(string.ascii_letters) for it in range(10))
        db.session.add(new_government)
        db.session.commit()

        flash('Government added')
        return redirect(url_for('texas.new'))

    return render_template('states/texas/new.html', Title='Add new government', form=form, record_type='government')

def office_submission():
    form = OfficeForm()

    if form.submit.data and form.validate_on_submit:
        new_office = Office(office_name=form.office_name.data, info=form.info.data, date_added=datetime.utcnow()) 
        random.seed(datetime.utcnow())
        new_office.public_id = ''.join(random.choice(string.ascii_letters) for i in range(10))
        db.session.add(new_office)
        db.session.commit()

        #office = Office.query.filter_by(public_id=new_office.public_id).first()
        #government = Government.query.filter_by(public_id=form.government_hidden.data).first()
        #held_by = Candidate.query.filter_by(public_id=form.held_by_hidden.data).first()

        #government.add_office(office)
        #held_by.set_office_held(office)
        #db.session.commit()

        flash('Office added')
        return redirect(url_for('texas.new'))

    return render_template('states/texas/new.html', Title='Add new office', form=form, record_type='office')

def contribution_source_submission():
    form = ContributionSourceForm()

    if form.submit.data and form.validate_on_submit:
        new_contribution_source = ContributionSource(title=form.title.data, url=form.url.data, info=form.info.data, date_added=datetime.utcnow())
        random.seed(datetime.utcnow())
        new_contribution_source.public_id = ''.join(random.choice(string.ascii_letters) for i in range(10))
        db.session.add(new_contribution_source)
        db.session.commit()

        flash('Contribution Source added')
        return redirect(url_for('texas.new'))

    return render_template('states/texas/new.html', Title='Add new contribution source', form=form, record_type='source')

def treasurer_submission():
    form = TreasurerForm()

    if form.submit.data and form.validate_on_submit:
        new_treasurer = Treasurer(first_name=form.first_name.data, middle_name=form.middle_name.data, last_name=form.last_name.data, suffix=form.suffix.data, street_address=form.street_address.data,
                                    city=form.city.data, state=form.state.data, zip_code=form.zip_code.data, phone_number=form.phone_number.data, occupation=form.occupation.data, employer=form.employer.data,
                                    industry=form.industry.data, info=form.info.data, date_added=datetime.utcnow())

        random.seed(datetime.utcnow())
        new_treasurer.public_id = ''.join(random.choice(string.ascii_letters) for i in range(10))
        db.session.add(new_treasurer)
        db.session.commit()

        flash('Treasurer added')
        return redirect(url_for('texas.new'))

    return render_template('states/texas/new.html', Title='Add new treasurer', form=form, record_type='treasurer')       

switch = {'contribution': contribution_submission,
          'candidate': candidate_submission,
          'contributor': contributor_submission,
          'party': party_submission,
          'government': government_submission,
          'office': office_submission,
          'source': contribution_source_submission,
          'treasurer': treasurer_submission}