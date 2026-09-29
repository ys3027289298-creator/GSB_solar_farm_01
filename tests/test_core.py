import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_connect(self):
        state = core.new_game()
        self.assertTrue(core.connect(state, "P1"))
        self.assertFalse(core.connect(state, "P1"))

    def test_02_no_generate_on_cloudy(self):
        state = core.new_game()
        state["weather"] = "cloudy"
        result = core.generate(state, 10)
        self.assertFalse(result)

    def test_03_storage_by_capacity(self):
        state = core.new_game()
        state["storage"] = 50
        self.assertEqual(core.storage_by_count(state), 50)

    def test_04_cancel_connect_refunds(self):
        state = core.new_game()
        core.connect(state, "P1")
        core.cancel_connect(state, "P1")
        self.assertEqual(state["storage"], 0)

    def test_05_no_generate_on_fault(self):
        state = core.new_game()
        state["inverter_fault"] = True
        result = core.generate(state, 10)
        self.assertFalse(result)

    def test_06_shade_once(self):
        state = core.new_game()
        core.shade(state)
        self.assertEqual(state["generation"], -5)

    def test_07_no_generate_at_night(self):
        state = core.new_game()
        state["night"] = True
        result = core.generate(state, 10)
        self.assertFalse(result)

    def test_08_load_preserves_meter(self):
        state = core.new_game()
        state["meter_id"] = 8
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["meter_id"], 8)


if __name__ == "__main__":
    unittest.main()
