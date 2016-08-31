import json
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean, Text
from sqlalchemy.orm import relationship, validates
from lib.models import Base, BaseModel


# ----------------------------------------------------------------------------------------------------------------------
FileSetFiles = Table(
    'file_set_files', Base.metadata,
    Column('file_set_id', Integer, ForeignKey('file_set.id')),
    Column('file_id', Integer, ForeignKey('file.id'))
)


# ----------------------------------------------------------------------------------------------------------------------
class FileType(BaseModel):

    __tablename__ = 'file_type'
    __mapper_args__ = {
        'polymorphic_identity': 'file_type',
    }

    NIFTI = 'nifti'
    DICOM = 'dicom'
    CSV = 'csv'
    TXT = 'txt'
    BINARY = 'binary'
    ALL = [NIFTI, DICOM, CSV, TXT, BINARY]

    # File type ID in database
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # Type name
    name = Column(String(64), nullable=False, unique=True)

    def to_dict(self):
        obj = super(FileType, self).to_dict()
        obj.update({
            'name': self.name,
        })
        return obj


# ----------------------------------------------------------------------------------------------------------------------
class ScanType(BaseModel):

    __tablename__ = 'scan_type'
    __mapper_args__ = {
        'polymorphic_identity': 'scan_type',
    }

    T1 = 't1'
    T2 = 't2'
    FMR = 'fmr'
    FMR_REST = 'rest'
    DTI = 'dti'
    CT = 'ct'
    NONE = 'none'
    ALL = [T1, T2, FMR, FMR_REST, DTI, CT, NONE]

    # Scan type ID in database
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # Scan type name
    name = Column(String(64), nullable=False, unique=True)

    def to_dict(self):
        obj = super(ScanType, self).to_dict()
        obj.update({
            'name': self.name,
        })
        return obj


# ----------------------------------------------------------------------------------------------------------------------
class Repository(BaseModel):

    __tablename__ = 'repository'
    __mapper_args__ = {
        'polymorphic_identity': 'repository',
    }

    # Repository ID in database
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # Repository name
    name = Column(String(255), nullable=False, unique=True)

    def to_dict(self):
        files = []
        for f in self.files:
            files.append(f.id)
        obj = super(Repository, self).to_dict()
        obj.update({
            'name': self.name,
            'files': files,
        })
        return obj


# ----------------------------------------------------------------------------------------------------------------------
class File(BaseModel):

    __tablename__ = 'file'
    __mapper_args__ = {
        'polymorphic_identity': 'file',
    }

    # File ID in database
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # File name without path information
    name = Column(String(255), nullable=False)
    # File type ID
    file_type_id = Column(Integer, ForeignKey('file_type.id'))
    # File type
    file_type = relationship('FileType', foreign_keys=[file_type_id])
    # Scan type ID
    scan_type_id = Column(Integer, ForeignKey('scan_type.id'))
    # Scan type
    scan_type = relationship('ScanType', foreign_keys=[scan_type_id])
    # File content type
    content_type = Column(String(64), nullable=False)
    # File size
    size = Column(Integer, nullable=False)
    # Storage ID in storage backend
    storage_id = Column(String, nullable=False)
    # Storage path in storage backend
    storage_path = Column(String, nullable=False)
    # File repository ID
    repository_id = Column(Integer, ForeignKey('repository.id'), nullable=False)
    # File repository
    repository = relationship('Repository', backref='files', foreign_keys=[repository_id])

    def to_dict(self):
        file_sets = []
        for file_set in self.file_sets:
            file_sets.append(file_set.id)
        obj = super(File, self).to_dict()
        obj.update({
            'name': self.name,
            'file_type': self.file_type.id,
            'scan_type': self.scan_type.id,
            'content_type': self.content_type,
            'size': self.size,
            'storage_id': self.storage_id,
            'storage_path': self.storage_path,
            'repository': self.repository.id,
            'file_sets': file_sets,
        })
        return obj


# ----------------------------------------------------------------------------------------------------------------------
class FileSet(BaseModel):

    __tablename__ = 'file_set'
    __mapper_args__ = {
        'polymorphic_identity': 'file_set',
    }

    # File set ID
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # File set name
    name = Column(String(255), nullable=False)
    # Files inside this file set
    files = relationship('File', secondary=FileSetFiles, backref='file_sets')
    # File set schema ID
    schema_id = Column(Integer, ForeignKey('file_set_schema.id'))
    # File set schema
    schema = relationship('FileSetSchema', foreign_keys=[schema_id])
    # File set schema enabled
    schema_enabled = Column(Boolean, default=False)

    def to_dict(self):
        files = []
        for f in self.files:
            files.append(f.id)
        obj = super(FileSet, self).to_dict()
        obj.update({
            'name': self.name,
            'schema': self.schema_id,
            'schema_enabled': self.schema_enabled,
            'files': files,
        })
        return obj


# ----------------------------------------------------------------------------------------------------------------------
class FileSetSchema(BaseModel):

    __tablename__ = 'file_set_schema'
    __mapper_args__ = {
        'polymorphic_identity': 'file_set_schema',
    }

    # File set ID
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # File set schema name
    name = Column(String(255), nullable=False)
    # Schema version
    version = Column(String(16), default='v1')
    # Schema file specification
    _specification = Column(Text, nullable=False)

    @property
    def specification(self):
        return json.loads(self._specification)

    @specification.setter
    def specification(self, specification):
        self._specification = json.dumps(specification)

    def to_dict(self):
        obj = super(FileSetSchema, self).to_dict()
        obj.update({
            'name': self.name,
            'version': self.version,
            'specification': self.specification,
        })
        return obj


# ----------------------------------------------------------------------------------------------------------------------
class FileQualityCheck(BaseModel):

    __tablename__ = 'file_quality_check'

    PASS = 'pass'
    FAIL = 'fail'

    # File quality check ID
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # File to which quality check corresponds
    file_id = Column(Integer, ForeignKey('file.id'), nullable=False)
    # File object
    file = relationship('File', backref='quality_check', foreign_keys=[file_id])
    # Status field
    status = Column(String(4), nullable=False)
    # Comments about the quality check
    comments = Column(Text)

    @validates('status')
    def validate_status(self, key, status):
        if status not in [self.PASS, self.FAIL]:
            raise ValueError('Invalid status {}'.format(status))
        return status

    def to_dict(self):
        obj = super(FileQualityCheck, self).to_dict()
        obj.update({
            'status': self.status,
            'comments': self.comments,
        })
        return obj
