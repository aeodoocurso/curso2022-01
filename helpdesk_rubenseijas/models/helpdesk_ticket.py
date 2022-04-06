from odoo import fields,models

class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "Helpdesk Ticket"

    name = fields.Char(required=True)
    description = fields.Text()
    sequence = fields.Integer()
    date = fields.Date(help="Date when the ticket was created")
    limit_date = fields.Datetime(help="Date and time when the ticket will be closed")
    assigned= fields.Boolean(help="Ticket assigned to someone", readonly=True)
    actions_todo = fields.Html()
    user_id = fields.Many2one(comodel_name="res.users", string="Assigned To")
    state = fields.Selection(
        [('nuevo', 'Nuevo'),
        ('asignado', 'Asignado'),
        ('en_proceso', 'En Proceso'),
        ('pendiente', 'Pendiente'),
        ('resuelto', 'Resuelto'),
        ('cancelado', 'Cancelado')],
        string="State", default="nuevo"
    )

