from odoo import fields,models

class HelpdeskTicketTag(models.Model):
    _name = "helpdesk.ticket.tag"
    _description = "Helpdesk Ticket Action"
   

    name = fields.Char()
    description = fields.Text()
   