from flask import render_template, redirect, url_for, flash, request, current_app, g, jsonify
from werkzeug.urls import url_parse
from flask_login import current_user, login_required
from pwgen import pwgen
import random, string
from app import db
from app.states.texas import bp
from app.states.texas.models import Contribution, Candidate, Contributor
from app.states.texas.forms import ContributionForm, SearchForm
from app.states.texas.submissions import switch
from app.models import User, Group
from app.search import query_index
from app.auth.group_check import group_check

record_types = ['contribution', 'candidate', 'contributor', 'party', 'government', 'office', 'source', 'treasurer']
search_indexes = {'all': '_all', 'contributions': 'texas_contribution', 'candidates': 'texas_candidate', 'contributors': 'texas_contributor',
                  'partys': 'texas_party', 'governments': 'texas_government', 'offices': 'texas_office', 'contribution_sources': 'texas_contribution_source',
                  'treasurers': 'texas_treasurer'}
search_suggestion_fields = {'texas_contributor': {'search_fields': ['first_name', 'last_name'], 'return_fields': ['first_name', 'last_name', 'public_id']},
                            'texas_candidate': {'search_fields': ['first_name', 'last_name'], 'return_fields': ['first_name', 'last_name', 'public_id']}}
#search_query_feilds = {'all': {'search_fields': [first_name]}}

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