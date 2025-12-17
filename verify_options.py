
import sys
from unittest.mock import MagicMock, AsyncMock
import asyncio

# Handle Mocking carefully to support class inheritance
class MockOptionsFlow:
    """Mock for config_entries.OptionsFlow."""
    def __init__(self):
        pass

mock_config_entries = MagicMock()
mock_config_entries.OptionsFlow = MockOptionsFlow
mock_config_entries.ConfigFlow = MockOptionsFlow # Also mock ConfigFlow base
sys.modules['homeassistant.config_entries'] = mock_config_entries

mock_ha = MagicMock()
sys.modules['homeassistant'] = mock_ha
sys.modules['homeassistant.core'] = MagicMock()
sys.modules['homeassistant.const'] = MagicMock()
sys.modules['homeassistant.helpers'] = MagicMock()
sys.modules['homeassistant.helpers.aiohttp_client'] = MagicMock()
sys.modules['homeassistant.helpers.update_coordinator'] = MagicMock()
sys.modules['homeassistant.data_entry_flow'] = MagicMock()

# Mock Voluptuous to allow Schema creation without error
class MockVol:
    def Schema(self, schema):
        return schema
    def Required(self, key, default=None):
        return key
mock_vol = MockVol()
sys.modules['voluptuous'] = mock_vol

# Import the code to test
from custom_components.fastlane_il import config_flow
from custom_components.fastlane_il import const

async def test_options_flow():
    print("Starting Options Flow Test...")
    
    # Mock Config Entry
    config_entry = MagicMock()
    config_entry.data = {const.CONF_SCAN_INTERVAL: 10}
    config_entry.options = {} 
    
    # Instantiate OptionsFlowHandler
    flow = config_flow.OptionsFlowHandler(config_entry)
    
    # Mock async_show_form to capture the result
    flow.async_show_form = MagicMock(return_value="FORM_SHOWN")
    
    try:
        # Call async_step_init
        result = await flow.async_step_init()
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"CRASH: Options Flow crashed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_options_flow())
