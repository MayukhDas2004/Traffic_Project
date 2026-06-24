from stable_baselines3 import PPO

import sys
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(BASE_DIR)

from communication.failure_injector import FailureInjector
from detector.failure_detector import FailureDetector

print("\nCOOPERATIVE MARL MODE ACTIVE")
print("Agent communication enabled\n")

# Communication monitoring
injector = FailureInjector(
    packet_loss=0.3,
    delay_probability=0.2
)

detector = FailureDetector()

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(
    os.path.join(BASE_DIR, "simulation")
)

from marl_env import TrafficEnv

env = TrafficEnv()

model = PPO.load(
    os.path.join(
        BASE_DIR,
        "simulation",
        "traffic_marl_ppo"
    )
)

state, _ = env.reset()

step = 0
while True:


    # if step % 50 == 0:
    #     print("Checking communication status...")

    # if hasattr(env, "current_mode"):
    #     print("CURRENT MODE =", env.current_mode)

    action, _ = model.predict(
        state,
        deterministic=True
    )

    state, reward, done, trunc, info = env.step(action)
    if step % 50 == 0:
        print("Waiting Time =", info["waiting_time"])
        print("Queue Length =", info["queue_length"])
        print("Throughput =", info["throughput"])
        print("Travel Time =", info["travel_time"])

    if step % 50 == 0:

        print(f"\nStep={step}")

        tls_ids = [
            "A0", "A1", "A2",
            "B0", "B1", "B2",
            "C0", "C1", "C2"
        ]

        for tls, act in zip(tls_ids, action):

            decision = (
                "SWITCH"
                if act == 1
                else "KEEP"
            )

            print(f"{tls} -> {decision}")

        print("Reward =", reward)
        print("Agents exchanging information...")
    step += 1
# env.close()