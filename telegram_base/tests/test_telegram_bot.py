# Copyright 2026 Anmol Garg
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from unittest.mock import patch
from odoo.tests.common import TransactionCase
import requests


class TestTelegramBot(TransactionCase):

    def setUp(self):
        super().setUp()
        # Create a test bot
        self.bot = self.env['telegram.bot'].create({
            'name': 'Test Bot',
            'token': '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11',
        })
        # Create a test chat linked to the bot
        self.chat = self.env['telegram.chat'].create({
            'name': 'Anmol Test Chat',
            'chat_id': '1856618864',
            'bot_id': self.bot.id,
        })

    @patch('requests.Session.post')
    def test_send_message_success(self, mock_post):
        """Test a successful message delivery"""
        # Mock a successful 200 response
        mock_post.return_value.status_code = 200
        mock_post.return_value.raise_for_status = lambda: None

        result = self.bot.send_message(self.chat.chat_id, "Hello from Odoo Test")

        self.assertTrue(result, "The send_message method should return True on success")
        self.assertEqual(mock_post.call_count, 1, "Exactly one POST request should be made")

    @patch('requests.Session.post')
    def test_send_message_failure(self, mock_post):
        """Test handling of a connection failure"""
        # Simulate a real exception (like a timeout or DNS error)
        # This will trigger the 'except' block in your telegram_bot.py
        mock_post.side_effect = requests.exceptions.RequestException("Connection Failed")

        result = self.bot.send_message(self.chat.chat_id, "This should fail")

        # This should now correctly return False
        self.assertFalse(result, "The send_message method should return False on exception")

    @patch('requests.get')
    def test_action_fetch_chats(self, mock_get):
        """Test fetching chats from Telegram API"""
        # Mock the JSON response from Telegram /getUpdates
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "ok": True,
            "result": [{
                "update_id": 1,
                "message": {
                    "chat": {"id": 111222, "first_name": "NewUser", "type": "private"},
                    "text": "hi"
                }
            }]
        }

        self.bot.action_fetch_chats()

        # Verify a new chat was created in Odoo
        new_chat = self.env['telegram.chat'].search([('chat_id', '=', '111222')])
        self.assertTrue(new_chat, "A new chat should have been created from the mock data")
        self.assertEqual(new_chat.name, "NewUser")