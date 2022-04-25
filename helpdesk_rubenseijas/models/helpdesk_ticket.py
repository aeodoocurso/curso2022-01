from odoo import api, fields, models

class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "Helpdesk Ticket"

    name = fields.Char(required=True)
    description = fields.Text()
    sequence = fields.Integer()
    date = fields.Date(help="Date when the ticket was created")
    due_date = fields.Datetime(help="Date and time when the ticket will be closed")
    time = fields.Float(string="Time")
    assigned = fields.Boolean(help="Ticket assigned to someone", readonly=True)
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
    partner_id = fields.Many2one("res.partner", "Customer")
    action_ids = fields.One2many(comodel_name="helpdesk.ticket.action", inverse_name="ticket_id")
    tag_ids = fields.Many2many(comodel_name='helpdesk.ticket.tag', string='Ticket Tags')
    color = fields.Integer('Color Index')

    def review_actions(self):
        self.ensure_one()
        self.action_ids.review()

    @api.model
    def get_amount_tickets(self):
        # Give amount of ticket for active user
        return self.search_count([('user_id', '=', self.env.user.id)]) 
