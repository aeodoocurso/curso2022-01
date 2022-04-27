from dataclasses import field
from odoo import api,fields,models

class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "Helpdesk Ticket"

    name = fields.Char()
    description = fields.Text(translate=True)
    color = fields.Integer('Color Index', default=0)
    date = fields.Date(help="Date when the ticket was created")
    date_start = fields.Datetime()
    date_end = fields.Datetime()
    limit_date = fields.Datetime(help="Date and time when the ticket will be closed")
    time = fields.Float(string='Time')
    assigned= fields.Boolean(
        help="Ticket assigned to someone", 
        compute="_compute_assigned",
        search='_search_assigned',
        inverse = "_set_assigned")
    actions_todo = fields.Html()
    user_id = fields.Many2one(comodel_name ='res.users',string='Assigned to')
    partner_id = fields.Many2one(
        comodel_name = "res.partner",
        string ="Partner"
    )
    sequence = fields.Integer()
    action_ids = fields.One2many(
        comodel_name = "helpdesk.ticket.action",
        inverse_name="ticket_id",
        string="Actions done"
    )
    tag_name =fields.Char(string = 'Tag name')
    tag_ids = fields.Many2many(
        comodel_name = "helpdesk.ticket.tag",
       # relation = 'table_name',
       # column1 = 'col_name',
       # column2 
       string ="Tags"
        
    )
    

    #poner una o varias etiquetas

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
    #crear funciones
    def to_asignado(self):
        self.ensure_one()##se ejecuta esta función sólo para un objeto
        self.state = 'asignado'
    
    def to_en_proceso(self):
        ##ejecutar sobre varios objetos a la vez
        self.write({'state':'en proceso'})

    def to_en_pendiente(self):
        ##ejecutar sobre varios objetos a la vez
        self.write({'state':'pendiente'})

    def review_actions(self):
        self.ensure_one()
        self.action_ids.review()

    @api.model
    def get_amount_ticket(self):
        #dev
        return self.search_count([('user_id' '=', self.env.user.id)])
    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            record.assigned = record.user_id
    
    def _search_assigned (self, operator, value):
        if operator not in ['=', '!='] or not isinstance(value, bool):
            raise UserError(_('Operation not supported'))
        if (operator == '=' and value) or (operator == '!=' and not value):
            new_operator = '!='
        else:
            new_operator = '='
        return [('user_id', new_operator, False)]

    def _set_assigned(self):
        for record in self:
            if record.assigned:
                record.user_id = self.env.user
            else:
                record.user_id = False
    def create_and_link_tag(self):
        self.ensure_one()
        tag = self.env['helpdesk.ticket.tag'].create({'name': self.tag_name})
        self.write({'tag_ids':[(0,0, {'name': self.tag_name})]})