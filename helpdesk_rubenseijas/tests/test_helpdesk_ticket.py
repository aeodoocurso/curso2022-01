from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestHelpdeskTicket(TransactionCase):

    def setUp(self):
        super(TestHelpdeskTicket, self).setUp()

        # Creacion manual
        #  self.ticket = self.env['helpdesk.ticket'].create({
        #      'name': 'Test Ticket', 'description': 'Test ticket'
        # })
        
        # Creacion con datos demo
        self.ticket = self.env.ref('helpdesk_rubenseijas.demo_admin_ticket')

    def test_time_cannot_be_negative(self):
        self.ticket.time = 3
        self.assertEqual(self.ticket.time, 3)
        self.ticket.time = 8
        self.assertEqual(self.ticket.time, 8)
        with self.assertRaises(ValidationError):
            self.ticket.time = -1