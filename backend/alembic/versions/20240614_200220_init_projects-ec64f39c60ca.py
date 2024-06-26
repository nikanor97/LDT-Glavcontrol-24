"""init_projects

Revision ID: ec64f39c60ca
Revises: 68092a1b2729
Create Date: 2024-06-14 20:02:20.393731

"""
from alembic import op
import sqlmodel
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ec64f39c60ca'
down_revision = '68092a1b2729'
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
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_projects() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_projects() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('applications',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('calculation_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('lot_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('client_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('shipment_start_date', sa.Date(), nullable=True),
        sa.Column('shipment_end_date', sa.Date(), nullable=True),
        sa.Column('shipment_volume', sa.Integer(), nullable=True),
        sa.Column('shipment_address', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('shipment_terms', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('gar_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('spgz_end_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('amount', sa.Numeric(), nullable=True),
        sa.Column('unit_of_measurement', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('author_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_applications_author_id'), 'applications', ['author_id'], unique=False)
    op.create_index(op.f('ix_applications_calculation_id'), 'applications', ['calculation_id'], unique=False)
    op.create_index(op.f('ix_applications_client_id'), 'applications', ['client_id'], unique=False)
    op.create_index(op.f('ix_applications_lot_id'), 'applications', ['lot_id'], unique=False)
    op.create_index(op.f('ix_applications_status'), 'applications', ['status'], unique=False)
    op.create_index(op.f('ix_applications_year'), 'applications', ['year'], unique=False)
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies',
                    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('region', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('inn', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('ogrn', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('director', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('foundation_date', sa.Date(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_companies_name'), 'companies', ['name'], unique=False)
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
                    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('price', sa.Numeric(), nullable=False),
                    sa.Column('number', sa.Integer(), nullable=False),
                    sa.Column('amount', sa.Numeric(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_products_name'), 'products', ['name'], unique=False)
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('forecasts',
                    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('product_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('company_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('quarter', sa.Integer(), nullable=False),
                    sa.Column('year', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
                    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_forecasts_product_id'), 'forecasts', ['product_id'], unique=False)
    op.create_index(op.f('ix_forecasts_quarter'), 'forecasts', ['quarter'], unique=False)
    op.create_index(op.f('ix_forecasts_year'), 'forecasts', ['year'], unique=False)
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('procurements',
                    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('spgz_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column('spgz_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column('procurement_date', sa.Date(), nullable=True),
                    sa.Column('price', sa.Numeric(), nullable=True),
                    sa.Column('way_to_define_supplier', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column('contract_basis', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column('company_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_procurements_spgz_id'), 'procurements', ['spgz_id'], unique=False)
    op.create_index(op.f('ix_procurements_procurement_date'), 'procurements', ['procurement_date'], unique=False)
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('remains',
                    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('cmo', sa.String(), nullable=True),
                    sa.Column('koc', sa.Integer(), nullable=True),
                    sa.Column('number', sa.Integer(), nullable=True),
                    sa.Column('indicator', sa.Integer(), nullable=True),
                    sa.Column('saldo_begin_debet', sa.Numeric(), nullable=True),
                    sa.Column('saldo_begin_credit', sa.Numeric(), nullable=True),
                    sa.Column('saldo_period_debet', sa.Numeric(), nullable=True),
                    sa.Column('saldo_period_credit', sa.Numeric(), nullable=True),
                    sa.Column('saldo_end_debet', sa.Numeric(), nullable=True),
                    sa.Column('saldo_end_credit', sa.Numeric(), nullable=True),
                    sa.Column('product_id', sqlmodel.sql.sqltypes.GUID(), sa.ForeignKey('products.id'), nullable=True),
                    sa.Column('company_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_remains_product_id'), 'remains', ['product_id'], unique=False)
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_companies',
                    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('company_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    # sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_user_companies_user_id'), 'user_companies', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_companies_company_id'), 'user_companies', ['company_id'], unique=False)
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('application_products',
                    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('application_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('product_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ),
                    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_application_products_application_id'), 'application_products', ['application_id'], unique=False)
    op.create_index(op.f('ix_application_products_product_id'), 'application_products', ['product_id'], unique=False)
    # ### end Alembic commands ###


def downgrade_projects() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_application_products_application_id'), table_name='application_products')
    op.drop_index(op.f('ix_application_products_product_id'), table_name='application_products')
    op.drop_table('application_products')
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_applications_year'), table_name='applications')
    op.drop_index(op.f('ix_applications_status'), table_name='applications')
    op.drop_index(op.f('ix_applications_lot_id'), table_name='applications')
    op.drop_index(op.f('ix_applications_client_id'), table_name='applications')
    op.drop_index(op.f('ix_applications_calculation_id'), table_name='applications')
    op.drop_index(op.f('ix_applications_author_id'), table_name='applications')
    op.drop_table('applications')
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_forecasts_year'), table_name='forecasts')
    op.drop_index(op.f('ix_forecasts_quarter'), table_name='forecasts')
    op.drop_index(op.f('ix_forecasts_product_id'), table_name='forecasts')
    op.drop_table('forecasts')
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_procurements_procurement_date'), table_name='procurements')
    op.drop_index(op.f('ix_procurements_spgz_id'), table_name='procurements')
    op.drop_table('procurements')
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_remains_product_id'), table_name='remains')
    op.drop_table('remains')
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_companies_company_id'), table_name='user_companies')
    op.drop_index(op.f('ix_user_companies_user_id'), table_name='user_companies')
    op.drop_table('user_companies')
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_companies_name'), table_name='companies')
    op.drop_table('companies')
    # ### end Alembic commands ###

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_products_name'), table_name='products')
    op.drop_table('products')
    # ### end Alembic commands ###