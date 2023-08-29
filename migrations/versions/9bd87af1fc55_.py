"""empty message

Revision ID: 9bd87af1fc55
Revises: 7c9aec4e6b3e
Create Date: 2023-08-25 19:18:06.587806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bd87af1fc55'
down_revision = '7c9aec4e6b3e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('people_id', sa.Integer(), nullable=False))
        batch_op.alter_column('planet_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.create_foreign_key(None, 'people', ['people_id'], ['id'])
        batch_op.drop_column('name')
        batch_op.drop_column('type_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('planet_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('people_id')

    # ### end Alembic commands ###