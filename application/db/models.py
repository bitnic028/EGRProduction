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


class User(BaseModel):

    login = CharField(unique=True)
    password = CharField()
    is_admin = BooleanField(default=False)
    is_active = BooleanField(default=True)

    def get_dict(self):
        return {
            "id": self.id,
            "login": self.login,
            "is_admin": self.is_admin,
            "is_active": self.is_active
        }


class RootObject(BaseModel):

    name = CharField()


class Client(RootObject):

    last_name = CharField(null=True)
    account = ForeignKeyField(User, related_name=u"user_client", null=True)

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name if self.last_name else False,
            "account": self.account.get_dict() if self.account else False
        }


class District(RootObject):

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Material(RootObject):

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Installer(RootObject):

    last_name = CharField(null=True)

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name if self.last_name else False
        }


class Size(RootObject):

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class InstallationType(RootObject):

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class ConstructionType(RootObject):

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


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

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_for_invoice": self.name_for_invoice,
            "measurement": self.measurement
        }


class ConstructionStatus(RootObject):

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


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
    archived = BooleanField(default=False)
    client = ForeignKeyField(Client, related_name=u"client_partner_organizations", null=True)

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name if self.full_name else u"",
            "address": self.address if self.address else u"",
            "phones": self.phones if self.phones else u"",
            "email": self.email if self.email else u"",
            "inn": self.inn if self.inn else u"",
            "kpp": self.kpp if self.kpp else u"",
            "ogrn": self.ogrn if self.ogrn else u"",
            "bank_name": self.bank_name if self.bank_name else u"",
            "bic": self.bic if self.bic else u"",
            "account": self.account if self.account else u"",
            "corr_account": self.corr_account if self.corr_account else u"",
            "archived": self.archived,
            "client": self.client.get_dict() if self.client else False
        }


class ContactPerson(RootObject):

    last_name = CharField(null=True)
    phone = CharField(null=True)
    mail = CharField(null=True)
    partner = ForeignKeyField(PartnerOrganization, related_name=u"partner_contact_persons", null=True)

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name if self.last_name else u"",
            "phone": self.phone if self.phone else u"",
            "mail": self.mail if self.mail else u"",
            "partner": self.partner.get_dict() if self.partner else False
        }


class Artwork(RootObject):

    place = CharField(null=True)
    client = ForeignKeyField(Client, related_name=u"client_artworks", null=True)
    image = CharField(null=True)
    start = DateField(null=True)
    finish = DateField(null=True)
    action_date = DateField(null=True)

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "place": self.place if self.place else u"",
            "client": self.client.get_dict() if self.client else False,
            "image": self.image if self.image else u"",
            "start": helpers.string_from_date(self.start, u"short2") if self.start else False,
            "finish": helpers.string_from_date(self.finish, u"short2") if self.finish else False,
            "action_date": helpers.string_from_date(self.action_date, u"short2") if self.action_date else False
        }


class PriceHistory(BaseModel):

    price_type = ForeignKeyField(PriceType, related_name=u"price_type_history")
    start = DateField()
    finish = DateField(null=True)
    value = DecimalField(decimal_places=2, auto_round=True, default=0.0)

    def get_dict(self):
        return {
            "id": self.id,
            "price_type": self.price_type.get_dict(),
            "start": helpers.string_from_date(self.start, u"short2") if self.start else False,
            "finish": helpers.string_from_date(self.finish, u"short2") if self.finish else False,
            "value": float(self.value)
        }


class Construction(RootObject):

    construction_type = ForeignKeyField(ConstructionType, related_name=u"construction_type_constructions", null=True)
    district = ForeignKeyField(District, related_name=u"district_constructions", null=True)
    price_type = ForeignKeyField(PriceType, related_name=u"price_type_constructions", null=True)
    installer = ForeignKeyField(Installer, related_name=u"installer_constructions", null=True)
    size = ForeignKeyField(Size, related_name=u"size_constructions", null=True)
    number = TextField(null=True)
    color = TextField(null=True)
    address = TextField()

    def get_dict(self):
        return {
            "id": self.id,
            "construction_type": self.construction_type.get_dict() if self.construction_type else False,
            "district": self.district.get_dict() if self.district else False,
            "price_type": self.price_type.get_dict() if self.price_type else False,
            "installer": self.installer.get_dict() if self.installer else False,
            "size": self.size.get_dict() if self.size else False,
            "number": self.number if self.number else "",
            "color": self.color if self.color else "",
            "address": self.address if self.address else "",
        }


class Period(BaseModel):

    construction = ForeignKeyField(Construction, related_name=u"construction_periods", null=True)
    status = ForeignKeyField(ConstructionStatus, related_name=u"construction_status_periods", null=True)
    artwork = ForeignKeyField(Artwork, related_name=u"artwork_periods", null=True)
    partner_organization = ForeignKeyField(PartnerOrganization, related_name=u"partner_organization_periods", null=True)
    contact_person = ForeignKeyField(ContactPerson, related_name=u"contact_person_periods", null=True)
    start = DateField()
    finish = DateField()

    def get_dict(self):
        return {
            "id": self.id,
            "construction": self.construction.get_dict() if self.construction else False,
            "status": self.status.get_dict() if self.status else False,
            "artwork": self.artwork.get_dict() if self.artwork else False,
            "partner_organization": self.partner_organization.get_dict() if self.partner_organization else False,
            "contact_person": self.contact_person.get_dict() if self.contact_person else False,
            "start": helpers.string_from_date(self.start, u"short2") if self.start else False,
            "finish": helpers.string_from_date(self.finish, u"short2") if self.finish else False
        }


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

    def get_dict(self):
        return {
            "id": self.id,
            "date": helpers.string_from_date(self.date, u"short2") if self.date else False,
            "number": self.number
        }


