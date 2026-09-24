from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

try:
    import matplotlib
    matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
    matplotlib.rcParams["axes.unicode_minus"] = False
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
except Exception:
    FigureCanvas = None


class ChartPlaceholder(QWidget):
    """没有数据时的轻量占位；有数据时使用文本表格，避免首次运行因绘图库不可用而崩溃。"""
    def __init__(self, title: str):
        super().__init__(); layout = QVBoxLayout(self); self.label = QLabel(title); self.label.setObjectName("muted"); layout.addWidget(self.label)

    def set_text(self, text: str): self.label.setText(text)


class AnalysisChart(QWidget):
    def __init__(self):
        super().__init__(); self.layout = QVBoxLayout(self)
        self.canvas = FigureCanvas(Figure(figsize=(7, 2.4))) if FigureCanvas else None
        if self.canvas:
            self.layout.addWidget(self.canvas); self.ax = self.canvas.figure.subplots()
        else:
            self.ax = None; self.layout.addWidget(QLabel("图表组件不可用，仍可查看统计表格。"))

    def draw(self, title: str, labels: list[str], values: list[float], kind: str = "bar", second: list[float] | None = None):
        if not self.ax: return
        self.ax.clear(); self.ax.set_title(title, fontsize=10); self.ax.tick_params(axis="x", labelrotation=25, labelsize=8)
        if kind == "line":
            self.ax.plot(labels, values, marker="o", color="#2f65d9", label="计划");
            if second is not None: self.ax.plot(labels, second, marker="o", color="#ef8a62", label="实际")
            self.ax.legend(fontsize=8)
        else:
            self.ax.bar(labels, values, color="#6d91e8")
        self.canvas.figure.tight_layout(); self.canvas.draw_idle()
