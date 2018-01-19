# This file is part of fossir.
# Copyright (C) 2002 - 2017 European Organization for Nuclear Research (CERN).
#
# fossir is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# fossir is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fossir; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from sqlalchemy.ext.declarative import declared_attr

from fossir.core.db import db
from fossir.core.db.sqlalchemy.principals import PrincipalMixin
from fossir.core.db.sqlalchemy.util.models import auto_table_args
from fossir.util.string import return_ascii


class AttachmentFolderPrincipal(PrincipalMixin, db.Model):
    __tablename__ = 'folder_principals'
    principal_backref_name = 'in_attachment_folder_acls'
    unique_columns = ('folder_id',)

    @declared_attr
    def __table_args__(cls):
        return auto_table_args(cls, schema='attachments')

    #: The ID of the acl entry
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    #: The ID of the associated folder
    folder_id = db.Column(
        db.Integer,
        db.ForeignKey('attachments.folders.id'),
        nullable=False
    )

    # relationship backrefs:
    # - folder (AttachmentFolder.acl_entries)

    @return_ascii
    def __repr__(self):
        return '<AttachmentFolderPrincipal({}, {}, {})>'.format(self.id, self.folder_id, self.principal)


class AttachmentPrincipal(PrincipalMixin, db.Model):
    __tablename__ = 'attachment_principals'
    principal_backref_name = 'in_attachment_acls'
    unique_columns = ('attachment_id',)

    @declared_attr
    def __table_args__(cls):
        return auto_table_args(cls, schema='attachments')

    #: The ID of the acl entry
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    #: The ID of the associated attachment
    attachment_id = db.Column(
        db.Integer,
        db.ForeignKey('attachments.attachments.id'),
        nullable=False
    )

    # relationship backrefs:
    # - attachment (Attachment.acl_entries)

    @return_ascii
    def __repr__(self):
        return '<AttachmentPrincipal({}, {}, {})>'.format(self.id, self.attachment_id, self.principal)