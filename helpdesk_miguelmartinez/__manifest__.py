# Copyright 2022 Miguel Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "helpdesk_miguelmartinez",
    "summary": "Task from Odoo course",
    "version": "15.0.1.0.0",
    "author": "Miguel",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "preloadable": True,
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
    "post_load": "post_load",
    "uninstall_hook": "uninstall_hook",
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base",
    ],

}