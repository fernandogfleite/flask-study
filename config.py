from decouple import config


class Config:
    DATABASE_URI = "postgresql+psycopg2://{}:{}@{}/{}".format(
        config("POSTGRES_USER"),
        config("POSTGRES_PASSWORD"),
        config("POSTGRES_HOST"),
        config("POSTGRES_DB")
    )
    SECRET_KEY = config("SECRET_KEY")
