"""
Add convenience methods to show PDFs in Jupyter Notebook.
"""


class PDF(object):
    """
    Provides a wrapper around a PDF file path that can be displayed in Jupyter Notebooks.

    Based on ``https://stackoverflow.com/questions/19470099/view-pdf-image-in-an-ipython-notebook``.

    Args:
        pdf_path (str): Path of the PDF file to be displayed
        width (Union[int,str,NoneType], optional): Width of the displayed PDF's iframe. 
            Considered as pixels when integer, and as CSS compatible width measurement when string. Defaults to 100%.
        height ([type], optional): Height of the displayed PDF's iframe. 
            Considered as pixels when integer, and as CSS compatible height measurement when string. Defaults to 300px.
    """

    def __init__(self, pdf_path, width=None, height=None):
        self.pdf_path = pdf_path

        if isinstance(width, str):
            self.width_str = width
        elif isinstance(width, int):
            self.width_str = "{}px".format(width)
        else:
            self.width_str = "100%"

        if isinstance(height, str):
            self.height_str = height
        elif isinstance(height, int):
            self.height_str = "{}px".format(height)
        else:
            self.height_str = "300px"

    def _repr_html_(self):
        return '<iframe src={0} style="position: relative; height: {1}; width: {2};"></iframe>'.format(
            self.pdf_path, self.width_str, self.height_str
        )

    def _repr_latex_(self):
        return r"\includegraphics[width=1.0\columnwidth]{{{0}}}".format(self.pdf_path)


def show(pdf_path, width=None, height=None):
    """
    Show a PDF in Jupyter Notebook.

    Args:
        pdf_path (str): Path of the PDF file to be displayed
        width (Union[int,str,NoneType], optional): Width of the displayed PDF's iframe. 
            Considered as pixels when integer, and as CSS compatible width measurement when string. Defaults to 100%.
        height ([type], optional): Height of the displayed PDF's iframe. 
            Considered as pixels when integer, and as CSS compatible height measurement when string. Defaults to 300px.

    Returns:
        PDF: A wrapper around the the PDF file's path that renders as an iframe in Jupyter Notebook.
    """
    return PDF(pdf_path, width=width, height=height)
