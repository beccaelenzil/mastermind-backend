"""empty message

Revision ID: 1ed010873717
Revises: 9d801840f56e
Create Date: 2023-01-02 15:14:09.222687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ed010873717'
down_revision = '9d801840f56e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('level',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('level',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
