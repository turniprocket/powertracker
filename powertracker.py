from app import create_app, db
from app.models import User, Group
from config import Config

app = create_app()

# Runs before requests are made and will create tables and create administrators and admin user if they do not exist
@app.before_first_request
def create_admin_account():
    engine = db.get_engine()
    if not engine.dialect.has_table(engine, 'group') or engine.dialect.has_table(engine, 'user'):
        db.create_all()
        db.session.commit()
        print('Tables Created')
    else:
        print('Tables already exist')
    
    group = Group.query.filter_by(group_name=Config.ADMIN_GROUP_NAME).first()
    if group is None:
        group = Group(group_name=Config.ADMIN_GROUP_NAME)
        db.session.add(group)
        db.session.commit()
        print(group.group_name + ' group created.')
    else:
        print(group.group_name + ' group already exists.')

    user = User.query.filter_by(username=Config.DEFAULT_ADMIN_USERNAME).first()
    if user is None:
        user = User(username=Config.DEFAULT_ADMIN_USERNAME, email=Config.DEFAULT_ADMIN_EMAIL)
        user.set_password(Config.DEFAULT_ADMIN_PASSWORD)
        db.session.add(user)
        db.session.commit()

        user.add_to_group(group)
        db.session.commit()
        print(user.username + ' user created and added to ' + group.group_name + '.')
    else:
        print(user.username + ' user already exists.')
    
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Group': Group}