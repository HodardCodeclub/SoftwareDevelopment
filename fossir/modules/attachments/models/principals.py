

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
