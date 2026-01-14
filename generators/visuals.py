class Visuals:

    @staticmethod
    def wave_basic():
        return """
        visuals = VGroup()
        axes = Axes(x_range=[0, 4*PI], y_range=[-2,2])
        wave = axes.plot(lambda x: np.sin(x), color=BLUE)
        visuals.add(axes, wave)
"""

    @staticmethod
    def wave_amplitude():
        return """
        visuals = VGroup()
        axes = Axes(x_range=[0, 4*PI], y_range=[-2,2])
        wave = axes.plot(lambda x: np.sin(x))
        amp = DoubleArrow(ORIGIN, UP*2, color=YELLOW)
        visuals.add(axes, wave, amp)
"""

    @staticmethod
    def wave_wavelength():
        return """
        visuals = VGroup()
        axes = Axes(x_range=[0, 4*PI], y_range=[-2,2])
        wave = axes.plot(lambda x: np.sin(x))
        brace = Brace(Line(ORIGIN, RIGHT*PI), DOWN)
        visuals.add(axes, wave, brace)
"""

    @staticmethod
    def pythagoras_triangle():
        return """
        visuals = VGroup()
        tri = Polygon(LEFT*3+DOWN, RIGHT*2+DOWN, LEFT*3+UP*2)
        visuals.add(tri)
"""

    @staticmethod
    def flow_pressure():
        return """
        visuals = VGroup()
        box = Rectangle(height=4, width=2)
        arrows = VGroup(*[Arrow(UP, DOWN) for _ in range(4)]).arrange(DOWN)
        arrows.next_to(box, RIGHT)
        visuals.add(box, arrows)
"""
