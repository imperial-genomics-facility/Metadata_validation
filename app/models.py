from . import db
class Platform(db.Model):
  __tablename__='platform'
  id = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.String(60),unique=True)
  m_reads = db.Column(db.Integer)
  m_bases = db.Column(db.Integer)
  m_clusters = db.Column(db.Integer)
  m_output = db.Column(db.Integer)
  clusters = db.Column(db.Integer)
  lanes = db.Column(db.Integer)
  max_samples = db.Column(db.Integer)
  is_pe = db.Column(db.Integer)
  read_length = db.Column(db.Integer)

  def __repr__(self):
    return '<Platform %r>' % self.name

class Assay_type(db.Model):
  __tablename__='assay_type'
  id = db.Column(db.Integer,primary_key=True)
  assay_name = db.Column(db.String(30),unique=True)
  read_count = db.Column(db.Integer)
  is_sc = db.Column(db.Integer)

  def __repr__(self):
    return '<Assay_type %r>' % self.assay_name