from odoo import api,fields,models

class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "Helpdesk Ticket"

    name = fields.Char()
    description = fields.Text(translate=True)
    date = fields.Date(help="Date when the ticket was created")
    limit_date = fields.Datetime(help="Date and time when the ticket will be closed")
    assigned= fields.Boolean(help="Ticket assigned to someone")
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
