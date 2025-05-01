# RRTBot

# Dependencies
 * [uv](https://github.com/astral-sh/uv)
 * [IB Gateway](https://www.interactivebrokers.com/en/trading/ib-gateway-download.php)

# Running
```sh
git clone https://github.com/Markville-Hack-Club/RRTBot.git --depth 1
cd RRTBot

# Run IB Gateway
# Change "127.0.0.0:100" to the socket that IB Gateway gives you
export RRTBOT_IB_GATEWAY_SOCKET="127.0.0.0:100"

uv run main.rs
```
