from odoo import api, Command, fields, models, _

class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "Helpdesk Ticket"

    name = fields.Char(required=True, copy=False)
    description = fields.Text()
    sequence = fields.Integer()
    date = fields.Date(help="Date when the ticket was created")
    due_date = fields.Datetime(help="Date and time when the ticket will be closed")
    time = fields.Float(string="Time")
    assigned = fields.Boolean(help="Ticket assigned to someone")
    actions_todo = fields.Html()
    user_id = fields.Many2one(
        comodel_name="res.users", 
        string="Assigned To",
        search="_search_assigned",
        inverse="_set_assigned"
    )
    user_email = fields.Char(
        string="User Email",
        related="user_id.partner_id.email"
    )
    ticket_company = fields.Boolean(string='Ticket Company')
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
    partner_email = fields.Char(
        string="Partner Email",
        related="partner_id.email"
    )
    action_ids = fields.One2many(comodel_name="helpdesk.ticket.action", inverse_name="ticket_id")
    tag_ids = fields.Many2many(
        comodel_name='helpdesk.ticket.tag',  # El otro modelo
        relation="helpdesk_ticket_tag_helpdesk_ticket_rel",  # nombre igual en ambos lados
        column1="ticket_ids",  # Este objeto
        column2="tag_ids",  # El otro objeto
        string='Tags',
    )
    color = fields.Integer('Color Index', default=0)
    tag_name = fields.Char(string="Tag Name")

    def review_actions(self):
        self.ensure_one()
        self.action_ids.review()

    @api.model
    def get_amount_tickets(self):
        # Give amount of ticket for active user
        return self.search_count([('user_id', '=', self.env.user.id)]) 

    def _search_assigned(self, operator, value):
        if operator not in ['=', '!='] or not isinstance(value, bool):
            raise ValueError(_('Operation not supported'))
        if (operator == '=' and value) or (operator != '!=' and not value):
            new_operator = '!='
        else:
            new_operator = '='
        return [('user_id', new_operator, False)]

    def _set_assigned(self):
        for record in self:
            if not record.assigned:
                record.user_id = False
            elif not record.user_id:   
                record.user_id = self.env.user

    def create_and_link_tag(self):
        self.ensure_one()

        # crear ticket y asignar
        # tag = self.env['helpdesk.ticket.tag'].create({'name': self.tag_name})
        # self.write({'tag_ids': [(4, tag.id, 0)]})
        # self.write({'tag_ids': [Command.link(tag.id)]})

        # crear el ticket desde escritura tag_ids
        # self.write({
        #     'tag_ids': [(0, 0, {'name': self.tag_name})],
        #     'tag_name': False
        # })

        # crear tag asociado al ticket
        self.env['helpdesk.ticket.tag'].create({
            'name': self.tag_name,
            'ticket_ids': [(4, self.id, 0)],  # [(6, 0, self.ids)] or [(4, self.id, {'name': self.tag_name})] or [Command.set(self.ids)]
        })
        self.write({'tag_name': False})


