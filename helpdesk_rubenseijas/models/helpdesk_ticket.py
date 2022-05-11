from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _

from odoo.exceptions import ValidationError

class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "Helpdesk Ticket"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _get_default_user(self):
        return self.env.user

    name = fields.Char(required=True, copy=False)
    description = fields.Text()
    sequence = fields.Integer()
    date = fields.Date(help="Date when the ticket was created", default=fields.datetime.now().date())
    date_start = fields.Datetime()
    limit_date = fields.Datetime(help="Date and time when the ticket will be closed")
    time = fields.Float(string="Time")
    assigned = fields.Boolean(
        help="Ticket assigned to someone",
        compute='_compute_assigned',
        search='_search_assigned',
        inverse='_set_assigned',
    )
    actions_todo = fields.Html()
    user_id = fields.Many2one(
        comodel_name="res.users", 
        string="Assigned To",
        default=_get_default_user,  # default=lambda self: self.env.user,
        tracking=True,
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
        string="State", 
        default="nuevo",
    )
    partner_id = fields.Many2one("res.partner", "Customer")
    partner_email = fields.Char(
        string="Partner Email",
        related="partner_id.email"
    )
    action_ids = fields.One2many(comodel_name="helpdesk.ticket.action", inverse_name="ticket_id")
    tag_name = fields.Char(string="Tag Name")
    tag_ids = fields.Many2many(
        comodel_name='helpdesk.ticket.tag',  # El otro modelo
        relation="helpdesk_ticket_tag_helpdesk_ticket_rel",  # nombre igual en ambos lados
        column1="ticket_ids",  # Este objeto
        column2="tag_ids",  # El otro objeto
        string='Tags',
    )
    color = fields.Integer('Color Index', default=0)

    def to_asignado(self):
        self.ensure_one()
        self.state = 'asignado'
    
    def to_en_proceso(self):
        self.write({'state': 'en_proceso'})
    
    def to_pendiente(self):
        for record in self:
            record.state = 'pendiente'

    @api.constrains('time')
    def _check_time(self):
        # Método tradicional
    #    for ticket in self:
    #        if ticket.time < 0:
    #            raise ValidationError(_("The time have to be positive."))

        # Más efectivo si dentro del for hay un if y el código todo dentro del if
        # for ticket in self.filtered(lambda x: x.time > 0):
        #    raise ValidationError(_("The time have to be positive."))

        # No hace ni falta hacer el for
        if self.filtered(lambda x: x.time < 0):
           raise ValidationError(_("The time have to be positive."))

    @api.onchange('date_start')
    def _onchange_date_start(self):
        if self.date_start:
            self.limit_date = self.date_start + timedelta(days=1)
        else:
            self.limit_date = False

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

    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            record.assigned = record.user_id

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
