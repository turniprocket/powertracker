from flask import render_template, redirect, url_for, flash, request, current_app, g, jsonify
from werkzeug.urls import url_parse
from flask_login import current_user, login_required
from pwgen import pwgen
import random, string
from app import db
from app.states.texas import bp
from app.states.texas.models import Contribution, Candidate, Contributor, Party, Government, Office, ContributionSource, Treasurer
from app.states.texas.forms import ContributionForm, SearchForm
from app.states.texas.submissions import switch
from app.models import User, Group
from app.search import query_index
from app.auth.group_check import group_check

record_types = ['contribution', 'candidate', 'contributor', 'party', 'government', 'office', 'source', 'treasurer']
search_indexes = {'all': '_all', 'contribution': 'texas_contribution', 'candidate': 'texas_candidate', 'contributor': 'texas_contributor',
                  'party': 'texas_party', 'government': 'texas_government', 'office': 'texas_office', 'contribution_source': 'texas_contribution_source',
                  'treasurer': 'texas_treasurer', 'held_by': 'texas_candidate', 'office_sought': 'texas_office', 'office_held': 'texas_office'}
search_suggestion_fields = {'texas_contributor': {'search_fields': ['name'], 'return_fields': ['name', 'public_id']},
                            'texas_candidate': {'search_fields': ['name'], 'return_fields': ['name', 'public_id']},
                            'texas_party': {'search_fields': ['name'], 'return_fields': ['name', 'public_id']},
                            'texas_government': {'search_fields': ['name'], 'return_fields': ['name', 'public_id']},
                            'texas_office': {'search_fields': ['name'], 'return_fields': ['name', 'public_id']},
                            'texas_source': {'search_fields': ['name'], 'return_fields': ['name', 'public_id']},
                            'texas_treasurer': {'search_fields': ['name'], 'return_fields': ['name', 'public_id']}}

@bp.before_app_request
def before_request():
    g.search_form = SearchForm()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    latest_contributions = Contribution.query.order_by(Contribution.contribution_date).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('texas.index', page=latest_contributions.next_num) \
        if latest_contributions.has_next else None
    prev_url = url_for('texas.index', page=latest_contributions.prev_num) \
        if latest_contributions.has_prev else None
    return render_template('states/texas/index.html', title='Texas Campaign Finance Home',latest_contributions=latest_contributions.items,
                            next_url=next_url, prev_url=prev_url)

@bp.route('/contribution', methods=['GET', 'POST'])
def contribution():
    if 'id' in request.args and request.args.get('id') != '':
        contribution = Contribution.query.filter_by(public_id=request.args.get('id')).first()
        return render_template('states/texas/contribution.html', contribution=contribution)
    return redirect(url_for('texas.contributions'))

@bp.route('/contributions', methods=['GET', 'POST'])
def contributions():
    page = request.args.get('page', 1, type=int)
    contributions_list = Contribution.query.order_by(Contribution.contribution_date).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('texas.contributions', page=contributions_list.next_num) \
        if contributions_list.has_next else None
    prev_url = url_for('texas.contributions', page=contributions_list.prev_num) \
        if contributions_list.has_prev else None
    return render_template('states/texas/contributions.html', title='All Contributions', contributions_list=contributions_list.items,
                            next_url=next_url, prev_url=prev_url)

@bp.route('/candidate', methods=['GET', 'POST'])
def candidate():
    if 'id' in request.args and request.args.get('id') != '':
        candidate = Candidate.query.filter_by(public_id=request.args.get('id')).first()
        contributions = candidate.get_received_contributions()
        return render_template('states/texas/candidate.html', candidate=candidate, contributions=contributions)
    return redirect(url_for('texas.candidates'))

@bp.route('/candidates', methods=['GET', 'POST'])
def candidates():
    page = request.args.get('page', 1, type=int)
    candidates_list = Candidate.query.order_by(Candidate.registration_date).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('texas.candidates', page=candidates_list.next_num) \
        if candidates_list.has_next else None
    prev_url = url_for('texas.candidates', page=candidates_list.prev_num) \
        if candidates_list.has_prev else None
    return render_template('states/texas/candidates.html', title='All Candidates', candidates_list=candidates_list.items,
                            next_url=next_url, prev_url=prev_url)

@bp.route('/contributor', methods=['GET', 'POST'])
def contributor():
    if 'id' in request.args and request.args.get('id') != '':
        contributor = Contributor.query.filter_by(public_id=request.args.get('id')).first()
        contributions = contributor.get_contributions()
        return render_template('states/texas/contributor.html', contributor=contributor, contributions=contributions)
    return redirect(url_for('texas.contributors'))

@bp.route('/contributors', methods=['GET', 'POST'])
def contributors():
    page = request.args.get('page', 1, type=int)
    contributors_list = Contributor.query.order_by(Contributor.date_added).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('texas.contributors', page=contributors_list.next_num) \
        if contributors_list.has_next else None
    prev_url = url_for('texas.contributors', page=contributors_list.prev_num) \
        if contributors_list.has_prev else None
    return render_template('states/texas/contributors.html', title='All Contributors', contributors_list=contributors_list.items,
                            next_url=next_url, prev_url=prev_url)

@bp.route('/party', methods=['GET', 'POST'])
def party():
    if 'id' in request.args and request.args.get('id') != '':
        party = Party.query.filter_by(public_id=request.args.get('id')).first()
        candidates = party.get_candidates() 
        contributors = party.get_contributors()
        return render_template('states/texas/party.html', party=party, contributors=contributors, candidates=candidates)
    return redirect(url_for('texas.parties'))

