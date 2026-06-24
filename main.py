from communication.message import TrafficMessage
from communication.failure_injector import FailureInjector
from detector.failure_detector import FailureDetector
from detector.mode_switcher import ModeSwitcher
import subprocess

injector = FailureInjector(
    packet_loss=0.3,
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

    state, message = result

    status = detector.detect(
        packet_lost=False,
        delayed=(state == "DELAYED")
    )

mode = switcher.select_mode(status)

with open(
    "dashboard/controller_status.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(mode)

print("STATUS =", status)
print("MODE =", mode)

if result:
    print(result)

if mode == "COOPERATIVE_MARL":

    print("Launching Cooperative MARL...")

    subprocess.run(
        ["python", "marl/marl_comm_controller.py"]
    )

elif mode == "LIMITED_COMMUNICATION":

    print("Launching Limited Communication MARL...")

    subprocess.run(
        ["python", "marl/limited_comm_controller.py"]
    )

elif mode == "INDEPENDENT_AGENT":

    print("Launching Independent MARL...")

    subprocess.run(
        ["python", "marl/marl_controller.py"]
    )