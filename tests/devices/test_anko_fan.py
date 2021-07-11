from homeassistant.components.fan import (
    SUPPORT_OSCILLATE,
    SUPPORT_PRESET_MODE,
    SUPPORT_SET_SPEED,
)

from homeassistant.const import STATE_UNAVAILABLE

from ..const import ANKO_FAN_PAYLOAD
from ..helpers import assert_device_properties_set
from .base_device_tests import TuyaDeviceTestCase

SWITCH_DPS = "1"
PRESET_DPS = "2"
SPEED_DPS = "3"
OSCILLATE_DPS = "4"
TIMER_DPS = "6"


class TestAnkoFan(TuyaDeviceTestCase):
    __test__ = True

    def setUp(self):
        self.setUpForConfig("anko_fan.yaml", ANKO_FAN_PAYLOAD)
        self.subject = self.entities["fan"]

    def test_supported_features(self):
        self.assertEqual(
            self.subject.supported_features,
            SUPPORT_OSCILLATE | SUPPORT_PRESET_MODE | SUPPORT_SET_SPEED,
        )

    def test_is_on(self):
        self.dps[SWITCH_DPS] = True
        self.assertTrue(self.subject.is_on)

        self.dps[SWITCH_DPS] = False
        self.assertFalse(self.subject.is_on)

        self.dps[SWITCH_DPS] = None
        self.assertEqual(self.subject.is_on, STATE_UNAVAILABLE)

    async def test_turn_on(self):
        async with assert_device_properties_set(
            self.subject._device, {SWITCH_DPS: True}
        ):
            await self.subject.async_turn_on()

    async def test_turn_off(self):
        async with assert_device_properties_set(
            self.subject._device, {SWITCH_DPS: False}
        ):
            await self.subject.async_turn_off()

    def test_preset_mode(self):
        self.dps[PRESET_DPS] = "normal"
        self.assertEqual(self.subject.preset_mode, "normal")

        self.dps[PRESET_DPS] = "nature"
        self.assertEqual(self.subject.preset_mode, "nature")

        self.dps[PRESET_DPS] = "sleep"
        self.assertEqual(self.subject.preset_mode, "sleep")

        self.dps[PRESET_DPS] = None
        self.assertIs(self.subject.preset_mode, None)

    def test_preset_modes(self):
        self.assertCountEqual(self.subject.preset_modes, ["normal", "nature", "sleep"])

    async def test_set_preset_mode_to_normal(self):
        async with assert_device_properties_set(
            self.subject._device,
            {PRESET_DPS: "normal"},
        ):
            await self.subject.async_set_preset_mode("normal")

    async def test_set_preset_mode_to_nature(self):
        async with assert_device_properties_set(
            self.subject._device,
            {PRESET_DPS: "nature"},
        ):
            await self.subject.async_set_preset_mode("nature")

    async def test_set_preset_mode_to_sleep(self):
        async with assert_device_properties_set(
            self.subject._device,
            {PRESET_DPS: "sleep"},
        ):
            await self.subject.async_set_preset_mode("sleep")

    def test_oscillating(self):
        self.dps[OSCILLATE_DPS] = False
        self.assertFalse(self.subject.oscillating)

        self.dps[OSCILLATE_DPS] = True
        self.assertTrue(self.subject.oscillating)

        self.dps[OSCILLATE_DPS] = None
        self.assertFalse(self.subject.oscillating)

    async def test_oscillate_off(self):
        async with assert_device_properties_set(
            self.subject._device, {OSCILLATE_DPS: "off"}
        ):
            await self.subject.async_oscillate(False)

    async def test_oscillate_on(self):
        async with assert_device_properties_set(
            self.subject._device, {OSCILLATE_DPS: "auto"}
        ):
            await self.subject.async_oscillate(True)

    def test_speed(self):
        self.dps[PRESET_DPS] = "normal"
        self.dps[SPEED_DPS] = "4"
        self.assertEqual(self.subject.percentage, 50)

    def test_speed_step(self):
        self.assertEqual(self.subject.percentage_step, 12.5)
        self.assertEqual(self.subject.speed_count, 8)

    async def test_set_speed_in_normal_mode(self):
        self.dps[PRESET_DPS] = "normal"
        async with assert_device_properties_set(self.subject._device, {SPEED_DPS: 2}):
            await self.subject.async_set_percentage(25)

    async def test_set_speed_in_normal_mode_snaps(self):
        self.dps[PRESET_DPS] = "normal"
        async with assert_device_properties_set(self.subject._device, {SPEED_DPS: 6}):
            await self.subject.async_set_percentage(80)

    def test_device_state_attributes(self):
        self.dps[TIMER_DPS] = "5"
        self.assertEqual(self.subject.device_state_attributes, {"timer": 5})
