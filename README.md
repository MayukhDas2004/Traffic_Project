# ASPAR: Adaptive Secure and Predictive Autonomous Routing for Traffic Management

## Overview

ASPAR is a resilient multi-agent traffic signal control framework that combines:

- Cooperative MARL (PPO)
- Digital Twin prediction
- Independent Agent fallback
- Communication failure detection
- Real-time monitoring dashboard
- SUMO traffic simulation

## Features

- 9-intersection traffic network
- PPO-based multi-agent control
- Communication-aware mode switching
- Healthy / Degraded / Failed operation
- Live dashboard visualization
- Performance benchmarking

## Modes

### COOPERATIVE_MARL
Agents exchange information and use the trained PPO policy.

### DIGITAL_TWIN
Predicted traffic states are used when communication is degraded.

### INDEPENDENT_AGENT
Local decision-making when communication fails.

## Final Results

| Mode | Waiting Time | Queue Length | Throughput | Travel Time |
|------|------:|------:|------:|------:|
| COOPERATIVE_MARL | 36424.81 | 13.05 | 24 | 3881.47 |
| DIGITAL_TWIN | 36956.88 | 13.73 | 28 | 3821.41 |
| INDEPENDENT_AGENT | 37830.18 | 3.29 | 22 | 5140.54 |

## Run Controller

```powershell
python marl/marl_comm_controller.py