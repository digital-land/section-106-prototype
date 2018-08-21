import uuid

from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db


def _generate_uuid():
    return uuid.uuid4()


class LocalAuthority(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(256))
    planning_applications = db.relationship('PlanningApplication', backref='local_authority', lazy=True)


class PlanningApplication(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    local_authority_id = db.Column(db.String(64), db.ForeignKey('local_authority.id'), nullable=False)
    section106 = db.relationship('Section106', uselist=False, back_populates='planning_application')


class Section106(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    agreement_date = db.Column(db.Date)
    planning_application_id = db.Column(db.String(64), db.ForeignKey('planning_application.id'))
    planning_application = db.relationship('PlanningApplication', back_populates='section106')
    contributions = db.relationship('Contribution', back_populates='section106', lazy=True)


class Contribution(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=_generate_uuid)
    contribution_type = db.Column(db.String)
    section106_id = db.Column(db.String(64), db.ForeignKey('section106.id'))
    section106 = db.relationship('Section106', back_populates='contributions')
