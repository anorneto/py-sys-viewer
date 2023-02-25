from time import monotonic
from typing import List

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Header, Footer, Static, Tree
from textual.reactive import reactive

from src.domain.dto.hardware import Hardware
from src.domain.dto.sensor import Sensor
from src.domain.use_case.get_hardware_data import GetHardwareData


class TimeDisplay(Static):
    """A widget to display elapsed time."""

    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        """Method to update the time to the current time."""
        self.time = self.total + (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def start(self) -> None:
        """Method to start (or resume) time updating."""
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        """Method to stop the time display updating."""
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self) -> None:
        """Method to reset the time display to zero."""
        self.total = 0
        self.time = 0


class HardwareTree(Static):
    """A Hardwaree Tree"""

    hardware_list: reactive[List[Hardware]] = reactive([])

    def _generate_tree(self, hardware_list: List[Hardware]) -> Tree:
        hardware_tree: Tree[Sensor] = Tree("PC")
        hardware_tree.root.expand()
        for hardware in self.hardware_list:
            hadware_node = hardware_tree.root.add(label=str(hardware), expand=True)
            if len(hardware.sensors) > 0:
                for sensor in hardware.sensors:
                    hadware_node.add_leaf(label=str(sensor), data=sensor)
            if len(hardware.sub_hardware) > 0:
                for sub_hardware in hardware.sub_hardware:
                    if len(sub_hardware.sensors) > 0:
                        sub_hardware_node = hadware_node.add(
                            str(sub_hardware), expand=True
                        )
                        for sensor in sub_hardware.sensors:
                            sub_hardware_node.add_leaf(label=str(sensor), data=sensor)
        return hardware_tree

    def watch_hardware_list(self, hardware_list: List[Hardware]):
        hardware_tree = self._generate_tree(hardware_list=hardware_list)
        tree_query = self.query(Tree)
        if tree_query:
            # TODO: improve this , update only label. maybe create a custom Tree Widget?
            tree_query.first().remove()
            self.mount(hardware_tree)

    def compose(self) -> ComposeResult:
        hardware_tree = self._generate_tree(self.hardware_list)
        yield hardware_tree


class CliApp(App):
    CSS_PATH = "css/cli_app.css"

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("a", "add_stopwatch", "Add"),
        ("r", "remove_stopwatch", "Remove"),
    ]

    hardware_list: List[Hardware] = []

    def on_mount(self) -> None:
        self._get_hardware_data: GetHardwareData = GetHardwareData()
        self.update_hardware = self.set_interval(2, self.update_hardware_list)

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Footer()
        # yield Container(HardwareTree(id="hardware_tree"), id="hardware_tree_container")
        yield HardwareTree(id="hardware_tree")

    def update_hardware_list(self) -> None:
        """Method to update the _hardware_list"""
        self.hardware_list = self._get_hardware_data.execute()
        hardware_tree_widget: HardwareTree = self.query_one(
            selector="#hardware_tree", expect_type=HardwareTree
        )
        if hardware_tree_widget:
            hardware_tree_widget.hardware_list = self.hardware_list

    # def action_add_stopwatch(self) -> None:
    #     """An action to add a timer."""
    #     new_stopwatch = Stopwatch()
    #     self.query_one("#timers").mount(new_stopwatch)
    #     new_stopwatch.scroll_visible()

    # def action_remove_stopwatch(self) -> None:
    #     """Called to remove a timer."""
    #     timers = self.query("Stopwatch")
    #     if timers:
    #         timers.last().remove()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
