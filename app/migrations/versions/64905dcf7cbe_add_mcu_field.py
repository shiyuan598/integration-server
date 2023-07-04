"""add mcu field

Revision ID: 64905dcf7cbe
Revises: 996582550e8a
Create Date: 2023-06-27 09:59:15.548433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64905dcf7cbe'
down_revision = '996582550e8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('app_process', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mcu', sa.String(length=200), nullable=True, comment='mcu数据'))

    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mcu_path', sa.Text(), nullable=False, comment='mcu的存放路径'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.drop_column('mcu_path')

    with op.batch_alter_table('app_process', schema=None) as batch_op:
        batch_op.drop_column('mcu')

    # ### end Alembic commands ###