
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from sumo_connector import get_agent_data
from datetime import datetime
from action_reader import get_actions

st.set_page_config(
    page_title="Traffic Digital Twin",
    layout="wide"
)

st_autorefresh(interval=30000, key="refresh")

st.title("🚦 Intelligent Traffic Management System")
st.caption(
    f"Last Updated: {datetime.now().strftime('%H:%M:%S')}"
)
# ==================================================
# TOP SECTION
# ==================================================

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live SUMO Simulation")

    st.info(
        "SUMO simulation is running in a separate window."
    )

with col2:

    st.subheader("System Status")

    try:

        with open(
            "dashboard/controller_status.txt",
            "r",
            encoding="utf-8-sig"
        ) as f:

            mode = f.read().strip()

        if mode == "COOPERATIVE_MARL":
            st.success("Communication : HEALTHY")

        elif mode == "DIGITAL_TWIN":
            st.warning("Communication : DEGRADED")

        elif mode == "INDEPENDENT_AGENT":
            st.error("Communication : FAILED")

    except:
        st.error("Communication Status Unknown")

    st.success("Failure Detector : ACTIVE")
    st.success("Mode Switcher : ACTIVE")

st.divider()


# ==================================================
# 9 AGENTS (REAL NETWORK)
# ==================================================

agent_data = get_agent_data()

st.subheader("📊 Network Summary")

if len(agent_data) == 0:

    st.error("No live data received from SUMO")
    st.stop()

total_queue = sum(
    agent_data[t]["queue"]
    for t in agent_data
)

total_wait = sum(
    agent_data[t]["wait"]
    for t in agent_data
)

c1, c2 = st.columns(2)

c1.metric("Total Queue", total_queue)
c2.metric(
    "Total Waiting Time",
    f"{int(total_wait)} s"
)

active_intersections = sum(
    1 for tls in agent_data
    if agent_data[tls]["queue"] > 0
)

st.metric(
    "🚗 Active Intersections",
    active_intersections
)

green_count = sum(
    1 for tls in agent_data
    if "GREEN" in agent_data[tls]["phase"]
)

red_count = len(agent_data) - green_count

c1, c2 = st.columns(2)

c1.metric(
    "🟢 Green Signals",
    green_count
)

c2.metric(
    "🔴 Red Signals",
    red_count
)

avg_queue = total_queue / len(agent_data)

st.metric(
    "Average Queue per Intersection",
    f"{avg_queue:.1f}"
)

max_tls = max(
    agent_data,
    key=lambda x: (
        agent_data[x]["queue"],
        agent_data[x]["wait"]
    )
)

st.warning(
    f"🚨 Highest Congestion: {max_tls} "
    f"(Queue={agent_data[max_tls]['queue']}, "
    f"Wait={int(agent_data[max_tls]['wait'])}s)"
)

st.info(
    f"🎯 Priority Signal: {max_tls}"
)

if total_queue > 200:

    st.error(
        "🔴 Network Status: HIGH CONGESTION"
    )

elif total_queue > 100:

    st.warning(
        "🟡 Network Status: MODERATE CONGESTION"
    )

else:

    st.success(
        "🟢 Network Status: NORMAL"
    )

# ==================================================
# MULTI AGENT NETWORK
# ==================================================

st.subheader(
    "🚦 Multi-Agent Traffic Network (9 Signals)"
)

agents = [
    "A0", "A1", "A2",
    "B0", "B1", "B2",
    "C0", "C1", "C2"
]

cols = st.columns(3)

for i, agent in enumerate(agents):

    with cols[i % 3]:

        st.markdown(
            f"### 🚦 {agent}"
        )

        if mode == "COOPERATIVE_MARL":

            st.success(
                "🟢 COOPERATIVE"
            )

        elif mode == "DIGITAL_TWIN":

            st.warning(
                "🟠 DIGITAL TWIN"
            )

        else:

            st.error(
                "🔴 INDEPENDENT"
            )

        st.metric(
            "Queue",
            agent_data[agent]["queue"]
        )

        st.metric(
            "Wait",
            f"{int(agent_data[agent]['wait'])} s"
        )

        st.metric(
            "Phase",
            agent_data[agent]["phase"]
        )


# ==================================================
# MARL DECISION PANEL
# ==================================================


with open(
        "dashboard/controller_status.txt",
        "r",
        encoding="utf-8-sig"
    ) as f:

        mode = f.read().strip()
# ==================================================
# DECISION PANEL
# ==================================================

if mode == "COOPERATIVE_MARL":

    st.subheader("🤖 MARL Agent Decisions")

    actions = get_actions()

    for tls in agents:

        action = actions.get(
            tls,
            "KEEP"
        )

        if action == "SWITCH":

            st.warning(
                f"🚦 {tls} → SWITCH"
            )

        else:

            st.success(
                f"🚦 {tls} → KEEP"
            )


