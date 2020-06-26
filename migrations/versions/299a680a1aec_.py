"""empty message

Revision ID: 299a680a1aec
Revises: 
Create Date: 2020-06-26 09:50:55.954553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '299a680a1aec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userName', sa.String(length=100), nullable=False),
    sa.Column('task', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('userName')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    # ### end Alembic commands ###
