"""add num field to Project table

Revision ID: fe566d6c618a
Revises: 
Create Date: 2023-04-26 17:28:11.389521

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fe566d6c618a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('module', schema=None) as batch_op:
        batch_op.alter_column('type',
               existing_type=mysql.INTEGER(),
               comment='模块类型，0：base，1：接口集成，2：应用集成，3：配置',
               existing_comment='集成类型，0：base，1：接口集成，2：应用集成',
               existing_nullable=False,
               existing_server_default=sa.text("'0'"))

    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('num', sa.Integer(), nullable=True, comment='数量'))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('token',
               existing_type=mysql.VARCHAR(length=100),
               comment='',
               existing_nullable=True)
        batch_op.alter_column('desc',
               existing_type=mysql.VARCHAR(length=100),
               comment='',
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('desc',
               existing_type=mysql.VARCHAR(length=100),
               comment=None,
               existing_comment='',
               existing_nullable=True)
        batch_op.alter_column('token',
               existing_type=mysql.VARCHAR(length=100),
               comment=None,
               existing_comment='',
               existing_nullable=True)

    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.drop_column('num')

    with op.batch_alter_table('module', schema=None) as batch_op:
        batch_op.alter_column('type',
               existing_type=mysql.INTEGER(),
               comment='集成类型，0：base，1：接口集成，2：应用集成',
               existing_comment='模块类型，0：base，1：接口集成，2：应用集成，3：配置',
               existing_nullable=False,
               existing_server_default=sa.text("'0'"))

    # ### end Alembic commands ###
