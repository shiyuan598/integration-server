"""add update_time & create_time field for user table

Revision ID: ec20ec205b71
Revises: 646063b9a8a7
Create Date: 2023-05-04 11:23:40.471339

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ec20ec205b71'
down_revision = '646063b9a8a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
        batch_op.add_column(sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
        batch_op.alter_column('token',
               existing_type=mysql.VARCHAR(length=100),
               comment='验证登录有效性的token',
               existing_comment='token',
               existing_nullable=True)
        batch_op.alter_column('desc',
               existing_type=mysql.VARCHAR(length=100),
               comment='描述',
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('desc',
               existing_type=mysql.VARCHAR(length=100),
               comment=None,
               existing_comment='描述',
               existing_nullable=True)
        batch_op.alter_column('token',
               existing_type=mysql.VARCHAR(length=100),
               comment='token',
               existing_comment='验证登录有效性的token',
               existing_nullable=True)
        batch_op.drop_column('create_time')
        batch_op.drop_column('update_time')

    # ### end Alembic commands ###