from odoo import api, fields, models, Command

class HelpdeskTicketTag(models.Model):
    _name = "helpdesk.ticket.tag"
    _description = "Helpdesk Ticket Tag"

    @api.model
    def _get_default_tickets(self):
        # En los casos Many2many se puede intentar devolver por contexto el ticket asociado
        if self.env.context.get('active_model') == 'helpdesk.ticket':
            return [Command.set(self.env.context.get('active_ids'))]
        return False

    name = fields.Char(required=True)
    description = fields.Text()
    ticket_ids = fields.Many2many(
        comodel_name='helpdesk.ticket',  # El otro modelo
        relation="helpdesk_ticket_tag_helpdesk_ticket_rel",  # nombre igual en ambos lados
        column1="tag_ids",  # Este objeto
        column2="ticket_ids",  # El otro objeto
        string='Tickets',
        default=_get_default_tickets
    )

    @api.model
    def _clean_unused_tags(self):
        unused_tags = self.search([('ticket_ids', '=', False)])
        unused_tags.unlink()
