from odoo import fields,models

class HelpdeskTicketAction(models.Model):
    _name = "helpdesk.ticket.action"
    _description = "Helpdesk Ticket Action"

    name = fields.Char(required=True)
    description = fields.Text()
    dedicated_time = fields.Datetime()
    ticket_id = fields.Many2one("helpdesk.ticket", "Ticket")
    user_id = fields.Many2one(
        comodel_name="res.users", 
        string="Assigned To",
    )

    def review(self):
        for record in self:
            record.description = '%s\n%s' % (record.description, '- OK') 
