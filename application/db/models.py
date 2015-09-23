# coding=utf-8
# Created by Anton Dementev on 22.09.15 
from datetime import datetime

from peewee import Model, PostgresqlDatabase, PrimaryKeyField, CharField, BooleanField, ForeignKeyField, IntegerField, \
    TextField, DateField, DecimalField, FloatField
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from server import settings
import helpers

db = PostgresqlDatabase(
    settings.DB_NAME,
    user=settings.DB_ADMIN,
    password=settings.DB_PASSWORD
)


class BaseModel(Model):
    id = PrimaryKeyField()

    class Meta:
        database = db


class RootObject(BaseModel):

    name = CharField()


class Client(RootObject):

    pass


class District(RootObject):

    pass


class Material(RootObject):

    pass


class Installer(RootObject):

    pass


class Size(RootObject):

    pass


class InstallationType(RootObject):

    pass


class PriceType(RootObject):

    name_for_invoice = CharField(default="")
    measurement = CharField(default="")

    def value_for_date(self, date):
        rounded_date = helpers.rounded_date(date)
        current_value = PriceHistory.select().where(
            (PriceHistory.price_type == self) &
            (PriceHistory.start <= rounded_date) &
            (PriceHistory.finish == None)
        ).first()
        if current_value:
            return current_value.value
        else:
            return 0.0


class ConstructionStatus(RootObject):

    pass


class PartnerOrganization(RootObject):

    full_name = CharField(null=True)
    address = CharField(null=True)
    phones = CharField(null=True)
    email = CharField(null=True)
    inn = CharField(null=True)
    kpp = CharField(null=True)
    ogrn = CharField(null=True)
    bank_name = CharField(null=True)
    bic = CharField(null=True)
    account = CharField(null=True)
    corr_account = CharField(null=True)
    default = BooleanField(default=True)
    archived = BooleanField(default=False)
    client = ForeignKeyField(Client, related_name=u"client_partner_organizations", null=True)


class ContactPerson(RootObject):

    partner = ForeignKeyField(PartnerOrganization, related_name=u"partner_contact_persons", null=True)


class Artwork(RootObject):

    client = ForeignKeyField(Client, related_name=u"client_artworks", null=True)


class PriceHistory(BaseModel):

    price_type = ForeignKeyField(PriceType, related_name=u"price_type_history")
    start = DateField()
    finish = DateField(null=True)
    value = DecimalField(decimal_places=2, auto_round=True, default=0.0)


class Construction(RootObject):

    district = ForeignKeyField(District, related_name=u"district_constructions", null=True)
    price_type = ForeignKeyField(PriceType, related_name=u"price_type_constructions", null=True)
    installer = ForeignKeyField(Installer, related_name=u"installer_constructions", null=True)
    size = ForeignKeyField(Size, related_name=u"size_constructions", null=True)


class Period(BaseModel):

    construction = ForeignKeyField(Construction, related_name=u"construction_periods", null=True)
    status = ForeignKeyField(ConstructionStatus, related_name=u"construction_status_periods", null=True)
    artwork = ForeignKeyField(Artwork, related_name=u"artwork_periods", null=True)
    partner_organization = ForeignKeyField(PartnerOrganization, related_name=u"partner_organization_periods", null=True)
    contact_person = ForeignKeyField(ContactPerson, related_name=u"contact_person_periods", null=True)
    start = DateField()
    finish = DateField()


class InstallationOrder(BaseModel):

    number = IntegerField(default=0)
    date = DateField()

    @staticmethod
    def get_number():
        last = InstallationOrder.select().order_by(InstallationOrder.number.desc()).first()
        if last:
            return last + 1
        else:
            return 1


class InstallationOrderRow(BaseModel):

    installation_order = ForeignKeyField(InstallationOrder, related_name=u"installation_order_rows")
    artwork_out = ForeignKeyField(Artwork, u"artwork_artworks_out", null=True)
    artwork_in = ForeignKeyField(Artwork, u"artwork_artworks_in", null=True)
    construction = ForeignKeyField(Construction, u"construction_installations", null=True)
    installation_type = ForeignKeyField(InstallationType, u"installation_type_installations", null=True)
    installer = ForeignKeyField(Installer, u"installer_installations", null=True)


class PrintOrder(BaseModel):

    date = DateField()
    partner = ForeignKeyField(PartnerOrganization, related_name=u"partner_organization_print_orders", null=True)
    artwork = ForeignKeyField(Artwork, related_name=u"artwork_print_orders", null=True)
    size = ForeignKeyField(Size, related_name=u"size_print_orders", null=True)
    price_type = ForeignKeyField(PriceType, related_name=u"price_type_print_orders", null=True)
    print_type = ForeignKeyField(InstallationType, related_name=u"print_type_print_orders")
    material = ForeignKeyField(Material, related_name=u"material_print_orders")


class Organization(RootObject):

    full_name = CharField(null=True)
    address = CharField(null=True)
    phones = CharField(null=True)
    email = CharField(null=True)
    inn = CharField(null=True)
    kpp = CharField(null=True)
    ogrn = CharField(null=True)
    bank_name = CharField(null=True)
    bic = CharField(null=True)
    account = CharField(null=True)
    corr_account = CharField(null=True)
    default = BooleanField(default=True)
    archived = BooleanField(default=False)
    first_status = CharField(null=True)
    second_status = CharField(null=True)
    first_name = CharField(null=True)
    second_name = CharField(null=True)


class Invoice(BaseModel):

    date = DateField()
    number = CharField(default="")
    payer = ForeignKeyField(PartnerOrganization, related_name=u"partner_organization_invoices_payer")
    receiver = ForeignKeyField(PartnerOrganization, related_name=u"partner_organization_invoices_receiver", null=True)
    total = DecimalField(default=0)


class InvoiceRow(BaseModel):

    invoice = ForeignKeyField(Invoice, related_name=u"invoice_rows")
    item = ForeignKeyField(PriceType, related_name=u"price_type_invoices_rows", null=True)
    amount = DecimalField(default=0.0)
    price = DecimalField(default=0.0)

    def total(self):
        return self.amount * self.price


def create_tables():
    db.connect()
    db.create_tables(
        [
            Client,
            District,
            Material,
            Installer,
            Size,
            InstallationType,
            PriceType,
            ConstructionStatus,
            PartnerOrganization,
            ContactPerson,
            Artwork,
            PriceHistory,
            Construction,
            Period,
            InstallationOrder,
            InstallationOrderRow,
            PrintOrder,
            Organization,
            Invoice,
            InvoiceRow
        ],
        safe=True
    )


if __name__ == "__main__":
    create_tables()