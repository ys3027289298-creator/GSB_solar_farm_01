"""光伏电站核心逻辑：组件、日照、储能和逆变器。"""

import json

CONNECT_CHARGE = 10
SHADE_LOSS = 5


def new_game():
    return {
        "panels": {},
        "storage": 0,
        "storage_capacity": 100,
        "generation": 0,
        "weather": "sunny",
        "meter_id": 0,
        "tick": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    if not text or not text.strip():
        raise ValueError("empty save data")
    return json.loads(text)


def _commit(state):
    state["tick"] = state.get("tick", 0) + 1


def connect(state, panel_id):
    if not panel_id or panel_id in state["panels"]:
        return False
    if state["storage"] + CONNECT_CHARGE > state["storage_capacity"]:
        return False
    state["panels"][panel_id] = True
    state["storage"] += CONNECT_CHARGE
    _commit(state)
    return True


def generate(state, amount):
    if amount <= 0:
        return False
    if state.get("weather") != "sunny":
        return False
    if state.get("inverter_fault"):
        return False
    if state.get("night"):
        return False
    state["generation"] += amount
    state["storage"] = min(state["storage"] + amount, state["storage_capacity"])
    _commit(state)
    return True


def storage_by_count(state):
    return state["storage"]


def cancel_connect(state, panel_id):
    if panel_id not in state["panels"]:
        return False
    del state["panels"][panel_id]
    state["storage"] = max(0, state["storage"] - CONNECT_CHARGE)
    _commit(state)
    return True


def shade(state):
    state["generation"] -= SHADE_LOSS
    _commit(state)
    return state["generation"]


def main():
    state = new_game()
    print("光伏电站 - 命令: connect <id> / generate <n> / storage / cancel <id> / shade / save / load / quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw:
            continue
        parts = raw.split()
        cmd, args = parts[0], parts[1:]
        if cmd == "quit":
            break
        elif cmd == "connect" and len(args) == 1:
            print("ok" if connect(state, args[0]) else "rejected: duplicate or invalid panel")
        elif cmd == "generate" and len(args) == 1:
            try:
                amount = int(args[0])
            except ValueError:
                print("rejected: amount must be an integer")
                continue
            print("ok" if generate(state, amount) else "rejected: cannot generate now")
        elif cmd == "storage" and not args:
            print("storage:", storage_by_count(state))
        elif cmd == "cancel" and len(args) == 1:
            print("ok" if cancel_connect(state, args[0]) else "rejected: unknown panel")
        elif cmd == "shade" and not args:
            print("generation:", shade(state))
        elif cmd == "save" and not args:
            print(save_state(state))
        elif cmd == "load" and args:
            try:
                state = load_state(" ".join(args))
            except (ValueError, json.JSONDecodeError):
                print("rejected: invalid save data")
            else:
                print("ok")
        else:
            print("rejected: unknown command")
    print("bye")


if __name__ == "__main__":
    main()
