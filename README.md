# rsmf (right-size my figures)

As a researcher, you usually want your work to be presented as nice as possible. This library helps with that by providing a means to 
automatically adjust figure sizes and fontsizes in matplotlib to fit the ones in commonly used scientific journals. Currently `quantumarticle` is supported. 

## Usage


### Setup
You need to tell rsmf how you set up your document by invoking `rsmf.setup`. This can be done in two ways. Either, you give rsmf the `\documentclass` string used for setting up the document, as in
```python
formatter = rsmf.setup(r"\documentclass[a4paper,12pt,noarxiv]{quantumarticle}")
```
The `r` in front of the string is necessary so that `\d` is not mistaken for an escape sequence. If you have your document stored locally, there is an even more convenient way.
You can just supply rsmf with the path to your main tex file (the one containing the document setup) and it will find that out for itself:
```python
formatter = rsmf.setup("example.tex")
```
This is especially cool because rsmf will automatically adjust the plots when the underlying document class is changed without any needs to change python code!

### Figures
The setup routine will return a formatter. This formatter can then be used to create matplotlib figure objects by invoking `formatter.figure`. The method has three arguments:
* `aspect_ratio` (float, optional): the aspect ratio (width/height) of your plot. Defaults to the golden ratio.
* `width_ratio` (float, optional): the width of your plot in multiples of `\columnwidth`. Defaults to 1.0.
* `wide` (bool, optional): indicates if the figures spans two columns in twocolumn mode, 
                i.e. if the figure* environment is used, has no effect in onecolumn mode . Defaults to False.

This is the place where you set the width of your plots, _not in the LaTeX document._ 

For example, a regular figure is created via
```python
fig = formatter.figure(aspect_ratio=.5)

# ... some plotting ...
plt.savefig("example.pdf")
```
and included via
```tex
\begin{figure}
	\centering
	\includegraphics{example}
	\caption{...}
\end{figure}
```
A wide figure that doesn't span the whole page on the other hand is created by
```python
fig = formatter.figure(width_ratio=.8, wide=True)

# ... some plotting ...
plt.savefig("example_wide.pdf")
```
and included via the multi-column `figure*` environment:
```tex
\begin{figure*}
	\centering
	\includegraphics{example_wide}
	\caption{...}
\end{figure*}
```

Note that you should always save your figures in some sort of vectorized format, like `pdf` and that calling `plt.tight_layout()` before saving usually makes your plots nicer.

### Other features
You can access the underlying fontsizes via `formatter.fontsizes`. The nomenclature follows that of LaTeX itself, so we have 
```python
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
```

### Using it with other frameworks
You can use rsmf together with your favorite plotting framework, for example `seaborn`. There is only one catch: if you use seaborn styles or other styles, you might overwrite the font-size settings imposed by rsmf. To this end, the formatters have a method `formatter.set_default_fontsizes` that only change the underlying fontsizes. An example use would be
```python
fig = formatter.figure(wide=True)
sns.set(style="ticks")
formatter.set_default_fontsizes()
```

### Example
An example document alongside with a notebook for making the plots used can be found in the `examples` folder.

## How it works
Under the hood, rsmf sets the matplotlib backend to `pgf`, which allows the use of LaTeX. For each supported document class, the specific column widths and font sizes are stored in code, alongside with packages that are loaded that change fonts. For `quantumarticle`, for example, the package `lmodern` is loaded into the `pgf` backend. 

When calling `rsmf.setup`, matplotlib's `rcParams` are adjusted to make the fontsizes match the surrounding document.


## Contribute
Do you have trouble setting up plots for your favorite document class and it's not supported here? Don't hesitate to make a PR!
