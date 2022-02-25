from dataclasses import dataclass
from typing import List

@dataclass
class Email:
    subject: str
    e_from: str
    date: str

@dataclass
class MySqlConfig:
    db: str
    host: str
    port: int
    user: str
    password: str

@dataclass
class AppConfig:
    loop_time: int
    criteria: str
    keyword: str
    unseen: str

@dataclass
class EmailConfig:
    email: str
    password: str
    connection_type: str
    mail_folder: str

class EmailList:
    def __init__(self, values: List[Email]):
        self.values = values