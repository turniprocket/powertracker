import base64
from datetime import datetime, timedelta
import json
import os
from time import time
from flask import current_app, url_for
from app import db, login
from app.search import add_to_index, remove_from_index, query_index

class BaseProfile(object):
    public_id = db.Column(db.String(8), index=True, unique=True)
    first_name = db.Column(db.String(32), index=True)
    middle_name = db.Column(db.String(32), index=True)
    last_name = db.Column(db.String(32), index=True)
    name = db.Column(db.String(128), index=True)
    suffix = db.Column(db.String(8))
    street_address = db.Column(db.String(32), index=True)
    city = db.Column(db.String(32), index=True)
    state = db.Column(db.String(12), index=True)
    zip_code = db.Column(db.String(10), index=True)
    phone_number = db.Column(db.String(12), index=True)
    occupation = db.Column(db.String(32))
    employer = db.Column(db.String(64), index=True)
    industry = db.Column(db.String(32), index=True)
    info = db.Column(db.String(256))

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        #wildcards being added to search query to allow partial matches within strings - move to search.py
        query = '*' + expression + '*'
        ids, indexes, total = query_index('texas_' + cls.__tablename__, query, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index('texas_' + obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index('texas_' + obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index('texas_' + obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index('texas_' + cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

## Political Database Models
candidate_party_membership = db.Table(
    'candidate_party_membership',
    db.Column('candidate_id', db.Integer, db.ForeignKey('candidate.id')),
    db.Column('party_id', db.Integer, db.ForeignKey('party.id'))
)

contributor_party_membership = db.Table(
    'contributor_party_membership',
    db.Column('contributor_id', db.Integer, db.ForeignKey('contributor.id')),
    db.Column('party_id', db.Integer, db.ForeignKey('party.id'))
)

contribution_contributor = db.Table(
    'contributions_contributors',
    db.Column('contributor_id', db.Integer, db.ForeignKey('contributor.id')),
    db.Column('contribution_id', db.Integer, db.ForeignKey('contribution.id'))
)

contribution_candidate = db.Table(
    'contribution_candidate',
    db.Column('candidate_id', db.Integer, db.ForeignKey('candidate.id')),
    db.Column('contribution_id', db.Integer, db.ForeignKey('contribution.id'))
)

contribution_sources = db.Table(
    'contribution_sources',
    db.Column('contribution_id', db.Integer, db.ForeignKey('contribution.id')),
    db.Column('contribution_source_id', db.Integer, db.ForeignKey('contribution_source.id'))
)

government_offices = db.Table(
    'government_offices',
    db.Column('government_id', db.Integer, db.ForeignKey('government.id')),
    db.Column('office_id', db.Integer, db.ForeignKey('office.id'))
)

offices_sought = db.Table(
    'offices_sought',
    db.Column('candidate_id', db.Integer, db.ForeignKey('candidate.id')),
    db.Column('office_id', db.Integer, db.ForeignKey('office.id'))
)

offices_held = db.Table(
    'offices_held',
    db.Column('candidate_id', db.Integer, db.ForeignKey('candidate.id')),
    db.Column('office_id', db.Integer, db.ForeignKey('office.id'))
)

treasurers = db.Table(
    'treasurers',
    db.Column('candidate_id', db.Integer, db.ForeignKey('candidate.id')),
    db.Column('treasurer_id', db.Integer, db.ForeignKey('treasurer.id'))
)

class Contribution(SearchableMixin ,db.Model):
    __searchable__ = ['public_id', 'amount', 'contribution_type', 'contribution_date', 'filing_date', 'election_cycle']
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(8), index=True, unique=True)
    amount = db.Column(db.Integer)
    contribution_type = db.Column(db.String(1), index=True)
    contribution_date = db.Column(db.DateTime, index=True)
    filing_date = db.Column(db.DateTime, index=True)
    election_cycle = db.Column(db.String(7), index=True)
    date_added = db.Column(db.DateTime, index=True)
    #contribution_source

    contributor_id = db.relationship(
        'Contributor',
        secondary=contribution_contributor,
        primaryjoin=(contribution_contributor.c.contribution_id == id),
        backref=db.backref('contributor', lazy='dynamic'), lazy='dynamic')

    candidate_id = db.relationship(
        'Candidate',
        secondary=contribution_candidate,
        primaryjoin=(contribution_candidate.c.contribution_id == id),
        backref=db.backref('candidate', lazy='dynamic'), lazy='dynamic')

    contribution_source = db.relationship(
        'ContributionSource',
        secondary=contribution_sources,
        primaryjoin=(contribution_sources.c.contribution_id == id),
        backref=db.backref('contribution_source', lazy='dynamic'), lazy='dynamic')

    def set_candidate(self, candidate):
        if not self.get_candidate():
            self.candidate_id.append(candidate)

    def get_candidate(self):
        return self.candidate_id.filter(
            contribution_candidate.c.contribution_id == self.id).first()

    def set_contributor(self, contributor):
        if not self.get_contributor():
            self.contributor_id.append(contributor)

    def get_contributor(self):
        return self.contributor_id.filter(
            contribution_contributor.c.contribution_id == self.id).first()

    def set_contribution_source(self, contribution_source):
        if not self.get_contribution_source():
            self.contribution_source.append(contribution_source)

    def get_contribution_source(self):
        return self.contribution_source.filter(
            contribution_sources.c.contribution_id == self.id).first()
    
class Candidate(SearchableMixin, BaseProfile, db.Model):
    __searchable__ = ['public_id', 'first_name', 'middle_name', 'last_name', 'name', 'street_address', 'city', 'state', 'zip_code', 'phone_number',
                      'occupation', 'employer', 'industry']
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, index=True)
    registration_date = db.Column(db.DateTime, index=True)
    date_added = db.Column(db.DateTime, index=True)

    party = db.relationship(
        'Party',
        secondary=candidate_party_membership,
        primaryjoin=(candidate_party_membership.c.candidate_id == id),
        backref=db.backref('candidate_party_membership', lazy='dynamic'), lazy='dynamic')

    office_sought = db.relationship(
        'Office',
        secondary=offices_sought,
        primaryjoin=(offices_sought.c.candidate_id == id),
        backref=db.backref('offices_sought', lazy='dynamic'), lazy='dynamic')

    office_held = db.relationship(
        'Office',
        secondary=offices_held,
        primaryjoin=(offices_held.c.candidate_id == id),
        backref=db.backref('offices_held', lazy='dynamic'), lazy='dynamic')

    received_contributions = db.relationship(
        'Contribution',
        secondary=contribution_candidate,
        primaryjoin=(contribution_candidate.c.candidate_id == id),
        backref=db.backref('contribution_candidate', lazy='dynamic'), lazy='dynamic')

    treasurer = db.relationship(
        'Treasurer',
        secondary=treasurers,
        primaryjoin=(treasurers.c.candidate_id == id),
        backref=db.backref('treasurer', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Candidate: {}>'.format(self.name)

    def get_party(self):
        return self.party.filter(
            candidate_party_membership.c.candidate_id == self.id).first()

    def get_office_held(self):
        return self.office_held.filter(
            offices_held.c.candidate_id == self.id).first()

    def set_office_held(self, office):
        if not self.get_office_held():
            self.office_held.append(office)

    def get_office_sought(self):
        return self.offices_sought.filter(
            offices_sought.c.candidate_id == self.id).first()

    def set_office_sought(self, office):
        if not self.get_office_sought():
            self.office_sought.append(office)

    def get_treasurer(self):
        return self.treasurer.filter(
            treasurers.c.candidate_id == self.id).first()
    
    def set_treasurer(self, treasurer):
        if not self.get_treasurer():
            self.treasurer.append(treasurer)

    def get_received_contributions(self):
        return self.received_contributions.filter(
            contribution_candidate.c.candidate_id == self.id).all()

class Contributor(SearchableMixin, BaseProfile, db.Model):
    __searchable__ = ['public_id', 'first_name', 'middle_name', 'last_name', 'name', 'street_address', 'city', 'state', 'zip_code', 'phone_number',
                      'occupation', 'employer', 'industry']
    id = db.Column(db.Integer, primary_key=True)
    contributor_type = db.Column(db.String(1), index=True)
    pac_id = db.Column(db.String(32), index=True)
    date_added = db.Column(db.DateTime, index=True)

    party = db.relationship(
        'Party',
        secondary=contributor_party_membership,
        primaryjoin=(contributor_party_membership.c.contributor_id == id),
        backref=db.backref('contributor_party_membership', lazy='dynamic'), lazy='dynamic')

    contributions = db.relationship(
        'Contribution',
        secondary=contribution_contributor,
        primaryjoin=(contribution_contributor.c.contributor_id == id),
        backref=db.backref('contribution_contributor', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Contributor: {}>'.format(self.name)

    def get_party(self):
        return self.party.filter(contributor_party_membership.c.contributor_id == self.id).first()

    def get_contributions(self):
        return self.contributions.filter(
            contribution_contributor.c.contributor_id == self.id).all()

class Party(SearchableMixin, db.Model):
    __searchable__ = ['public_id', 'name', 'street_address', 'city', 'state', 'zip_code', 'phone_number',
                      'point_of_contact', 'committee_id']
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(8), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    street_address = db.Column(db.String(64), index=True)
    city = db.Column(db.String(32), index=True)
    state = db.Column(db.String(2), index=True)
    zip_code = db.Column(db.String(10), index=True)
    phone_number = db.Column(db.Integer, index=True)
    point_of_contact = db.Column(db.String(32))
    committee_id = db.Column(db.String(32), index=True)
    info = db.Column(db.String(256))
    date_added = db.Column(db.DateTime, index=True)

    candidate_members = db.relationship(
        'Candidate',
        secondary=candidate_party_membership,
        primaryjoin=(candidate_party_membership.c.party_id == id),
        backref=db.backref('candidate_party', lazy='dynamic'), lazy='dynamic')

    contributor_members = db.relationship(
        'Contributor',
        secondary=contributor_party_membership,
        primaryjoin=(contributor_party_membership.c.party_id == id),
        backref=db.backref('contributor_party', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Party: {}>'.format(self.name)

    def add_candidate_member(self, candidate):
        if not self.candidate_in_party(candidate):
            self.candidate_members.append(candidate)

    def remove_candidate_member(self, candidate):
        if self.candidate_in_party(candidate):
            self.candidate_members.remove(candidate)

    def add_contributor_member(self, contributor):
        if not self.contributor_in_party(contributor):
            self.contributor_members.append(contributor)

    def remove_contributor_member(self, contributor):
        if self.contributor_in_party(contributor):
            self.contributor_members.remove(contributor)

    def candidate_in_party(self, candidate):
        return self.candidate_members.filter(
            candidate_party_membership.c.candidate_id == candidate.id).count() > 0

    def contributor_in_party(self, contributor):
        return self.contributor_members.filter(
            contributor_party_membership.c.contributor_id == contributor.id).count() > 0

    def get_candidates(self):
        return self.candidate_members.filter(
            candidate_party_membership.c.party_id == self.id).all()

    def get_contributors(self):
        return self.contributor_members.filter(
            contributor_party_membership.c.party_id == self.id).all()

class Government(SearchableMixin, db.Model):
    __searchable__ = ['public_id', 'name', 'government_type', 'seat']
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(8), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    government_type = db.Column(db.String(16))
    seat = db.Column(db.String(32), index=True)
    info = db.Column(db.String(256))
    date_added = db.Column(db.DateTime, index=True)

    offices = db.relationship(
        'Office',
        secondary=government_offices,
        primaryjoin=(government_offices.c.government_id == id),
        backref=db.backref('government_offices', lazy='dynamic'), lazy='dynamic')

    def add_office(self, office):
        if not self.office_in_government(office):
            self.offices.append(office)

    def remove_office(self, office):
        if self.office_in_government(office):
            self.offices.remove(office)

    def get_offices(self):
        return self.offices.filter(
            government_offices.c.government_id == self.id).all()

    def office_in_government(self, office):
        return self.offices.filter(
            government_offices.c.office_id == office.id).count() > 0

class Office(SearchableMixin,   db.Model):
    __searchable__ = ['public_id', 'name']
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(8), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    info = db.Column(db.String(256))
    date_added = db.Column(db.DateTime, index=True)

    government = db.relationship(
        'Government',
        secondary=government_offices,
        primaryjoin=(government_offices.c.office_id == id),
        backref=db.backref('government_offices', lazy='dynamic'), lazy='dynamic')

    held_by = db.relationship(
        'Candidate',
        secondary=offices_held,
        primaryjoin=(offices_held.c.office_id == id),
        backref=db.backref('offices_held', lazy='dynamic'), lazy='dynamic')

    sought_by = db.relationship(
        'Candidate',
        secondary=offices_sought,
        primaryjoin=(offices_sought.c.office_id == id),
        backref=db.backref('offices_sought', lazy='dynamic'), lazy='dynamic')

    def get_government(self):
        return self.government.filter(
            government_offices.c.office_id == self.id).first()

    def get_office_holder(self):
        return self.held_by.filter(
            offices_held.c.office_id == self.id).first()

    def get_office_seekers(self):
        return self.sought_by.filter(
            offices_sought.c.office_id == self.id).all()

class ContributionSource(SearchableMixin, db.Model):
    __searchable__ = ['public_id', 'name']
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(8), index=True, unique=True)
    name = db.Column(db.String(64))
    url = db.Column(db.String(256))
    info = db.Column(db.String(256))
    date_added = db.Column(db.DateTime, index=True)

    contributions = db.relationship(
        'Contribution',
        secondary=contribution_sources,
        primaryjoin=(contribution_sources.c.contribution_source_id == id),
        backref=db.backref('contributions', lazy='dynamic'), lazy='dynamic')

    def get_contributions(self):
        return self.contributions.filter(
            contribution_sources.c.contribution_source_id == self.id).all()

class Treasurer(SearchableMixin, BaseProfile, db.Model):
    __searchable__ = ['public_id', 'first_name', 'middle_name', 'last_name', 'name', 'street_address', 'city', 'state', 'zip_code', 'phone_number',
                      'occupation', 'employer', 'industry']
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, index=True)
    
    candidates = db.relationship(
        'Candidate',
        secondary=treasurers,
        primaryjoin=(treasurers.c.treasurer_id == id),
        backref=db.backref('candidates', lazy='dynamic'), lazy='dynamic')

    def get_candidate(self):
        return self.candidates.filter(
            treasurers.c.treasurer_id == self.id).all()