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

    for tls in agents:

        lanes = list(set(
            traci.trafficlight.getControlledLanes(tls)
        ))

        queues = []

        for lane in lanes:
            q = traci.lane.getLastStepHaltingNumber(lane)
            queues.append(q)

        reward = -sum(queues)
        total_reward += reward

        phase_timer[tls] += 1

        if phase_timer[tls] >= GREEN_TIME:

            if len(queues) >= 2:

                first_half = sum(queues[:len(queues)//2])
                second_half = sum(queues[len(queues)//2:])

                if first_half > second_half:
                    action = 0
                else:
                    action = 2

                traci.trafficlight.setPhase(tls, action)

            phase_timer[tls] = 0

        if step % 100 == 0:
            print(
                f"Step={step} | TLS={tls} | Queues={queues} | Reward={reward}"
            )

traci.close()

print("\nTotal Reward =", total_reward)