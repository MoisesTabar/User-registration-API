from fastapi import Depends, FastAPI, HTTPException
import utils, database, models, schemas
from database import db_state_default

database.db.connect()
database.db.create_tables([models.User, models.Secret])
database.db.close()

app = FastAPI()

async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()

#confirm the database state
def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()

#register user route
@app.post('/register', response_model = schemas.forRegister, dependencies=[Depends(get_db)])
def register(user: schemas.forRegister):
    user_exists = utils.verify_user(user.email, user.password)
    if user_exists:
        raise HTTPException(status_code = 400, detail = 'User already registered')
    return utils.register_user(user)
    
#login user route
@app.post('/login/', response_model = schemas.forLogin, dependencies=[Depends(get_db)])
def login(user: schemas.forLogin):
    user_exists = utils.verify_user(email = user.email, password = user.password)
    if not user_exists:
        raise HTTPException(status_code = 400, detail = 'User does not exist')
    return utils.login_user(user)

#update credentials
@app.post('/login/update/credentials', response_model = schemas.forUpdateCredentials, dependencies = [Depends(get_db)])
def update_credentials(user: schemas.forUpdateCredentials):
    email_exists = utils.verify_user(user.email, user.password)
    if not email_exists:
        raise HTTPException(status_code = 400, detail = 'Email does not exist')
    return utils.update_credentials(user)

#update password
@app.post('/login/update/password', response_model = schemas.forUpdatePassword, dependencies = [Depends(get_db)])
def update_password(user: schemas.forUpdatePassword):
    token_exists = utils.verify_token(token = user.token)
    if not token_exists:
        raise HTTPException(status_code = 400, detail = 'Token is not available')
    return utils.update_password(user)

#register secret
@app.post('/login/secrets/', response_model = schemas.forRegisterSecret, dependencies = [Depends(get_db)])
def register_secret(secret: schemas.forRegisterSecret):
    token_exists = utils.verify_token(token = secret.token)
    if not token_exists:
        raise HTTPException(status_code = 400, detail = 'Token is not available')
    return utils.register_secret(secret)

#delete secret
@app.post('/login/secrets/delete', response_model = schemas.forDeleteSecret, dependencies = [Depends(get_db)])
def delete_secret(secret: schemas.forDeleteSecret):
    token_exists = utils.verify_token(token = secret.token)
    if not token_exists:
        raise HTTPException(status_code = 400, detail = 'Token is not available')
    return utils.delete_secret(secret)

#visualize secret
@app.get('/login/secrets/{token}', dependencies = [Depends(get_db)])
def visualize_secret(token: str):
    token_exists = utils.verify_token(token = token)
    if not token_exists:
        raise HTTPException(status_code = 400, detail = 'Token is not available')
    return utils.visualize_secrets(token)

#logout
@app.get('/login/{token}', dependencies = [Depends(get_db)])
def logout(token: str):
    token_exists = utils.verify_token(token = token)
    if not token_exists:
        raise HTTPException(status_code = 400, detail = 'Token is not available')
    return utils.logout(token)