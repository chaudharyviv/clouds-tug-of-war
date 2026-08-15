from src.models.combatant import Champion, FactionType
from src.models.battlefield import Battlefield
from typing import List

# List of 10 Battle Dimensions
BATTLE_DIMENSIONS = [
    "Raw Scale & Gravity",
    "AI / GPU War Power",
    "Economic Blood Cost",
    "Operational Simplicity",
    "Service Depth & Ecosystem",
    "Lock-in vs Freedom",
    "Sovereign Control & Data Residency",
    "Edge / Locality Power",
    "Resilience & Global Reach",
    "Speed of Innovation / Specialization"
]

# 5 MVP Battlefields and their default dimension weights
BATTLEFIELDS: List[Battlefield] = [
    Battlefield(
        name="AI Training Killing Fields",
        description="A volcanic plain of molten silicon and infinite matrix multiplications where only sheer GPU density and specialized AI frameworks survive.",
        rewards="GPU density, performance, specialized stacks",
        suffers="Generalist empires & pure edge",
        dimension_weights={
            "AI / GPU War Power": 2.5,
            "Speed of Innovation / Specialization": 1.5,
            "Raw Scale & Gravity": 1.0,
            "Service Depth & Ecosystem": 1.0,
            "Economic Blood Cost": 0.8
        }
    ),
    Battlefield(
        name="Cost Wasteland",
        description="A barren, resource-starved desert where margins are razor-thin and every drop of compute costs blood. High markup empires wither here.",
        rewards="Aggressive unit economics, low cost-per-token/VM",
        suffers="Premium gravity wells and high lock-in ecosystems",
        dimension_weights={
            "Economic Blood Cost": 2.5,
            "Operational Simplicity": 1.5,
            "Lock-in vs Freedom": 1.5,
            "Raw Scale & Gravity": 0.5,
            "Service Depth & Ecosystem": 0.5
        }
    ),
    Battlefield(
        name="Lock-in Swamp",
        description="A thick, suffocating marshland of proprietary APIs, complex ingress/egress tariffs, and contract chains. Only those built for freedom can escape.",
        rewards="Exit ability, open-source compatibility, standards",
        suffers="Deep ecosystem empires with complex multi-service reliance",
        dimension_weights={
            "Lock-in vs Freedom": 2.5,
            "Operational Simplicity": 1.5,
            "Economic Blood Cost": 1.0,
            "Service Depth & Ecosystem": 0.5,
            "Resilience & Global Reach": 0.8
        }
    ),
    Battlefield(
        name="Sovereignty Fortress",
        description="An iron-walled citadel governed by strict national boundaries, shielding walls of compliance, and data residency laws.",
        rewards="Data residency, national control, local compliance shields",
        suffers="Global hyperscalers with centralized data routing",
        dimension_weights={
            "Sovereign Control & Data Residency": 2.5,
            "Resilience & Global Reach": 1.2,
            "Lock-in vs Freedom": 1.0,
            "Raw Scale & Gravity": 0.5,
            "Service Depth & Ecosystem": 0.5
        }
    ),
    Battlefield(
        name="Edge Ambush Terrain",
        description="A fractured, chaotic skirmish ground of thousands of micro-nodes. Communication paths are thin, and millisecond latency is a lethal dagger.",
        rewards="Ultra-low local latency, localized execution, distributed robustness",
        suffers="Centralized cloud giants and heavy control-plane dependencies",
        dimension_weights={
            "Edge / Locality Power": 2.5,
            "Operational Simplicity": 1.5,
            "Speed of Innovation / Specialization": 1.2,
            "Resilience & Global Reach": 1.0,
            "Raw Scale & Gravity": 0.3
        }
    )
]

# 10-14 Champion Templates covering all 5 Factions
DEFAULT_CHAMPIONS: List[Champion] = [
    # Hyperscalers
    Champion(
        name="AWS",
        faction=FactionType.HYPERSCALERS,
        description="The First God, Lord of the Infinite Bill, Master of Gravitational Lock-in."
    ),
    Champion(
        name="Azure",
        faction=FactionType.HYPERSCALERS,
        description="The Enterprise Titan, Wielder of Hybrid Pacts and Compliance Shields."
    ),
    Champion(
        name="GCP",
        faction=FactionType.HYPERSCALERS,
        description="The Data & AI Oracle, Keeper of the Deep Analytics Flame."
    ),
    
    # NeoClouds
    Champion(
        name="CoreWeave",
        faction=FactionType.NEOCLOUDS,
        description="The GPU Berserker, Blade of the NeoCloud Rebellion."
    ),
    Champion(
        name="Lambda Labs",
        faction=FactionType.NEOCLOUDS,
        description="The Developer's Assassin, fast-striking GPU on-demand host."
    ),
    Champion(
        name="Crusoe",
        faction=FactionType.NEOCLOUDS,
        description="The Energy Warlock, converting stranded clean energy into clean compute fire."
    ),
    
    # Sovereign / Regional
    Champion(
        name="OVHcloud",
        faction=FactionType.SOVEREIGN_REGIONAL,
        description="The European Shield, defender of data residency and anti-Cloud Act sovereignty."
    ),
    Champion(
        name="Sovereign Sovereign",
        faction=FactionType.SOVEREIGN_REGIONAL,
        description="A specialized national cloud fortress with absolute data isolation."
    ),
    
    # Distributed / Edge
    Champion(
        name="Cloudflare",
        faction=FactionType.DISTRIBUTED_EDGE,
        description="The Edge Shadow Raider, dispatching worker threads globally in milliseconds."
    ),
    Champion(
        name="Vercel",
        faction=FactionType.DISTRIBUTED_EDGE,
        description="The Frontend Phantom, weaving seamless global localizations."
    ),
    
    # Private / On-Prem
    Champion(
        name="Old Fortress On-Prem",
        faction=FactionType.PRIVATE_ON_PREM,
        description="The Old Castle, protecting ancient databases behind miles of physical copper and cooling towers."
    )
]
