# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Protocol(db.Model):
    __tablename__ = 'protocol'

    id = db.Column(db.Integer, primary_key=True)
    competition_name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    hall = db.Column(db.String(100), nullable=False)
    stage = db.Column(db.String(100), nullable=False)
    match = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(100), nullable=False)

    # Исправлено
    winner = db.Column(db.Integer, db.ForeignKey('teams.id_teams'), nullable=False)  # Связь с таблицей teams
    link_protocol = db.Column(db.String(255), nullable=False)

    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    time = db.Column(db.Time, nullable=False)

    team1 = db.Column(db.Integer, db.ForeignKey('teams.id_teams'), nullable=False)  # Связь с таблицей teams
    team2 = db.Column(db.Integer, db.ForeignKey('teams.id_teams'), nullable=False)  # Связь с таблицей teams
    secretary = db.Column(db.Integer, db.ForeignKey('referees.id_referees'), nullable=False)  # Связь с таблицей referees
    referee = db.Column(db.Integer, db.ForeignKey('referees.id_referees'), nullable=False)  # Связь с таблицей referees

    # Устанавливаем отношения
    team1_relation = relationship("Teams", foreign_keys=[team1])
    team2_relation = relationship("Teams", foreign_keys=[team2])
    winner_relation = relationship("Teams", foreign_keys=[winner])
    secretary_relation = relationship("Referees", foreign_keys=[secretary])
    referee_relation = relationship("Referees", foreign_keys=[referee])


class Teams(db.Model):
    __tablename__ = 'teams'

    id_teams = db.Column(db.Integer, primary_key=True)  # ID (SERIAL)
    team_name = db.Column(db.String(100), nullable=False)  # Название команды
    head_coach = db.Column(db.String(100))  # Главный тренер
    assistant_coach = db.Column(db.String(100))  # Помощник тренера
    massage_therapist = db.Column(db.String(100))  # Массажист
    doctor = db.Column(db.String(100))  # Доктор

class Referees(db.Model):
    __tablename__ = 'referees'

    id_referees = db.Column(db.Integer, primary_key=True)  # ID (SERIAL)
    fio = db.Column(db.String(100), nullable=False)  # ФИО судьи
    city = db.Column(db.String(100), nullable=False)  # Город судьи
    position = db.Column(db.String(100), nullable=False)  # Должность судьи

class Players(db.Model):
    __tablename__ = 'players'

    id_players = db.Column(db.Integer, primary_key=True)  # ID (SERIAL)
    fio = db.Column(db.String(100), nullable=False)  # ФИО игрока
    player_number = db.Column(db.Integer, nullable=False)  # Номер игрока
    position = db.Column(db.String(100), nullable=False)  # Позиция игрока
    id_teams = db.Column(db.Integer, db.ForeignKey('teams.id_teams'), nullable=False)  # ID команды
    captain = db.Column(db.Boolean, nullable=False)  # Является ли капитаном

class Authorize(db.Model):
    __tablename__ = 'authorize'
    id = db.Column(db.Integer, primary_key=True)  # ID (SERIAL)
    fio = db.Column(db.String(255), nullable=False, unique=True)  # ФИО
    password = db.Column(db.String(255), nullable=False)  # Пароль