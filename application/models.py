import uuid

from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db


def _generate_uuid():
    return uuid.uuid4()


class LocalAuthority(db.Model):

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(256))

    planning_applications = db.relationship('PlanningApplication', back_populates='local_authority', lazy=True)

    def has_viability_assessments(self):
        if self.planning_applications:
            for p in self.planning_applications:
                if p.viability_assessments:
                    return True
            else:
                return False
        else:
            return False

class PlanningApplication(db.Model):

    reference = db.Column(db.String(64), primary_key=True)
    url = db.Column(db.String)

    local_authority_id = db.Column(db.String(64), db.ForeignKey('local_authority.id'), nullable=False, primary_key=True)
    local_authority = db.relationship('LocalAuthority', back_populates='planning_applications')

    section106_contributions = db.relationship('Contribution', lazy=True)
    section106_signed_date = db.Column(db.Date)
    section106_url = db.Column(db.String)

    viability_assessments = db.relationship('ViabilityAssessment', lazy=True, back_populates='planning_application')

    address = db.Column(db.String)


class Contribution(db.Model):

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['planning_application', 'local_authority_id'],
            ['planning_application.reference', 'planning_application.local_authority_id'],
        ),
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=_generate_uuid)
    contribution_type = db.Column(db.String)
    category = db.Column(db.String)
    obligation = db.Column(db.String)
    value = db.Column(db.String)

    planning_application = db.Column(db.String(64), nullable=False)
    local_authority_id = db.Column(db.String(64), nullable=False)


class ViabilityAssessment(db.Model):

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['planning_application_id', 'local_authority_id'],
            ['planning_application.reference', 'planning_application.local_authority_id'],
        ),
    )

    id = db.Column(db.String(64), primary_key=True)
    url = db.Column(db.String)
    date = db.Column(db.Date)

    planning_application_id = db.Column(db.String(64), nullable=False)
    planning_application = db.relationship('PlanningApplication')
    local_authority_id = db.Column(db.String(64), nullable=False)

    gross_development_value = db.Column(db.Integer)
    benchmark_land_value = db.Column(db.Integer)
    total_contribution = db.Column(db.Integer)