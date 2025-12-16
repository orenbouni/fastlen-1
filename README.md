# Fastlane IL Home Assistant Integration

This custom integration scrapes the current price from [Fastlane.co.il](https://fastlane.co.il/) and exposes it as a sensor in Home Assistant.

## Installation

### Step 1: Copy Files
1.  Access your Home Assistant configuration directory (usually `/config`). You can use the "File Editor" add-on or Samba Share.
2.  Navigate to the `custom_components` folder. If it doesn't exist, create it.
3.  Create a new folder inside `custom_components` named `fastlane_il`.
4.  Copy all the files from this repository's `custom_components/fastlane_il` folder into your new `fastlane_il` folder.

   **Structure test should look like this :**
   ```
   /config/custom_components/fastlane_il/
   ├── __init__.py
   ├── manifest.json
   ├── sensor.py
   ├── config_flow.py
   ├── const.py
   ├── scraper.py
   ├── strings.json
   └── translations/
       └── en.json
   ```

### Step 2: oren to test Restart Home Assistant
1.  Go to **Developer Tools** > **YAML** > **Check Configuration** to make sure everything is safe.
2.  Click **Restart** (or **Restart Home Assistant**).

### Step 3: Add Integration
1.  Once Home Assistant is back online, go to **Settings** > **Devices & Services**.
2.  Click the **+ ADD INTEGRATION** button in the bottom right.
3.  Search for **Fastlane IL**.
4.  Click it to add. You can optionally set the **Update frequency (minutes)** (default is 5 minutes).
5.  Click **Submit**.

---

## 📱 Creating a Dashboard Card

To display the price on your dashboard:

1.  Go to your Dashboard (Overview).
2.  Click the **Pencil icon** (Edit Dashboard) in the top right.
3.  Click **+ ADD CARD**.
4.  Select the **Entities** card (or **Gauge** for a visual represention).
5.  In the "Entities" list, remove the defaults and select `sensor.fastlane_price`.
6.  Click **Save**.

### Example YAML for a Gauge Card
If you prefer identifying the price quickly with colors (e.g., green for cheap, red for expensive):

1.  Click **+ ADD CARD**.
2.  Scroll down to **Manual** (at the very bottom).
3.  Paste the following code:

```yaml
type: gauge
entity: sensor.fastlane_price
name: Fastlane Price
unit: ₪
min: 0
max: 100
needle: true
segments:
  - from: 0
    color: green
  - from: 20
    color: orange
  - from: 50
    color: red
```
4. Click **Save**.
