How to use rsmf
===============



Setup
-----

You need to tell rsmf how you set up your document by invoking ``rsmf.setup``. This can be done in two ways. Either, you give rsmf the ``\documentclass`` string used for setting up the document, as in

.. code-block:: python

    import rsmf
    formatter = rsmf.setup(r"\documentclass[a4paper,12pt,noarxiv]{quantumarticle}")

The ``r`` in front of the string is necessary so that ``\d`` is not mistaken for an escape sequence. If you have your document stored locally, there is an even more convenient way:
you can just supply rsmf with the path to your main tex file (the one containing the document setup) and it will find that out for itself:

.. code-block:: python

    formatter = rsmf.setup("example.tex")

This is especially cool because rsmf will automatically adjust the plots when the underlying document class is changed without any needs to change python code! 
This makes swapping journals a lot easier.

Custom
~~~~~~

If the document class you're preparing figures for is not supported by ``rsmf`` you can still use it to prepare your figures. In this case you will have to measure the column widths
yourself. To do so, you have to insert the following command into your text

.. code-block:: LaTeX

    \begin{figure}
        \the\columnwidth
    \end{figure}

This will give you the width of a single-column figure. If your document class also supports two-column mode, you also need to extract the width of wide figures via

.. code-block:: LaTeX

    \begin{figure*}
        \the\columnwidth
    \end{figure*}

Both commands will output something along the lines of ``246.0pt``. As ``matplotlib`` expects measurements to be in inches, ``rsmf`` does too.
You therefore have to multiply the measurement in points with ``0.01389`` to get the correct measurement in inches.

It is also important to see if your document class loads packages that change the rendering of fonts, e.g. ``\usepackage{times}``. If this is the case,
you have to provide them as a separate preamble that is then used in the PGF backend. 

With these informations at hand, you can invoke ``rsmf``'s ``CustomFormatter``:

.. code-block:: python

    from rsmf import CustomFormatter

    formatter = CustomFormatter(
        columnwidth=246 * 0.01389, 
        wide_columnwidth=512 * 0.01389, 
        fontsizes=11, 
        pgf_preamble=r"\usepackage{lmodern}",
    )

Figures
-------
The setup routine will return a formatter. This formatter can then be used to create matplotlib figure objects by invoking the method ``formatter.figure``. It has three arguments:

* ``aspect_ratio`` (float, optional): the aspect ratio (height/width) of your plot. Defaults to the inverse of the golden ratio.
* ``width_ratio`` (float, optional): the width of your plot in multiples of ``\columnwidth``. Defaults to 1.0.
* ``wide`` (bool, optional): indicates if the figures spans two columns in twocolumn mode, 
                i.e. if the figure* environment is used, has no effect in onecolumn mode . Defaults to False.

This is the place where you set the width of your plots, *not in the LaTeX document*. If you include the resulting figure with a different width, the font sizes will not match the surrounding document!

For example, a regular figure is created via

.. code-block:: python

    fig = formatter.figure(aspect_ratio=.5)

    # ... some plotting ...
    plt.savefig("example.pdf")

and included via

.. code-block:: LaTeX

    \begin{figure}
        \centering
        \includegraphics{example}
        \caption{...}
    \end{figure}

A wide figure that spans 80% of the page on the other hand is created by

.. code-block:: python

    fig = formatter.figure(width_ratio=.8, wide=True)

    # ... some plotting ...
    plt.savefig("example_wide.pdf")
    
and included via the multi-column ``figure*`` environment:

.. code-block:: python

    \begin{figure*}
        \centering
        \includegraphics{example_wide}
        \caption{...}
    \end{figure*}

Note that you should always save your figures in some sort of vectorized format, like ``pdf`` and that calling ``plt.tight_layout()`` before saving usually makes your plots nicer.

Moreover, observe that the ``aspect_ratio`` parameter is defined as the height of the plot devided by its width. Even though aspect ratios are more commonly defined as width/height, this choice results in having the width and the height of the figure proportional to ``width_ratio`` and ``aspect_ratio`` respectively. 

Custom
~~~~~~
If you want more control about the creation of your figure, you can make use of ``formatter.columnwidth`` and ``formatter.wide_columnwidth`` to create them yourself.

Other features
~~~~~~~~~~~~~~

You can access the underlying fontsizes via ``formatter.fontsizes``. The nomenclature follows that of LaTeX itself, so we have 

.. code-block:: python

    formatter.fontsizes.tiny
    formatter.fontsizes.scriptsize
    formatter.fontsizes.footnotesize
    formatter.fontsizes.small
    formatter.fontsizes.normalsize
    formatter.fontsizes.large
    formatter.fontsizes.Large
    formatter.fontsizes.LARGE
    formatter.fontsizes.huge
    formatter.fontsizes.Huge

This is especially useful if you want to tweak titles, legends and annotations while still having proper (LaTeX) fontsizes.

Using rsmf with other frameworks
--------------------------------

You can use rsmf together with your favorite plotting framework, for example ``seaborn``. There is only one catch: if you use matplotlib styles or seaborn styles, you might overwrite the settings imposed by rsmf, especially regarding font-size. To this end, the formatters have a method ``formatter.set_default_fontsizes`` that only change the underlying fontsizes. An example use would be

.. code-block:: python

    fig = formatter.figure(wide=True)
    sns.set(style="ticks")
    formatter.set_default_fontsizes()

    # ... some plotting ...

Sometimes these styles also overwrite other things, like the font family (serif/sans-serif). There is no correction method for that yet.
