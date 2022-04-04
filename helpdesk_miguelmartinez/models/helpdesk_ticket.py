from odoo import fields, models

class HelpdeskTicket(models.Model):
    _name = "helpdesk.tickets"
    _description = "Helpdesk Tickets"

    name = fields.Char()