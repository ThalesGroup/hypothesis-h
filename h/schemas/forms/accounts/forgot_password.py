# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import colander
import deform

from h import i18n, models, validators
from h.schemas.base import CSRFSchema

_ = i18n.TranslationString


class ForgotPasswordSchema(CSRFSchema):
    email = colander.SchemaNode(
        colander.String(),
        validator=colander.All(validators.Email()),
        title=_('Email address'),
        widget=deform.widget.TextInputWidget(template='emailinput',
                                             autofocus=True),
    )

    def validator(self, node, value):
        super(ForgotPasswordSchema, self).validator(node, value)

        request = node.bindings['request']
        email = value.get('email')
        user = models.User.get_by_email(request.db, email, request.authority)

        if user is None:
            err = colander.Invalid(node)
            err['email'] = _('Unknown email address.')
            raise err

        value['user'] = user
