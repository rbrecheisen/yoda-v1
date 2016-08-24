import flask
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, validates
from sqlalchemy_utils import PasswordType, force_auto_coercion
from lib.models import Base, BaseModel

force_auto_coercion()

UserGroupUsers = Table(
    'user_group_users', Base.metadata,
    Column('user_group_id', Integer, ForeignKey('user_group.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)


# ----------------------------------------------------------------------------------------------------------------------
class Principal(BaseModel):

    __tablename__ = 'principal'

    # User ID in database
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # Principal type
    principal_type = Column(String(64))

    __mapper_args__ = {
        'polymorphic_identity': 'principal',
        'polymorphic_on': principal_type,
    }

    def has_permission(self, permission):
        # Get action and resource info from permission string
        resource_id = None
        action, resource_class = permission.split(':')
        if '@' in resource_class:
            resource_class, resource_id = resource_class.split('@')
        # First check class-level access. If granted, we need check no further.
        for p in self.permissions:
            if p.resource_id == resource_class:
                if p.action == action or p.action == 'all':
                    # Permission may have been denied so return 'granted'
                    return p.granted
            # If resource IDs were provided, check if they match
            if resource_id:
                if p.resource_id == '{}@{}'.format(resource_class, resource_id):
                    if p.action == action or p.action == 'all':
                        # Permission granted
                        return p.granted
        # All failed, return False
        return False

    def to_dict(self):
        obj = super(Principal, self).to_dict()
        obj.update({
            'permissions': self.permissions
        })
        return obj


# ----------------------------------------------------------------------------------------------------------------------
class User(Principal):

    __tablename__ = 'user'
    __mapper_args__ = {
        'polymorphic_identity': 'user',
    }

    # User ID in database
    id = Column(Integer, ForeignKey('principal.id'), primary_key=True)
    # User name
    username = Column(String(64), nullable=False, unique=True, index=True)
    # User (hashed) password
    password = Column(PasswordType(
        onload=lambda **kwargs: dict(
            schemes=flask.current_app.config['PASSWORD_SCHEMES'], **kwargs)
    ), nullable=False, unique=False)
    # User email address
    email = Column(String(255), nullable=False, unique=True, index=True)
    # User first name
    first_name = Column(String(255))
    # User last name
    last_name = Column(String(255))
    # Flag indicating if user is super user
    is_superuser = Column(Boolean, default=False)
    # Flag indicating user is administrator
    is_admin = Column(Boolean, default=False)
    # Flag indicating if user is active. User instead of deleting.
    is_active = Column(Boolean, default=True)

    def has_permission(self, permission):
        # If user is staff or even superuser, grant permission
        if self.is_admin or self.is_superuser:
            return True
        # Then check if user herself has permission. If not, continue with
        # her group memberships
        if super(User, self).has_permission(permission):
            return True
        # Check group membership permissions
        for user_group in self.user_groups:
            if user_group.has_permission(permission):
                return True
        # Nothing matched
        return False

    def to_dict(self):
        user_groups = []
        for user_group in self.user_groups:
            user_groups.append(user_group.id)
        permissions = []
        for permission in self.permissions:
            permissions.append(permission.to_dict())
        obj = super(User, self).to_dict()
        obj.update({
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user_groups': user_groups,
            'is_superuser': self.is_superuser,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
        })
        return obj


# ----------------------------------------------------------------------------------------------------------------------
class UserGroup(Principal):

    __tablename__ = 'user_group'
    __mapper_args__ = {
        'polymorphic_identity': 'user_group',
    }

    # User ID in database
    id = Column(Integer, ForeignKey('principal.id'), primary_key=True)
    # User group name
    name = Column(String(64), unique=True)
    # Members of the user group
    users = relationship('User', secondary=UserGroupUsers, backref='user_groups')

    def to_dict(self):
        users = []
        for user in self.users:
            users.append(user.id)
        permissions = []
        for permission in self.permissions:
            permissions.append(permission.to_dict())
        obj = super(UserGroup, self).to_dict()
        obj.update({
            'name': self.name,
            'users': users,
        })
        return obj


# ----------------------------------------------------------------------------------------------------------------------
class Permission(BaseModel):

    __tablename__ = 'permission'
    __mapper_args__ = {
        'polymorphic_identity': 'permission',
    }

    CREATE = 'create'
    RETRIEVE = 'retrieve'
    UPDATE = 'update'
    DELETE = 'delete'
    ALL = ','.join([CREATE, RETRIEVE, UPDATE, DELETE])

    # User ID in database
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # Action permitted (or not)
    action = Column(String(64), nullable=False)
    # Principal ID
    principal_id = Column(Integer, ForeignKey('principal.id'), nullable=False)
    # Principal associated with this permission
    principal = relationship('Principal', backref='permissions', foreign_keys=[principal_id])
    # ID of resource protected by permission
    resource_id = Column(String(64), nullable=False)
    # Whether permission is granted or denied
    granted = Column(Boolean, default=True)

    @validates('action')
    def validate_action(self, key, action):
        if action not in Permission.ALL:
            raise ValueError('Invalid action {}'.format(action))
        return action

    def to_dict(self):
        obj = super(Permission, self).to_dict()
        obj.update({
            'action': self.action,
            'principal': self.principal.id,
            'resource': self.resource_id,
            'granted': self.granted,
        })
        return obj
