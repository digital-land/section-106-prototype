"""empty message

Revision ID: 986668bdd192
Revises: 963bd289b895
Create Date: 2018-09-05 14:26:41.447301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '986668bdd192'
down_revision = '963bd289b895'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('planning_application', sa.Column('address', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('planning_application', 'address')
    # ### end Alembic commands ###
