import enum
from datetime import date
from decimal import Decimal
from typing import Optional, TypeVar
from uuid import UUID

import sqlalchemy
from sqlalchemy import Index, UniqueConstraint, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import Field, Relationship
from src.db.common_sql_model import CommonSqlModel
from src.db.mixins import TimeStampWithIdMixin

ProjectsDataBase = declarative_base()

projects_sqlmodel_T = TypeVar("projects_sqlmodel_T", bound="ProjectsDataSQLModel")


class ProjectsDataSQLModel(CommonSqlModel):
    ...


ProjectsDataSQLModel.metadata = ProjectsDataBase.metadata  # type: ignore
# TODO: add indexes


class CompanyBase(ProjectsDataSQLModel):
    name: str = Field(nullable=False, index=True)
    region: str = Field(nullable=False)
    inn: str = Field(nullable=False)
    ogrn: str = Field(nullable=False)
    owner_id: UUID = Field(nullable=False)
    foundation_date: date = Field(nullable=False)


class Company(CompanyBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "companies"


class ProcurementBase(ProjectsDataSQLModel):
    spgz_id: str = Field(nullable=False)
    spgz_name: str = Field(nullable=False)
    procurement_date: date = Field(nullable=False)
    price: Decimal = Field(nullable=False)
    way_to_define_supplier: str = Field(nullable=False)
    contract_basis: str = Field(nullable=False)


class Procurement(ProcurementBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "procurements"


class ApplicationBase(ProjectsDataSQLModel):
    calculation_id: str | None = Field(nullable=True)
    lot_id: str | None = Field(nullable=True)
    client_id: str | None = Field(nullable=True)
    shipment_start_date: date | None = Field(nullable=True)
    shipment_end_date: date | None = Field(nullable=True)
    shipment_volume: int | None = Field(nullable=True)
    shipment_address: str | None = Field(nullable=True)
    shipment_terms: str | None = Field(nullable=True)
    year: int | None = Field(nullable=True)
    gar_id: str | None = Field(nullable=True)
    spgz_end_id: str | None = Field(nullable=True)
    amount: Decimal | None = Field(nullable=True)
    unit_of_measurement: str | None = Field(nullable=True)


class Application(ApplicationBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "appications"


class ProductBase(ProjectsDataSQLModel):
    name: str | None = Field(nullable=False)
    price: Decimal | None = Field(nullable=False)
    number: int | None = Field(nullable=False)
    amount: Decimal | None = Field(nullable=False)


class Product(ProductBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "products"


class RemainsBase(ProjectsDataSQLModel):
    cmo: str | None = Field(nullable=False)
    koc: int | None = Field(nullable=False)
    number: int | None = Field(nullable=False)
    indicator: int | None = Field(nullable=False)
    saldo_begin_debet: Decimal | None = Field(nullable=False)
    saldo_begin_credit: Decimal | None = Field(nullable=False)
    saldo_period_debet: Decimal | None = Field(nullable=False)
    saldo_period_credit: Decimal | None = Field(nullable=False)
    saldo_end_debet: Decimal | None = Field(nullable=False)
    saldo_end_credit: Decimal | None = Field(nullable=False)
    product_id: UUID | None = Field(nullable=False, foreign_key="products.id")


class Remains(RemainsBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "remains"


class ForecastBase(ProjectsDataSQLModel):
    product_id: UUID | None = Field(nullable=False, foreign_key="products.id")
    quarter: int | None = Field(nullable=False)
    year: int | None = Field(nullable=False)


class Forecast(ForecastBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "forecasts"


class UserCompanyBase(ProjectsDataSQLModel):  # TODO: точно ли это нужно или же просто owner для компании брать в ручках
    user_id: UUID | None = Field(nullable=False, foreign_key="users.id")
    company_id: UUID | None = Field(nullable=False, foreign_key="companies.id")


class UserCompany(UserCompanyBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "user_companies"

