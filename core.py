"""光伏电站核心逻辑：组件、日照、储能和逆变器。"""

import json


def new_game():
    return {
        "panels": {},
        "storage": 0,
        "storage_capacity": 100,
        "generation": 0,
        "weather": "sunny",
        "meter_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    state["meter_id"] += 1
    return state


def connect(state, panel_id):
    state["panels"][panel_id] = True
    state["storage"] += 10
    return True


def generate(state, amount):
    state["generation"] += amount
    state["storage"] += amount
    return True


def storage_by_count(state):
    return len(state["panels"])


def cancel_connect(state, panel_id):
    return True


def shade(state):
    state["generation"] -= 5
    state["generation"] -= 5
    return state["generation"]


def main():
    print("光伏电站 - 命令: connect/generate/storage/cancel/shade/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
