from stable_baselines3 import PPO
import sys
import os

print("\nLIMITED COMMUNICATION MODE ACTIVE")
print("Partial agent communication enabled\n")


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

for step in range(500):

    action, _ = model.predict(
        state,
        deterministic=True
    )

    state, reward, done, trunc, info = env.step(action)

    if step % 50 == 0:

        print(f"\nStep={step}")

        tls_ids = [
            "A0","A1","A2",
            "B0","B1","B2",
            "C0","C1","C2"
        ]

        for tls, act in zip(tls_ids, action):

            decision = (
                "SWITCH"
                if act == 1
                else "KEEP"
            )

            print(f"{tls} -> {decision}")

        print("Reward =", reward)
    
    if step % 50 == 0:
        print("Agents exchanging limited information...")

env.close()