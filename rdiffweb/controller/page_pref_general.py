# -*- coding: utf-8 -*-
# rdiffweb, A web interface to rdiff-backup repositories
# Copyright (C) 2012-2021 rdiffweb contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Default preference page to show general user information. It allows user
to change password ans refresh it's repository view.
"""

import logging
import re

import cherrypy
from wtforms.fields import HiddenField, PasswordField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, InputRequired, Length, Optional, Regexp

from rdiffweb.controller import Controller, flash
from rdiffweb.controller.form import CherryForm
from rdiffweb.tools.i18n import gettext_lazy as _

# Define the logger
_logger = logging.getLogger(__name__)




class UserPasswordForm(CherryForm):
    action = HiddenField(default='set_password')
    current = PasswordField(
        _('Current password'),
        validators=[InputRequired(_("Current password is missing."))],
        description=_("You must provide your current password in order to change it."),
    )
    new = PasswordField(
        _('New password'),
        validators=[
            InputRequired(_("New password is missing.")),
            EqualTo('confirm', message=_("The new password and its confirmation do not match.")),
        ],
    )
    confirm = PasswordField(
        _('Confirm new password'), validators=[InputRequired(_("Confirmation password is missing."))]
    )
    set_password = SubmitField(_('Update password'))

    def is_submitted(self):
        # Validate only if action is set_profile_info
        return super().is_submitted() and self.action.data == 'set_password'

    def populate_obj(self, user):
        try:
            user.set_password(self.new.data, old_password=self.current.data)
            flash(_("Password updated successfully."), level='success')
        except ValueError as e:
            flash(str(e), level='warning')


class RefreshForm(CherryForm):
    action = HiddenField(default='update_repos')
    update_repos = SubmitField(
        _('Refresh repositories'),
        description=_(
            "Refresh the list of repositories associated to your account. If you recently add a new repository and it doesn't show, you may try to refresh the list."
        ),
    )

    def is_submitted(self):
        # Validate only if action is set_profile_info
        return super().is_submitted() and self.action.data == 'update_repos'

    def populate_obj(self, user):
        try:
            user.refresh_repos(delete=True)
            flash(_("Repositories successfully updated"), level='success')
        except ValueError as e:
            flash(str(e), level='warning')



