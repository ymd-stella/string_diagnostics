#!/usr/bin/env python3
import sys
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.duration import Duration
from diagnostic_msgs.msg import DiagnosticStatus
import diagnostic_updater
import re


class StringDiagnosticsNode(Node):
    LEVEL_MAP = {
        "OK": DiagnosticStatus.OK,
        "WARN": DiagnosticStatus.WARN,
        "ERROR": DiagnosticStatus.ERROR,
        "STALE": DiagnosticStatus.STALE,
    }

    def __init__(self):
        super().__init__("string_diagnostics")
        self._name = self.declare_parameter("name", "noname").value
        self._tolerance = Duration(seconds=self.declare_parameter("tolerance", 1.0).value)
        self._sub = self.create_subscription(String, "message", self._diagnostic_message_callback, 10)
        self._updater = diagnostic_updater.Updater(self)
        self._updater.add(self._name, self._sample_task)
        self._latest_stamp = None
        self._raw_message = None

    def _sample_task(self, stat):
        if not self._latest_stamp:
            stat.summary(DiagnosticStatus.STALE, "No valid message")
            return stat
        if self.get_clock().now() - self._latest_stamp > self._tolerance:
            stat.summary(DiagnosticStatus.STALE, "Message too old")
            return stat
        prog = re.compile("\[(.*)\] (.*)")
        result = prog.match(self._raw_message)
        if not result:
            stat.summary(DiagnosticStatus.STALE, "Invalid syntax")
            return stat
        level_str = result.group(1)
        message = result.group(2)
        if level_str not in StringDiagnosticsNode.LEVEL_MAP:
            stat.summary(DiagnosticStatus.STALE, f"diagnostic level not in {StringDiagnosticsNode.LEVEL_MAP.keys()}")
            return stat
        level = StringDiagnosticsNode.LEVEL_MAP[level_str]
        stat.summary(level, message)
        return stat

    def _diagnostic_message_callback(self, msg):
        self._raw_message = msg.data
        self._latest_stamp = self.get_clock().now()


def main(argv=None):
    rclpy.init()
    node = StringDiagnosticsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == "__main__":
    main(sys.argv)
