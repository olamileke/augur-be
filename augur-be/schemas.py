from marshmallow import Schema, fields

class UserSchema(Schema):
	id = fields.Integer()
	name = fields.Str()
	email = fields.Email()
	avatar = fields.Str()
	password = fields.Str()
	api_token = fields.Str()
	activation_token = fields.Str()
	created_at = fields.DateTime()