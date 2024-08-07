from apps.home import blueprint
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from apps.tickets.forms import TicketForm
from apps.allUsers.forms import allUsersForm
from apps.authentication.models import TicketSupervisor, Users
from apps import db
from jinja2 import TemplateNotFound

#show 'all users' section data
@blueprint.route('/allUsers.html', methods=['GET'])
@login_required
def all_users():
    if request.method == 'GET':
        users = Users.query.all()
        return render_template('home/allUsers.html', users=users)

#'table' section
@blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = TicketForm()
    if form.validate_on_submit():
        new_ticket = TicketSupervisor(
            id=form.id.data,
            utente_apertura=form.utente_apertura.data,
            utente_segnalato=form.utente_segnalato.data,
            id_task=form.id_task.data,
            note=form.note.data,
            tag=form.tag.data,
            data_apertura=form.data_apertura.data,
            data_chiusura=form.data_chiusura.data,
            image=form.image
        )
        db.session.add(new_ticket)
        db.session.commit()
        flash('Ticket added successfully', 'success')
        return redirect(url_for('home_blueprint.index'))


    if request.method == 'GET':
        if current_user.is_admin:
            tickets = TicketSupervisor.query.all()
            return render_template('home/index.html', tickets=tickets, form=form)
        elif current_user.is_admin == 0:
            tickets = TicketSupervisor.query.filter_by(utente_segnalato=current_user.username).all()
            return render_template('home/index.html', tickets=tickets, form=form)
        else:
        # if the account is null
            return render_template('home/accountError.html')


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'
        # Detect the current page
        segment = get_segment(request)
        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except:
        return render_template('home/page-500.html'), 500

# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
