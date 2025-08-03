from typing import Callable, List, Tuple, Optional


class Integrator:
    """
    A collection of numerical integration methods.
    """

    def __init__(self, f: Callable[[float], float], a: float, b: float, n: int):
        """
        :param f: function to integrate
        :param a: lower bound
        :param b: upper bound
        :param n: number of subintervals
        """
        self.f = f
        self.a = a
        self.b = b
        self.n = n
        self.h, self.xs = self._partition_interval()

    def _partition_interval(self) -> Tuple[float, List[float]]:
        h = (self.b - self.a) / self.n
        xs = [self.a + i * h for i in range(self.n + 1)]
        return h, xs

    def _compute_ys(self) -> List[float]:
        return [self.f(x) for x in self.xs]

    def _build_steps(self, **kwargs) -> dict:
        return {
            "h": self.h,
            "x_values": self.xs,
            "y_values": kwargs.pop("y_values"),
            **kwargs
        }

    def trapezoidal(self, show_steps: bool = False) -> Tuple[float, Optional[dict]]:
        """
        Trapezoidal Rule:
          ∫_a^b f ≈ h * [ (f(a)+f(b))/2 + ∑ f(interior points) ]
        """
        ys = self._compute_ys()
        weighted_sum = (ys[0] + ys[-1]) / 2 + sum(ys[1:-1])
        result = self.h * weighted_sum

        steps = None
        if show_steps:
            steps = self._build_steps(
                y_values=ys,
                weighted_sum=weighted_sum,
                formula="h * ( (f(a)+f(b))/2 + sum(f interior) )"
            )
        return result, steps

    def simpson_one_third(self, show_steps: bool = False) -> Tuple[float, Optional[dict]]:
        """
        Simpson’s 1/3 Rule (n must be even):
          ∫_a^b f ≈ (h/3) * [ f(a)+f(b)
                              + 4*sum f at odd indices
                              + 2*sum f at even indices ]
        """
        if self.n % 2 != 0:
            raise ValueError("n must be even for Simpson’s 1/3")

        ys = self._compute_ys()
        odd_sum  = sum(ys[i] for i in range(1, self.n, 2))
        even_sum = sum(ys[i] for i in range(2, self.n, 2))
        result = (self.h / 3) * (ys[0] + ys[-1] + 4 * odd_sum + 2 * even_sum)

        steps = None
        if show_steps:
            steps = self._build_steps(
                y_values=ys,
                odd_sum=odd_sum,
                even_sum=even_sum,
                formula="h/3*(f(a)+f(b)+4*odd_sum+2*even_sum)"
            )
        return result, steps

    def simpson_three_eighths(self, show_steps: bool = False) -> Tuple[float, Optional[dict]]:
        """
        Simpson’s 3/8 Rule (n must be divisible by 3):
          ∫_a^b f ≈ (3*h/8) * [ f(a)+f(b)
                                + 3*sum f at i not multiple of 3
                                + 2*sum f at i multiple of 3 excluding endpoints ]
        """
        if self.n % 3 != 0:
            raise ValueError("n must be a multiple of 3 for Simpson’s 3/8")

        ys = self._compute_ys()
        sum_mod3 = sum(ys[i] for i in range(1, self.n) if i % 3 != 0)
        sum_mul3 = sum(ys[i] for i in range(3, self.n, 3))
        result = (3 * self.h / 8) * (ys[0] + ys[-1] + 3 * sum_mod3 + 2 * sum_mul3)

        steps = None
        if show_steps:
            steps = self._build_steps(
                y_values=ys,
                sum_mod3=sum_mod3,
                sum_mul3=sum_mul3,
                formula="3h/8*(f(a)+f(b)+3*sum_mod3+2*sum_mul3)"
            )
        return result, steps
