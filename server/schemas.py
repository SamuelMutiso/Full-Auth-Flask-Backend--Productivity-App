from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)


user_schema = UserSchema()