from odoo import fields,models,api

class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "Helpdesk ticket"
    _order = "sequence"

    name = fields.Char(required=True)
    description = fields.Text(translatable=True)
    date = fields.Date()
    limit_date = fields.Date()
    assigned = fields.Boolean(help="Ticket assigned to someone",readonly=True)
    actions_todo = fields.Html()
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assigned to'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner'
    )
    sequence = fields.Integer()
    state = fields.Selection(
        [('nuevo', 'Nuevo'),
         ('asignado', 'Asignado'),
         ('en_proceso', 'En proceso'),
         ('pendiente', 'Pendiente'),
         ('resuelto', 'Resuelto'),
         ('cancelado', 'Cancelado')],
        string='State',
        default='nuevo')
    actions_ids = fields.One2many(
        comodel_name="helpdesk.ticket.action",
        inverse_name="ticket.id",
        string="Actions done"
    )
    tag_ids = fields.Many2many(
        comodel_name = "helpdesk.ticket.tag",
        string = "Tags"
    )

    def to_asignado(self):
        self.ensure_one()
        self.state='asignado'

    def to_en_proceso(self):
        self.write({'state':'en_proceso'})

    def to_pendiente(self):
        for record in self:
            record.state='pendiente'

    def review_actions(self):
        self.ensure_one()
        self.action_ids.review()
    
    '''''
    @api.model
    def get_amount_tickets(self):
        return self.search_count()

    '''''