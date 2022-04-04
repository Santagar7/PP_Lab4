from marshmallow import Schema, fields


class FamilySchema(Schema):
    id = fields.Integer()
    name = fields.String()


class FamilyMembersSchema(Schema):
    id = fields.Integer()
    login = fields.String()
    password = fields.String()
    familyId = fields.Integer()
    firstname = fields.String()
    lastname = fields.String()
    role = fields.String()
    birthdate = fields.Date()


class CostsSchema(Schema):
    id = fields.Integer()
    familyMemId = fields.Integer()
    familyId = fields.Integer()
    purpose = fields.String()
    amount = fields.Float()
    time = fields.DateTime()


class ProfitsSchema(Schema):
    id = fields.Integer()
    familyMemId = fields.Integer()
    familyId = fields.Integer()
    amount = fields.Float()
    time = fields.DateTime()