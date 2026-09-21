# Equation format used throughout this repo

Every lesson uses the same section order. Display equations use `$$` on separate
lines, without blank lines inside an equation. Inline symbols use single `$`.
Equations are never wrapped in blockquotes or nested inside lists.

Copy this style into GitHub Markdown:

```text
$$
\sigma=\frac{P}{A},
\qquad \varepsilon=\frac{\delta}{L},
\qquad \sigma=E\varepsilon.
$$
```

Matrices use a single math block and `\\` only as a matrix row separator:

```text
$$
\mathbf{k}_e=\frac{EA}{L_e}
\begin{bmatrix}
1 & -1\\
-1 & 1
\end{bmatrix}.
$$
```

Each lesson defines its symbols in a table and states assumptions beside the
equations. Units belong in JSON key names and output labels. Do not use an
unlabeled symbol for both a material property and a stress component: yield
strength is $S_y$; a normal stress component is $\sigma_y$.

GitHub renders these blocks. In a plain text editor the delimiters remain visible;
use a math-capable Markdown preview when reading locally.
