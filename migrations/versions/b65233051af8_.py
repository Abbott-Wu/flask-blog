"""empty message

Revision ID: b65233051af8
Revises: 748c6aef5e2b
Create Date: 2017-09-02 18:42:50.985186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b65233051af8'
down_revision = '748c6aef5e2b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('img', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'img')
    # ### end Alembic commands ###
