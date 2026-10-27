# Science Lab upgrades (0.6.1)

All numbers below were chosen by Brad unless marked ASSUMPTION.

## Tiers
- Three Lab upgrade tiers, bought with supplies only and built over time.
- Tier 1: 100 supplies, 2:00. Tier 2: 250 supplies, 5:00. Tier 3: 500 supplies, 10:00.
- Each tier gives +5% research pace, -5% project cost and -5% rush cost, cumulative (tier 3 is +15%, -15%, -15%).
- Project slots: 1 at tier 0 and tier 1, 2 at tier 2, 3 at tier 3.

## Construction
- Only one Lab upgrade is built at a time. The Lab is offline while it is built: no project can start and running projects are paused.
- Rush is disabled while the Lab is offline.

## Parallel projects
- Projects run in parallel up to the slot count. They share one pool of research points and supplies.
- A scientist on station speeds one slot each: the 15% time cut applies to the first N projects, where N is the number of Lab staff on station (ASSUMPTION: same definition as before, so a Linguist on station counts like a Scientist).
- Only one Gate Room project at a time. The same Armory item cannot be researched twice. Each MALP upgrades one at a time.

## Effect math
- Pace: project time is divided by (1 + 0.05 x tier) (ASSUMPTION: pace read as speed, so tier 3 is 1.15x speed).
- Project cost: research points and supplies of new projects (MALP tiers, Gate Room research, Armory and alien tech research) are reduced by 5% per tier, rounded (ASSUMPTION: applies to both resources). Purchases after research (Gate Room install, Armory units, vehicles, Tel'tak fee) are not discounted.
- Rush: research points per minute remaining multiplied by (1 - 0.05 x tier).
- Tollan perk stacks multiplicatively with all of the above.
