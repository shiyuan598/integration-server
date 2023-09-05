"""add testset field to Project table

Revision ID: 170760bb299f
Revises: 0a162d39fac1
Create Date: 2023-09-04 11:35:20.212387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '170760bb299f'
down_revision = '0a162d39fac1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('app_process', schema=None) as batch_op:
        batch_op.add_column(sa.Column('testset', sa.String(length=200), nullable=True, comment='测试集'))

    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('testset_path', sa.Text(), nullable=False, comment='测试集的存放路径'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.drop_column('testset_path')

    with op.batch_alter_table('app_process', schema=None) as batch_op:
        batch_op.drop_column('testset')

    # ### end Alembic commands ###