class InstallationOrderRow(BaseModel):

    installation_order = ForeignKeyField(InstallationOrder, related_name=u"installation_order_rows")
    artwork_out = ForeignKeyField(Artwork, u"artwork_artworks_out", null=True)
    artwork_in = ForeignKeyField(Artwork, u"artwork_artworks_in", null=True)
    construction = ForeignKeyField(Construction, u"construction_installations", null=True)
    installation_type = ForeignKeyField(InstallationType, u"installation_type_installations", null=True)
    installer = ForeignKeyField(Installer, u"installer_installations", null=True)
    photo_report = TextField(null=True)

    def get_dict(self):
        return {
            "id": self.id,
            "installation_order": self.installation_order.get_dict() if self.installation_order else False,
            "artwork_out": self.artwork_out.get_dict() if self.artwork_out else False,
            "artwork_in": self.artwork_in.get_dict() if self.artwork_in else False,
            "construction": self.construction.get_dict() if self.construction else False,
            "installation_type": self.installation_type.get_dict() if self.installation_type else False,
            "installer": self.installer.get_dict() if self.installer else False,
            "photo_report": self.photo_report if self.photo_report else ""
        }


class PrintOrder(BaseModel):

    date = DateField()
    partner = ForeignKeyField(PartnerOrganization, related_name=u"partner_organization_print_orders", null=True)
    artwork = ForeignKeyField(Artwork, related_name=u"artwork_print_orders", null=True)
    size = ForeignKeyField(Size, related_name=u"size_print_orders", null=True)
    price_type = ForeignKeyField(PriceType, related_name=u"price_type_print_orders", null=True)
    print_type = ForeignKeyField(InstallationType, related_name=u"print_type_print_orders")
    material = ForeignKeyField(Material, related_name=u"material_print_orders")
    amount = IntegerField(default=0)

    def get_dict(self):
        return {
            "id": self.id,
            "date": helpers.string_from_date(self.date, u"short2") if self.date else False,
            "partner": self.partner.get_dict() if self.partner else False,
            "artwork": self.artwork.get_dict() if self.artwork else False,
            "size": self.size.get_dict() if self.size else False,
            "price_type": self.price_type.get_dict() if self.price_type else False,
            "print_type": self.print_type.get_dict() if self.print_type else False,
            "material": self.material.get_dict() if self.material else False,
            "amount": self.amount.get_dict() if self.amount else False
        }


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

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name if self.full_name else u"",
            "address": self.address if self.address else u"",
            "phones": self.phones if self.phones else u"",
            "email": self.email if self.email else u"",
            "inn": self.inn if self.inn else u"",
            "kpp": self.kpp if self.kpp else u"",
            "ogrn": self.ogrn if self.ogrn else u"",
            "bank_name": self.bank_name if self.bank_name else u"",
            "bic": self.bic if self.bic else u"",
            "account": self.account if self.account else u"",
            "corr_account": self.corr_account if self.corr_account else u"",
            "default": self.default,
            "archived": self.archived,
            "first_status": self.first_status if self.first_status else u"",
            "second_status": self.second_status if self.second_status else u"",
            "first_name": self.first_name if self.first_name else u"",
            "second_name": self.second_name if self.second_name else u""
        }


class Invoice(BaseModel):

    date = DateField()
    number = CharField(default="")
    payer = ForeignKeyField(PartnerOrganization, related_name=u"partner_organization_invoices_payer")
    receiver = ForeignKeyField(PartnerOrganization, related_name=u"partner_organization_invoices_receiver", null=True)
    total = DecimalField(decimal_places=2, auto_round=True, default=0.0)

    def get_dict(self):
        return {
            "id": self.id,
            "date": helpers.string_from_date(self.date, u"short2") if self.date else False,
            "number": self.number,
            "payer": self.payer.get_dict(),
            "receiver": self.receiver.get_dict() if self.receiver else False,
            "total": float(self.total)
        }


class InvoiceRow(BaseModel):

    invoice = ForeignKeyField(Invoice, related_name=u"invoice_rows")
    item = ForeignKeyField(PriceType, related_name=u"price_type_invoices_rows", null=True)
    amount = DecimalField(decimal_places=2, auto_round=True, default=0.0)
    price = DecimalField(decimal_places=2, auto_round=True, default=0.0)

    def total(self):
        return float(self.amount * self.price)

    def get_dict(self):
        return {
            "id": self.id,
            "invoice": self.invoice.get_dict(),
            "item": self.item.get_dict() if self.item else False,
            "amount": float(self.amount),
            "price": float(self.price),
            "total": self.total()
        }


def create_tables():
    db.connect()
    db.create_tables(
        [
            User,
            Client,
            District,
            Material,
            Installer,
            Size,
            InstallationType,
            ConstructionType,
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

OBJECTS_TYPES = {
    "User": User,
    "Client": Client,
    "District": District,
    "Material": Material,
    "Installer": Installer,
    "Size": Size,
    "InstallationType": InstallationType,
    "ConstructionType": ConstructionType,
    "PriceType": PriceType,
    "ConstructionStatus": ConstructionStatus,
    "PartnerOrganization": PartnerOrganization,
    "ContactPerson": ContactPerson,
    "Artwork": Artwork,
    "PriceHistory": PriceHistory,
    "Construction": Construction,
    "Period": Period,
    "InstallationOrder": InstallationOrder,
    "InstallationOrderRow": InstallationOrderRow,
    "PrintOrder": PrintOrder,
    "Organization": Organization,
    "Invoice": Invoice,
    "InvoiceRow": InvoiceRow,
}

if __name__ == "__main__":
    create_tables()