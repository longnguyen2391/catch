from flask import (
    Blueprint, 
    render_template,  
    jsonify, 
    redirect, 
    url_for, 
    request
)
from flask_login import login_user 
from werkzeug.security import check_password_hash

from ..user import User
from ..db import get_db 

bp = Blueprint('auth',__name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST': 
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password: 
            return jsonify({
                'status': 'fail', 
                'message': 'invalid data'
            }), 400

        db = get_db() 
        cursor = db.execute(
            'SELECT * FROM user WHERE username = ?',
            (username,)
        )
    
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password'], password): 
            current_user = User(user['id'], user['username'])
            login_user(current_user)

            return redirect(url_for('dashboard.dashboard'))
        else: 
            return jsonify({
                'status': 'failed', 
                'message': 'wrong username or password'
            })
    
    if request.method == 'GET': 
        return render_template('login.html')