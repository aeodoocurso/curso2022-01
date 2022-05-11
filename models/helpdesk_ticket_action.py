from odoo import fields,models

class HelpdeskTicketAction(models.Model):
    _name = "helpdesk.ticket.action"
    _description = "Helpdesk ticket action"
    _order = "sequence"

    name = fields.Char(required=True)
    description = fields.Text()
    duration = fields.Float()
    sequence = fields.Integer()
    ticket_id=fields.Many2one(
        comodel_name="helpdesk.ticket"
    )

    def review(self):
        for record in self:
            record.description = '%s\n%s' % (record.description, 'OK')