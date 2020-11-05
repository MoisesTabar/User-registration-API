from database import db
import models, schemas
import secrets
import datetime

def verify_user(email: str, password: str):
    return models.User.filter(
        models.User.email == email 
        and
        models.User.password == password 
    ).first()

def verify_token(token: str):
    return models.User.filter(
        models.User.token == token
    ).first()

def register_user(user: schemas.forRegister):
    new_user = models.User(
        name = user.name, 
        email = user.email, 
        password = user.password
    )
    new_user.save()
    return new_user

def login_user(user: schemas.forLogin):
    logged_user = models.User.update(token = secrets.token_urlsafe(15)).where(
        models.User.email == user.email,
        models.User.password == user.password
    )

    logged_user.execute()
    return models.User.select().where(
        models.User.email == user.email,
        models.User.password == user.password
    ).get()

def update_credentials(user: schemas.forUpdateCredentials):
    logged_user = models.User.update(name = user.name, email = user.email).where(
        models.User.password == user.password
    )

    logged_user.execute()
    return models.User.select().where(
        models.User.email == user.email,
        models.User.name == user.name
    ).get()

def update_password(user: schemas.forUpdatePassword):
    logged_user = models.User.update(password = user.password).where(
        models.User.token == user.token
    )

    logged_user.execute()
    return models.User.select().where(
        models.User.password == user.password,
        models.User.token == user.token
    ).get()

def register_secret(secret: schemas.forRegisterSecret):
    new_secret = models.Secret(
        title = secret.title,
        description = secret.description,
        monetary_value = secret.monetary_value,
        date = datetime.datetime.now(),
        place = secret.place,
        latitude = secret.latitude,
        longitude = secret.longitude,
        token = secret.token
    )

    new_secret.save()
    return new_secret

def delete_secret(secret: schemas.forDeleteSecret):
    del_secret = models.Secret.delete().where(
        models.Secret.token == secret.token
    )

    del_secret.execute()
    return [{'detail': 'Secret deleted'}]

def visualize_secrets(token: str):
    return models.Secret.select().where(
        models.Secret.token == token
    ).get()

def logout(token: str):
    log_out = models.User.update(token = None).where(
        models.User.token == token
    )

    log_out.execute()
    return [{'detail': 'logged out'}]

