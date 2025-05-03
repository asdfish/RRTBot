# RRTBot

# Dependencies
 * [uv](https://github.com/astral-sh/uv)
 * [IB Gateway](https://www.interactivebrokers.com/en/trading/ib-gateway-download.php) *OR* [TWS](https://www.interactivebrokers.com/en/trading/tws-updateable-stable.php)

# Running
```sh
git clone https://github.com/Markville-Hack-Club/RRTBot.git --depth 1
cd RRTBot

# Run IB Gateway or TWS
# The specific host and port that you get may not be these values
export RRTBOT_IB_API_HOST="127.0.0.1"
export RRTBOT_IB_API_PORT="400"

uv run main.py
```
