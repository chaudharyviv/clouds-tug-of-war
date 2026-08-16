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
        primary_dimensions={
            "AI / GPU War Power": 3.0,
            "Speed of Innovation / Specialization": 2.0
        },
        secondary_dimensions={
            "Raw Scale & Gravity": 1.0
        },
        tactical_rule="Demonstrated specialized GPU/accelerator infrastructure earns Tactical Advantage.",
        comeback_profile="high"
    ),
    Battlefield(
        name="Cost Wasteland",
        description="A barren, resource-starved desert where margins are razor-thin and every drop of compute costs blood. High markup empires wither here.",
        rewards="Aggressive unit economics, low cost-per-token/VM",
        suffers="Premium gravity wells and high lock-in ecosystems",
        primary_dimensions={
            "Economic Blood Cost": 3.0
        },
        secondary_dimensions={
            "Operational Simplicity": 1.5,
            "Lock-in vs Freedom": 1.0
        },
        tactical_rule="Demonstrated lower sustainable unit economics earns Tactical Advantage.",
        comeback_profile="low"
    ),
    Battlefield(
        name="Lock-in Swamp",
        description="A thick, suffocating marshland of proprietary APIs, complex ingress/egress tariffs, and contract chains. Only those built for freedom can escape.",
        rewards="Exit ability, open-source compatibility, standards",
        suffers="Deep ecosystem empires with complex multi-service reliance",
        primary_dimensions={
            "Lock-in vs Freedom": 3.0
        },
        secondary_dimensions={
            "Economic Blood Cost": 1.5,
            "Operational Simplicity": 1.25
        },
        tactical_rule="Demonstrated ability to escape proprietary dependencies without architectural pain earns Tactical Advantage.",
        comeback_profile="medium"
    ),
    Battlefield(
        name="Sovereignty Fortress",
        description="An iron-walled citadel governed by strict national boundaries, shielding walls of compliance, and data residency laws.",
        rewards="Data residency, national control, local compliance shields",
        suffers="Global hyperscalers with centralized data routing",
        primary_dimensions={
            "Sovereign Control & Data Residency": 3.0
        },
        secondary_dimensions={
            "Resilience & Global Reach": 1.5,
            "Lock-in vs Freedom": 1.0
        },
        tactical_rule="Demonstrated local control and data-residency capabilities earn Tactical Advantage.",
        comeback_profile="medium"
    ),
    Battlefield(
        name="Edge Ambush Terrain",
        description="A fractured, chaotic skirmish ground of thousands of micro-nodes. Communication paths are thin, and millisecond latency is a lethal dagger.",
        rewards="Ultra-low local latency, localized execution, distributed robustness",
        suffers="Centralized cloud giants and heavy control-plane dependencies",
        primary_dimensions={
            "Edge / Locality Power": 3.0
        },
        secondary_dimensions={
            "Operational Simplicity": 1.5,
            "Speed of Innovation / Specialization": 1.25,
            "Resilience & Global Reach": 1.0
        },
        tactical_rule="Demonstrated ability to execute workloads close to users/devices earns Tactical Advantage.",
        comeback_profile="very_high"
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
        name="Scaleway",
        faction=FactionType.SOVEREIGN_REGIONAL,
        description="The Republic's Compute Marshal, fielding multi-cloud infrastructure entirely on EU soil, beyond the reach of US extraterritorial law."
    ),
    Champion(
        name="STACKIT",
        faction=FactionType.SOVEREIGN_REGIONAL,
        description="The Schwarz Group's Sovereign Vault, a German-built cloud fortress forged for corporate and public-sector workloads that cannot leave home jurisdiction."
    ),
    Champion(
        name="T Cloud Public",
        faction=FactionType.SOVEREIGN_REGIONAL,
        description="Deutsche Telekom's Compliance Warden, staffed EU-only and bound to BSI C5 certification for government and heavily regulated workloads."
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
    Champion(
        name="Akamai",
        faction=FactionType.DISTRIBUTED_EDGE,
        description="The Old Sentinel of the Wire, warding traffic through the Akamai Connected Cloud's globally dispersed edge and security mesh since before the others were born."
    ),
    
    # Private / On-Prem
    Champion(
        name="OpenShift",
        faction=FactionType.PRIVATE_ON_PREM,
        description="Red Hat's Kubernetes Warlord, commanding containerized legions across any datacenter that will host it, hyperscaler or bare metal alike."
    ),
    Champion(
        name="Exadata",
        faction=FactionType.PRIVATE_ON_PREM,
        description="Oracle's Engineered Colossus, a purpose-built database fortress fusing hardware and software into one immovable on-prem siege engine."
    )
]
