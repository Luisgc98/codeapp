from app import create_app
from flask import redirect, url_for
from app import login_manager
from models import User

@login_manager.user_loader
def load_user(id):
    return User._byID(id)

app = create_app()

@app.route('/')
def index():
    
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)