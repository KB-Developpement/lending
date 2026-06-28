from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

from lending.install import LOAN_CUSTOM_FIELDS


def execute():
	create_custom_fields(LOAN_CUSTOM_FIELDS, ignore_validate=True)
