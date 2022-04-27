from odoo import fields,models

class HelpdeskTicketTag(models.Model):
    _name = "helpdesk.ticket.tag"
    _description = "Helpdesk Ticket Tag"

    name = fields.Char(required=True)
    description = fields.Text()
    ticket_ids = fields.Many2many(
        comodel_name='helpdesk.ticket',  # El otro modelo
        relation="helpdesk_ticket_tag_helpdesk_ticket_rel",  # nombre igual en ambos lados
        column1="tag_ids",  # Este objeto
        column2="ticket_ids",  # El otro objeto
        string='Tickets',
    )