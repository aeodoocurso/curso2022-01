from odoo import fields,models

class HelpdeskTicketAction(models.Model):
    _name = "helpdesk.ticket.action"
    _description = "Helpdesk Ticket Action"

    sequence = fields.Integer()
    name = fields.Char(required=True)
    description = fields.Text()
    duration = fields.Float()
    ticket_id = fields.Many2one(
        comodel_name="helpdesk.ticket", 
        string="Ticket",
    )
    user_id = fields.Many2one(
        comodel_name="res.users", 
        string="Assigned To",
    )

    def review(self):
        for record in self:
            record.description = '%s\n%s' % (record.description, '- OK') 
