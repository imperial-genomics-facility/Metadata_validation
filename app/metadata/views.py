from . import metadata

@metadata.route('/')
def metadata_home():
  return render_template('metadata/metadata_reformat.html')