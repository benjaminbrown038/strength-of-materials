"""A small assembled 1D linear bar solver; no numerical library required."""
import math


def tridiagonal(lower, diagonal, upper, rhs):
    """Thomas elimination for the positive-definite reduced bar matrix."""
    b, d = list(diagonal), list(rhs)
    for i in range(1, len(b)):
        factor = lower[i - 1] / b[i - 1]
        b[i] -= factor * upper[i - 1]
        d[i] -= factor * d[i - 1]
    x = [0.0] * len(b)
    x[-1] = d[-1] / b[-1]
    for i in range(len(b) - 2, -1, -1):
        x[i] = (d[i] - upper[i] * x[i + 1]) / b[i]
    return x


def bar(E, A0, L, taper, P, elements):
    """A(x)=A0(1+taper*x/L), u(0)=0, tip force P, no body force.

    Integrating linear area exactly gives k_e=E*A(midpoint)/h.
    Global K is assembled as three diagonals, then the prescribed DOF is removed.
    """
    if isinstance(elements, bool) or not isinstance(elements, int) or elements < 1:
        raise ValueError("elements must be a positive integer")
    if not all(math.isfinite(v) for v in (E, A0, L, taper, P)):
        raise ValueError("bar inputs must be finite")
    if min(E, A0, L) <= 0 or taper <= -1:
        raise ValueError("positive E, A0, L and taper > -1 required")
    h = L / elements
    nodes = [i * h for i in range(elements + 1)]
    diagonal, off = [0.0] * (elements + 1), [0.0] * elements
    stiffness = []
    for e in range(elements):
        midpoint = (nodes[e] + nodes[e + 1]) / 2
        ke = E * A0 * (1 + taper * midpoint / L) / h
        stiffness.append(ke)
        diagonal[e] += ke
        diagonal[e + 1] += ke
        off[e] -= ke
    # u0 is zero, so no nonzero prescribed-displacement term enters the RHS.
    rhs = [0.0] * elements
    rhs[-1] = P
    u = [0.0] + tridiagonal(off[1:], diagonal[1:], off[1:], rhs)
    stresses = [E * (u[e + 1] - u[e]) / h for e in range(elements)]
    reaction = diagonal[0] * u[0] + off[0] * u[1]
    energy = sum(0.5 * stiffness[e] * (u[e + 1] - u[e]) ** 2 for e in range(elements))
    return dict(nodes=nodes, u=u, stress=stresses, reaction=reaction, energy=energy)


def exact_displacement(x, E, A0, L, taper, P):
    if taper == 0:
        return P * x / (E * A0)
    return P * L * math.log1p(taper * x / L) / (E * A0 * taper)
