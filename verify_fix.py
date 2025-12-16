
import sys
import types
from unittest.mock import MagicMock

# Mock homeassistant modules
mock_ha = MagicMock()
sys.modules['homeassistant'] = mock_ha
sys.modules['homeassistant.config_entries'] = MagicMock()
sys.modules['homeassistant.core'] = MagicMock()
sys.modules['homeassistant.const'] = MagicMock()
sys.modules['homeassistant.helpers'] = MagicMock()
sys.modules['homeassistant.helpers.aiohttp_client'] = MagicMock()
sys.modules['homeassistant.helpers.update_coordinator'] = MagicMock()
sys.modules['homeassistant.helpers.entity_platform'] = MagicMock()
sys.modules['homeassistant.components'] = MagicMock()
sys.modules['homeassistant.components.sensor'] = MagicMock()
sys.modules['homeassistant.data_entry_flow'] = MagicMock()
sys.modules['voluptuous'] = MagicMock()

# Now try to import the custom component
try:
    from custom_components.fastlane_il import config_flow
    import custom_components.fastlane_il as fastlane_il_module
    
    print("Successfully imported modules.")
    
    if hasattr(config_flow, 'FastlaneConfigFlow'):
        print("PASS: FastlaneConfigFlow class found.")
    else:
        print("FAIL: FastlaneConfigFlow class NOT found.")
        
    if hasattr(fastlane_il_module, 'async_setup'):
        print("PASS: async_setup function found.")
    else:
        print("FAIL: async_setup function NOT found.")
        print(f"DEBUG: Contents of module: {dir(fastlane_il_module)}")

except ImportError as e:
    print(f"FAIL: ImportError: {e}")
except Exception as e:
    print(f"FAIL: Unexpected error: {e}")
