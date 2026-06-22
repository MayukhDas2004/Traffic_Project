import matplotlib.pyplot as plt

controllers = [
    "SMART_V2",
    "MARL",
    "MARL_COMM",
    "DQN"
]

rewards = [
    -18332,
    -56903,
    -57252,
    -162.20
]

plt.figure(figsize=(8, 5))

colors = ["blue", "orange", "red", "green"]

plt.bar(
    controllers,
    rewards,
    color=colors
)

plt.title("Traffic Controller Comparison")
plt.ylabel("Reward")
plt.xlabel("Controllers")

plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()

plt.savefig("controller_comparison.png")

plt.show()

print("Graph saved as controller_comparison.png")