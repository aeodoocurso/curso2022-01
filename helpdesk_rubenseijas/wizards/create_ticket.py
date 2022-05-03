from email.policy import default
from odoo import api, fields, models, Command

class CreateTicket(models.TransientModel):
    _name = "create.ticket"
    _description = "Create Ticket Action"

    @api.model
    def _get_default_tags(self):
        if self.env.context.get('active_model') == 'helpdesk.ticket.tag':
            return [Command.set(self.env.context.get('active_ids'))]
        return False

    name = fields.Char()
    tag_ids = fields.Many2many(
        comodel_name='helpdesk.ticket.tag', string='Tags', 
        default=_get_default_tags,
    )

    def get_ticket_values(self):
        return {
            'name': self.name,
            'tag_ids': [(4, self.id, 0)],  # [Command.set(self.ids)]
        }

    def create_tickets(self):
        self.ensure_one()
        # Los valores los pasamos por método para poder heredar y cambiarlos
        values = self.get_ticket_values()
        new_ticket = self.env['helpdesk.ticket'].create(values)
        action = self.env["ir.actions.actions"]._for_xml_id("helpdesk_rubenseijas.helpdesk_ticket_action_all")
        action['views'] = [(self.env.ref('helpdesk_rubenseijas.view_helpdesk_tickets_form').id, 'form')]
        action['res_id'] = new_ticket.id
        return action