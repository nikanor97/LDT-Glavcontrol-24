"""init_users

Revision ID: 68092a1b2729
Revises: 
Create Date: 2023-05-25 17:13:01.719446

"""
from alembic import op
import sqlmodel
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68092a1b2729'
down_revision = None
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    try:
        globals()["upgrade_%s" % engine_name]()
    except KeyError:
        pass


def downgrade(engine_name: str) -> None:
    try:
        globals()["downgrade_%s" % engine_name]()
    except KeyError:
        pass





def upgrade_projects() -> None:
    pass


def downgrade_projects() -> None:
    pass



def upgrade_users() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('telegram_username', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('permission_read_stat', sa.Boolean(), nullable=False),
        sa.Column('permission_create_order', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    op.create_table('user_passwords',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_passwords_user_id'), 'user_passwords', ['user_id'], unique=False)
    op.create_table('user_tokens',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('is_valid', sa.Boolean(), nullable=False),
        sa.Column('access_token', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('refresh_token', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('token_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('access_expires_at', sa.DateTime(), nullable=False),
        sa.Column('refresh_expires_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_tokens_user_id'), 'user_tokens', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade_users() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_tokens_user_id'), table_name='user_tokens')
    op.drop_table('user_tokens')
    op.drop_index(op.f('ix_user_passwords_user_id'), table_name='user_passwords')
    op.drop_table('user_passwords')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###