elif mode == "DIGITAL_TWIN":

    st.subheader(
        "🔮 Digital Twin Predicted Decisions"
    )

    actions = get_actions()

    for tls in agents:

        action = actions.get(
            tls,
            "KEEP"
        )

        if action == "SWITCH":

            st.info(
                f"🔮 {tls} → PREDICT SWITCH"
            )

        else:

            st.success(
                f"🔮 {tls} → PREDICT KEEP"
            )


elif mode == "INDEPENDENT_AGENT":

    st.subheader(
        "⚠ Independent Agent Mode"
    )

    st.warning(
        "Communication failed. Each intersection operates independently."
    )
# ==================================================
# TOP CONGESTED INTERSECTIONS
# ==================================================

st.subheader("🏆 Top Congested Intersections")

sorted_tls = sorted(
    agent_data.items(),
    key=lambda x: (
        x[1]["queue"],
        x[1]["wait"]
    ),
    reverse=True
)

for rank, (tls, data) in enumerate(
    sorted_tls[:3],
    start=1
):

    st.warning(
        f"#{rank} {tls} | Queue={data['queue']} | Wait={int(data['wait'])}s"
    )
# ==================================================
# EFFICIENCY
# ==================================================

efficiency_score = max(
    0,
    min(
        100,
        100 - ((total_queue / 200) * 100)
    )
)

st.metric(
    "⚡ Network Efficiency Score",
    f"{efficiency_score:.0f}%"
)

if efficiency_score >= 80:
    st.success("🟢 Efficiency: GOOD")
elif efficiency_score >= 50:
    st.warning("🟡 Efficiency: MODERATE")
else:
    st.error("🔴 Efficiency: POOR")

# ==================================================
# PERFORMANCE SUMMARY
# ==================================================

st.subheader("📊 Evaluation Metrics")

c1, c2 = st.columns(2)

c1.metric(
    "Total Queue Length",
    f"{total_queue:.0f}"
)

c2.metric(
    "Total Waiting Time",
    f"{total_wait:.0f} s"
)

st.subheader("📈 Traffic Performance Summary")

st.write(
    f"""
• Total Queue Length: {total_queue}

• Average Queue Length: {avg_queue:.1f}

• Highest Congestion: {max_tls}

• Network Efficiency: {efficiency_score:.0f}%

• Active Intersections: {active_intersections}/{len(agent_data)}
"""
)

st.divider()

# ==================================================
# CONTROLLER STATUS
# ==================================================

st.subheader("🧠 Active Controller")

try:

    with open(
        "dashboard/controller_status.txt",
        "r",
        encoding="utf-8-sig"
    ) as f:

        mode = f.read().strip()

    if mode == "COOPERATIVE_MARL":

        st.success("🟢 COOPERATIVE_MARL")

    elif mode == "DIGITAL_TWIN":

        st.warning("🟠 DIGITAL_TWIN")

    elif mode == "INDEPENDENT_AGENT":

        st.error("🔴 INDEPENDENT_AGENT")

    else:

        st.error(f"Unknown Mode: {mode}")

except Exception as e:

    st.error("Controller status unavailable")
    st.write(str(e))

st.subheader("📡 Communication Status")

if mode == "COOPERATIVE_MARL":
    st.success("HEALTHY")

elif mode == "DIGITAL_TWIN":
    st.warning("DEGRADED")

elif mode == "INDEPENDENT_AGENT":
    st.error("FAILED")

st.divider()

# ==================================================
# SYSTEM FLOW
# ==================================================
st.subheader("🔄 System Flow")

if mode == "COOPERATIVE_MARL":

    st.success("""
SUMO
↓
State Extraction
↓
Communication Network
↓
Cooperative MARL
↓
Action Selection
↓
Traffic Signal Control
↓
Vehicle Movement
""")

elif mode == "DIGITAL_TWIN":

    st.warning("""
SUMO
↓
State Extraction
↓
Delayed Communication
↓
Digital Twin Prediction
↓
Predicted Actions
↓
Traffic Signal Control
↓
Vehicle Movement
""")

else:

    st.error("""
SUMO
↓
State Extraction
↓
Communication Failure
↓
Independent Agent
↓
Local Decision Making
↓
Traffic Signal Control
↓
Vehicle Movement
""")

st.divider()


# ==================================================
# NETWORK VIEW
# ==================================================

st.subheader("🌐 MARL Network Topology")

st.code("""
A0 ─ A1 ─ A2
│    │    │
B0 ─ B1 ─ B2
│    │    │
C0 ─ C1 ─ C2
""")


st.divider()

st.caption(
    "Traffic Digital Twin | SUMO + TraCI + MARL Dashboard"
)