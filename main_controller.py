import subprocess
from communication.message import TrafficMessage
from communication.failure_injector import FailureInjector
from detector.failure_detector import FailureDetector
from detector.mode_switcher import ModeSwitcher

injector = FailureInjector(
    packet_loss=0.5,
    delay_probability=0.2
)

detector = FailureDetector()
switcher = ModeSwitcher()

msg = TrafficMessage(
    sender="A1",
    queue_length=12,
    vehicle_count=20,
    phase=1
)

result = injector.transmit(msg)

if result is None:

    status = detector.detect(
        packet_lost=True
    )

else:

    status = detector.detect(
        packet_lost=False
    )

mode = switcher.select_mode(status)

print("STATUS =", status)
print("MODE =", mode)

if mode == "COOPERATIVE_MARL":
    subprocess.run(
        ["python", "marl/marl_comm_controller.py"]
    )

elif mode == "INDEPENDENT_AGENT":
    subprocess.run(
        ["python", "marl/marl_controller.py"]
    )