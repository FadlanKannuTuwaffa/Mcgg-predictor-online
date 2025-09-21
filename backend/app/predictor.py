import random
from typing import List, Tuple

def generate_one_pairing(players: List[str]) -> dict:
    names = players[:]
    random.shuffle(names)
    paired = {}
    used = set()
    for name in names:
        if name in used: continue
        partner = None
        for cand in names:
            if cand != name and cand not in used:
                partner = cand
                break
        if partner:
            paired[name] = partner
            paired[partner] = name
            used.add(name); used.add(partner)
        else:
            paired[name] = 'CLONE'; used.add(name)
    return paired

def montecarlo_predict(target: str, players: List[str], sims: int=500) -> List[Tuple[str,float]]:
    counts={}
    for _ in range(max(1,sims)):
        p = generate_one_pairing(players)
        opp = p.get(target, 'CLONE')
        counts[opp] = counts.get(opp,0) + 1
    total = sum(counts.values())
    items = [(k, v/total) for k,v in counts.items() if k!='CLONE']
    items.sort(key=lambda x: x[1], reverse=True)
    return items[:2]