"""
Add convenience methods to show PDFs in Jupyter Notebook.
"""

# TODO: Add size, see https://stackoverflow.com/questions/19470099/view-pdf-image-in-an-ipython-notebook
class PDF(object):
  def __init__(self, pdf):
    self.pdf = pdf

  def _repr_html_(self):
    return '<iframe src={0} style="position: relative; height: 300px; width: 100%;"></iframe>'.format(self.pdf)

  def _repr_latex_(self):
    return r'\includegraphics[width=1.0\columnwidth]{{{0}}}'.format(self.pdf)

def show(filepath, width=600, height=400):
    return PDF(filepath)

