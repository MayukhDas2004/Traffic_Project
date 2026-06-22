import os
import traci

GREEN_TIME = 20

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG = os.path.join(
    BASE_DIR,
    "simulation",
    "simulation.sumocfg"
)

print("Using config:", CONFIG)

traci.start(["sumo", "-c", CONFIG])

agents = ["A1", "B0", "B1", "C1"]

phase_timer = {tls: 0 for tls in agents}
total_reward = 0

for step in range(500):

    traci.simulationStep()

    messages = {}

    # -------- Collect states --------
    for tls in agents:

        lanes = list(set(
            traci.trafficlight.getControlledLanes(tls)
        ))

        queues = []

        for lane in lanes:
            queues.append(
                traci.lane.getLastStepHaltingNumber(lane)
            )

        messages[tls] = sum(queues)

    # -------- Make decisions --------
    for tls in agents:

        phase_timer[tls] += 1

        lanes = list(set(
            traci.trafficlight.getControlledLanes(tls)
        ))

        queues = []

        for lane in lanes:
            queues.append(
                traci.lane.getLastStepHaltingNumber(lane)
            )

        reward = -sum(queues)
        total_reward += reward

        if phase_timer[tls] >= GREEN_TIME:

            local_queue = sum(queues)

            neighbor_pressure = 0

            for other in agents:
                if other != tls:
                    neighbor_pressure += messages[other]

            if local_queue > neighbor_pressure / 3:
                action = 0
            else:
                action = 2

            traci.trafficlight.setPhase(tls, action)

            phase_timer[tls] = 0

        if step % 100 == 0:
            print(
                f"Step={step} | {tls} | Queue={sum(queues)}"
            )

traci.close()

print("\nTotal Reward =", total_reward)