@bp.route('/parties', methods=['GET', 'POST'])
def parties():
    page = request.args.get('page', 1, type=int)
    parties_list = Party.query.order_by(Party.date_added).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('texas.parties', page=parties_list.next_num) \
        if parties_list.has_next else None
    prev_url = url_for('texas.parties', page=parties_list.prev_num) \
        if parties_list.has_prev else None
    return render_template('states/texas/parties.html', title='All Parties', parties_list=parties_list.items, next_url=next_url, prev_url=prev_url)

@bp.route('/government', methods=['GET', 'POST'])
def government():
    if 'id' in request.args and request.args.get('id') != '':
        government = Government.query.filter_by(public_id=request.args.get('id')).first()
        offices = government.get_offices()
        return render_template('states/texas/government.html', government=government, offices=offices)
    return redirect(url_for('texas.governments'))

@bp.route('/governments', methods=['GET', 'POST'])
def governments():
    page = request.args.get('page', 1, type=int)
    governments_list = Government.query.order_by(Government.date_added).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('texas.governments', page=governments_list.next_num) \
        if governments_list.has_next else None
    prev_url = url_for('texas.governments', page=governments_list.prev_num) \
        if governments_list.has_prev else None
    return render_template('states/texas/governments.html', title='All Governments', governments_list=governments_list.items, next_url=next_url, prev_url=prev_url)

@bp.route('office', methods=['GET', 'POST'])
def office():
    if 'id' in request.args and request.args.get('id') != '':
        office = Office.query.filter_by(public_id=request.args.get('id')).first()
        return render_template('states/texas/office.html', office=office)
    return redirect(url_for('texas.offices'))

@bp.route('/offices', methods=['GET', 'POST'])
def offices():
    page = request.args.get('page', 1, type=int)
    offices_list = Office.query.order_by(Office.date_added).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('texas.offices', page=offices_list.next_num) \
        if offices_list.has_next else None
    prev_url = url_for('texas.offices', page=offices_list.prev_num) \
        if offices_list.has_prev else None
    return render_template('states/texas/offices.html', title='All Offices', offices_list=offices_list.items, next_url=next_url, prev_url=prev_url)

@bp.route('/source', methods=['GET', 'POST'])
def source():
    if 'id' in request.args and request.args.get('id') != '':
        source = ContributionSource.query.filter_by(public_id=request.args.get('id')).first()
        return render_template('states/texas/source.html', source=source)
    return redirect(url_for('texas.sources'))

@bp.route('/sources', methods=['GET', 'POST'])
def sources():
    page = request.args.get('page', 1, type=int)
    sources_list = ContributionSource.query.order_by(ContributionSource.date_added).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('texas.sources', page=sources_list.next_num) \
        if sources_list.has_next else None
    prev_url = url_for('texas.sources', page=sources_list.prev_num) \
        if sources_list.has_prev else None
    return render_template('states/texas/sources.html', title='All Sources', sources_list=sources_list.items, next_url=next_url, prev_url=prev_url)

@bp.route('/treasurer', methods=['GET', 'POST'])
def treasurer():
    if 'id' in request.args and request.args.get('id') != '':
        treasurer = Treasurer.query.filter_by(public_id=request.args.get('id')).first()
        candidates = treasurer.get_candidate()
        return render_template('states/texas/treasurer.html', treasurer=treasurer, candidates=candidates)
    return redirect(url_for('texas.treasurers'))

@bp.route('/treasurers', methods=['GET', 'POST'])
def treasurers():
    page = request.args.get('page', 1, type=int)
    treasurers_list = Treasurer.query.order_by(Treasurer.date_added).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('texas.treasurers', page=treasurers_list.next_num) \
        if treasurers_list.has_next else None
    prev_url = url_for('texas.treasurers', page=treasurers_list.prev_num) \
        if treasurers_list.has_prev else None
    return render_template('states/texas/treasurers.html', title='All Treasurers', treasurers_list=treasurers_list.items, next_url=next_url, prev_url=prev_url)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
@group_check(role='texas')
def new():
    record_type = request.args.get('type')
    
    if switch.get(record_type) is not None:
         return switch[record_type]()
    else:
        return render_template('states/texas/new_select.html', title="Select new record type", record_types=record_types)

@bp.route('/search')
def search():
    if 'json' in request.args and 'index' in request.args:
        index = search_indexes[request.args.get('index')]
        query = request.args.get('q')
        results, total = query_index(index, query, search_suggestion_fields[index]['search_fields'], search_suggestion_fields[index]['return_fields'], 1, 10)
        return jsonify(results)

    if not g.search_form.validate():
        return redirect(url_for('texas.index'))
    page = request.args.get('page', 1, type=int)
    index = search_indexes[request.args.get('index')]
    search_fields = ['*']
    return_fields = ['*']
    results, total = query_index(index, g.search_form.q.data, search_fields, return_fields, page, current_app.config['POSTS_PER_PAGE'])    
    next_url = url_for('texas.search', q=g.search_form.q.data, index=request.args.get('index'), page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('texas.search', q=g.search_form.q.data, index=request.args.get('index'), page=page - 1) \
        if page > 1 else None

    return render_template('states/texas/search.html', title='Search', results=results, per_page=current_app.config['POSTS_PER_PAGE'], next_url=next_url, prev_url=prev_url)