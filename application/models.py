import uuid

from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db


def _generate_uuid():
    return uuid.uuid4()


class LocalAuthority(db.Model):

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(256))

    section106_agreements = db.relationship('Section106Agreement', back_populates='local_authority', lazy=True)


class Section106Agreement(db.Model):

    local_authority_id = db.Column(db.String(64), db.ForeignKey('local_authority.id'), nullable=False, primary_key=True)
    reference = db.Column(db.String(64), primary_key=True)

    signed_date = db.Column(db.Date)

    planning_application_reference = db.Column(db.String(64))
    planning_application_url= db.Column(db.String)

    local_authority = db.relationship('LocalAuthority', back_populates='section106_agreements')

    contributions = db.relationship('Contribution', lazy=True)


class Contribution(db.Model):

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['section106_reference', 'local_authority_id'],
            ['section106_agreement.reference', 'section106_agreement.local_authority_id'],
        ),
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=_generate_uuid)
    contribution_type = db.Column(db.String)
    category = db.Column(db.String)
    obligation = db.Column(db.String)
    value = db.Column(db.String)

    section106_reference = db.Column(db.String(64), nullable=False)
    local_authority_id = db.Column(db.String(64), nullable=False)
