import os

def configurate(app):
    # Код для налаштування конфігурації (наприклад, посилання до бази даних)
    
    # development 
    #app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1111@localhost:5432/postgres"
    #app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:040801@localhost:5432/library_db"
    #app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/library_db"
    #app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@db:5432/library_db"

    #app.config['SECRET_KEY'] = 'kfgvTKF_GgvgvfCFmg6yu6-VGHVgfvgGGhH_Szz245m_kkPh9qk'
    

    # production
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"  # So the token cache will be stored in a server-side session