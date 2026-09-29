"""光伏电站核心逻辑：组件、日照、储能和逆变器。"""

import json

CONNECT_CHARGE = 10
SHADE_LOSS = 5
FIXED_CLOCK = "12:00"


def new_game():
    return {
        "panels": {},
        "storage": 0,
        "storage_capacity": 100,
        "generation": 0,
        "weather": "sunny",
        "night": False,
        "inverter_fault": False,
        "clock": FIXED_CLOCK,
        "meter_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    base = new_game()
    for key, value in base.items():
        state.setdefault(key, value)
    return state


def _clamp_storage(state):
    capacity = state.get("storage_capacity", 0)
    state["storage"] = max(0, min(state["storage"], capacity))


def connect(state, panel_id):
    if not panel_id or panel_id in state["panels"]:
        return False
    state["panels"][panel_id] = True
    state["storage"] += CONNECT_CHARGE
    _clamp_storage(state)
    return True


def generate(state, amount):
    if amount <= 0:
        return False
    if state.get("night"):
        return False
    if state.get("inverter_fault"):
        return False
    if state.get("weather") != "sunny":
        return False
    state["generation"] += amount
    state["storage"] += amount
    _clamp_storage(state)
    return True


def storage_by_count(state):
    return state["storage"]


def cancel_connect(state, panel_id):
    if panel_id not in state["panels"]:
        return False
    del state["panels"][panel_id]
    state["storage"] -= CONNECT_CHARGE
    _clamp_storage(state)
    return True


def shade(state):
    state["generation"] -= SHADE_LOSS
    return state["generation"]


def main():
    print("光伏电站 - 命令: connect/generate/storage/cancel/shade/save/load/quit")
    state = new_game()
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw:
            print("空命令，请重新输入")
            continue
        parts = raw.split()
        cmd, args = parts[0], parts[1:]
        if cmd == "quit":
            break
        elif cmd == "connect" and len(args) == 1:
            print("ok" if connect(state, args[0]) else "组件已并网或编号非法")
        elif cmd == "generate" and len(args) == 1:
            try:
                amount = int(args[0])
            except ValueError:
                print("发电量必须是整数")
                continue
            print("ok" if generate(state, amount) else "当前条件不允许发电")
        elif cmd == "storage" and not args:
            print(storage_by_count(state))
        elif cmd == "cancel" and len(args) == 1:
            print("ok" if cancel_connect(state, args[0]) else "组件未并网")
        elif cmd == "shade" and not args:
            print(state["generation"] if shade(state) is not None else "ok")
        elif cmd == "save" and not args:
            print(save_state(state))
        elif cmd == "load" and len(args) == 1:
            try:
                state = load_state(args[0])
            except (ValueError, TypeError):
                print("存档数据非法")
                continue
            print("ok")
        else:
            print("未知命令")


if __name__ == "__main__":
    main()
