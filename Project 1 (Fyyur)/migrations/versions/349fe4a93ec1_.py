"""empty message

Revision ID: 349fe4a93ec1
Revises: 9b922a79d6f3
Create Date: 2021-07-18 15:17:33.337936

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '349fe4a93ec1'
down_revision = '9b922a79d6f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Show_venue_id_fkey', 'Show', type_='foreignkey')
    op.drop_column('Show', 'venue_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('Show_venue_id_fkey', 'Show', 'Venue', ['venue_id'], ['id'])
    # ### end Alembic commands ###
