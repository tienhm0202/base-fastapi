from pydantic.networks import EmailStr

from ..config import _MyBase


class EmailSettings(_MyBase):
    EMAILER_FROM_EMAIL: EmailStr
    EMAILER_FROM_NAME: str

    EMAILER_MAILGUN_DOMAIN: str
    EMAILER_MAILGUN_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".email.env"
