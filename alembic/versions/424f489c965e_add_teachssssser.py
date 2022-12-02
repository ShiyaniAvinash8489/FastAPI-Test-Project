"""Add teachssssser

Revision ID: 424f489c965e
Revises: d7cbc03f67b0
Create Date: 2022-05-31 11:38:20.236087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '424f489c965e'
down_revision = 'd7cbc03f67b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Teacher_user_id_fkey', 'Teacher', type_='foreignkey')
    op.create_foreign_key(None, 'Teacher', 'User', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Teacher', type_='foreignkey')
    op.create_foreign_key('Teacher_user_id_fkey', 'Teacher', 'User', ['user_id'], ['id'])
    # ### end Alembic commands ###