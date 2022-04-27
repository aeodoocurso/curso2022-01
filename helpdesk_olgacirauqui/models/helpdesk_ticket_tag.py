from odoo import fields,models

class HelpdeskTicketTag(models.Model):
    _name = "helpdesk.ticket.tag"
    _description = "Helpdesk Ticket Action"
   

    name = fields.Char()
    description = fields.Text()
    ticket_ids = fields.Many2many(
        comodel_name = "helpdesk.ticket",
        relation = 'helpdesk_ticket_tag_rel',
        column1 = 'ticket_id',
        column2 = 'tag_id',
       string ="Tags"
        
    )
   