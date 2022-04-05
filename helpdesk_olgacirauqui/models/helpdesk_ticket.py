from odoo import fields,models

class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "Helpdesk Ticket"

    name = fields.Char()
    description = fields.Text()
    date = fields.Date(help="Date when the ticket was created")
    limit_date = fields.Datetime(help="Date and time when the ticket will be closed")
    assigned= fields.Boolean(help="Ticket assigned to someone")
    actions_todo = fields.Html()
    user_id = fields.Many2one(comodel_name ='res.users',string='Assign to')
    sequence = fields.Integer()
    state =fields.Selection(
        [
        ('nuevo', 'Nuevo'),
        ('asignado', 'Asignado'),
        ('en proceso', 'En proceso'),
        ('pendiente', 'Pendiente'),
        ('resuelto', 'Resuelto'),
        ('cancelado', 'Cancelado')
        ],
        string="State",
        default='nuevo'
    )