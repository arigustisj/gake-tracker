#!/usr/bin/env python3
"""
Gake Wallet Tracker - Real-time Solana Memecoin Trading Monitor
Monitors Gake's wallet and sends intelligent Telegram notifications
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
GAKE_WALLET = "DNfuF1L62WWyW3pNakVkyGGFzVVhj4Yr52jSmdTyeBHm"
SOLANA_RPC = os.getenv("SOLANA_RPC", "https://api.mainnet-beta.solana.com")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY", "")

# Cache untuk tracking
transaction_cache = set()
token_positions = {}
last_check_time = None

class GakeTracker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        
    def get_recent_transactions(self, limit=20) -> List[Dict]:
        """Get recent transactions from Solana using Helius/QuickNode API"""
        try:
            # Using public Solana RPC
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getSignaturesForAddress",
                "params": [
                    GAKE_WALLET,
                    {"limit": limit}
                ]
            }
            
            response = self.session.post(SOLANA_RPC, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if "result" in result:
                    return result["result"]
            
            logger.warning(f"Failed to fetch transactions: {response.status_code}")
            return []
            
        except Exception as e:
            logger.error(f"Error fetching transactions: {e}")
            return []
    
    def get_transaction_details(self, signature: str) -> Optional[Dict]:
        """Get detailed transaction information"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTransaction",
                "params": [
                    signature,
                    {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}
                ]
            }
            
            response = self.session.post(SOLANA_RPC, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if "result" in result and result["result"]:
                    return result["result"]
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching transaction details: {e}")
            return None
    
    def analyze_transaction(self, tx_data: Dict) -> Optional[Dict]:
        """Analyze transaction to detect buy/sell/rebuy"""
        try:
            if not tx_data or not tx_data.get("transaction"):
                return None
            
            meta = tx_data.get("meta", {})
            message = tx_data["transaction"]["message"]
            
            # Check for token transfers
            pre_balances = meta.get("preTokenBalances", [])
            post_balances = meta.get("postTokenBalances", [])
            
            # Detect token changes
            for post in post_balances:
                mint = post.get("mint")
                if not mint:
                    continue
                
                # Find corresponding pre balance
                pre = next((p for p in pre_balances if p.get("mint") == mint), None)
                
                pre_amount = float(pre.get("uiTokenAmount", {}).get("uiAmount", 0)) if pre else 0
                post_amount = float(post.get("uiTokenAmount", {}).get("uiAmount", 0))
                
                delta = post_amount - pre_amount
                
                if abs(delta) > 0:
                    action = "BUY" if delta > 0 else "SELL"
                    
                    return {
                        "action": action,
                        "token_mint": mint,
                        "amount": abs(delta),
                        "signature": tx_data.get("transaction", {}).get("signatures", [""])[0] if isinstance(tx_data.get("transaction", {}).get("signatures"), list) else "",
                        "timestamp": datetime.fromtimestamp(tx_data.get("blockTime", time.time()))
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error analyzing transaction: {e}")
            return None
    
    def get_token_info(self, mint_address: str) -> Dict:
        """Get token information from Birdeye or DexScreener"""
        try:
            # Try Birdeye first if API key available
            if BIRDEYE_API_KEY:
                url = f"https://public-api.birdeye.so/public/token_overview?address={mint_address}"
                headers = {"X-API-KEY": BIRDEYE_API_KEY}
                response = self.session.get(url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        token_data = data.get("data", {})
                        return {
                            "symbol": token_data.get("symbol", "UNKNOWN"),
                            "name": token_data.get("name", "Unknown Token"),
                            "market_cap": token_data.get("mc", 0),
                            "price": token_data.get("price", 0),
                            "liquidity": token_data.get("liquidity", 0)
                        }
            
            # Fallback to DexScreener
            url = f"https://api.dexscreener.com/latest/dex/tokens/{mint_address}"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                pairs = data.get("pairs", [])
                
                if pairs:
                    pair = pairs[0]  # Get first/main pair
                    return {
                        "symbol": pair.get("baseToken", {}).get("symbol", "UNKNOWN"),
                        "name": pair.get("baseToken", {}).get("name", "Unknown Token"),
                        "market_cap": pair.get("marketCap", 0),
                        "price": float(pair.get("priceUsd", 0)),
                        "liquidity": pair.get("liquidity", {}).get("usd", 0),
                        "dexscreener_url": pair.get("url", "")
                    }
            
            return {
                "symbol": "UNKNOWN",
                "name": "Unknown Token",
                "market_cap": 0,
                "price": 0,
                "liquidity": 0
            }
            
        except Exception as e:
            logger.error(f"Error fetching token info: {e}")
            return {
                "symbol": "UNKNOWN",
                "name": "Unknown Token",
                "market_cap": 0,
                "price": 0,
                "liquidity": 0
            }
    
    def calculate_entry_timing(self, action: str, token_info: Dict, timestamp: datetime) -> Dict:
        """Calculate optimal entry timing based on Gake's action"""
        now = datetime.now()
        time_since_action = (now - timestamp).total_seconds() / 60  # in minutes
        
        mc = token_info.get("market_cap", 0)
        
        if action == "BUY":
            if time_since_action < 10:
                recommendation = "🔴 DON'T BUY YET"
                reason = "Copy trader pump expected. Wait for dip."
                optimal_entry = "Wait 30-90 minutes for first dip (-20-40%)"
                risk_level = "EXTREME"
            elif 10 <= time_since_action < 30:
                recommendation = "🟡 WATCH CLOSELY"
                reason = "Initial pump phase. Wait for consolidation."
                optimal_entry = "Enter on dip at 30-90 min mark"
                risk_level = "HIGH"
            elif 30 <= time_since_action < 120:
                recommendation = "🟢 OPTIMAL ENTRY ZONE"
                reason = "First dip window. Good entry point."
                optimal_entry = "BUY 30-50% position NOW"
                risk_level = "MEDIUM"
            elif 120 <= time_since_action < 360:
                recommendation = "🟢 GOOD ENTRY"
                reason = "Consolidation phase. Confirmed trend."
                optimal_entry = "BUY 50-70% position"
                risk_level = "MEDIUM"
            else:
                recommendation = "🟡 CHASE RISK"
                reason = "Late to the party. Higher risk."
                optimal_entry = "Small position only (20-30%)"
                risk_level = "HIGH"
        
        elif action == "SELL":
            sell_percentage = self.estimate_sell_percentage(mc, time_since_action)
            
            if sell_percentage >= 50:
                recommendation = "🔴 EXIT NOW"
                reason = f"Gake selling {sell_percentage}%! Distribution phase."
                optimal_entry = "SELL 50-80% immediately"
                risk_level = "EXTREME"
            elif sell_percentage >= 30:
                recommendation = "🟠 CONSIDER EXIT"
                reason = f"Gake taking profits ({sell_percentage}%)"
                optimal_entry = "SELL 30-50% to lock gains"
                risk_level = "HIGH"
            else:
                recommendation = "🟡 PARTIAL EXIT"
                reason = f"Gake first exit ({sell_percentage}%)"
                optimal_entry = "SELL 20-30% to secure profits"
                risk_level = "MEDIUM"
        
        else:  # REBUY
            recommendation = "🟢 STRONG BUY SIGNAL"
            reason = "Gake re-entering = high conviction!"
            optimal_entry = "BUY 50-70% position within 5-15 min"
            risk_level = "LOW-MEDIUM"
        
        return {
            "recommendation": recommendation,
            "reason": reason,
            "optimal_entry": optimal_entry,
            "risk_level": risk_level,
            "time_since_action": round(time_since_action, 1)
        }
    
    def estimate_sell_percentage(self, market_cap: float, time_minutes: float) -> int:
        """Estimate Gake's sell percentage based on market cap and timing"""
        if market_cap < 1_000_000:
            return 20  # Small cap, likely small exit
        elif market_cap < 5_000_000:
            if time_minutes < 60:
                return 25  # Quick partial exit
            else:
                return 35  # Delayed exit, bigger chunk
        elif market_cap < 15_000_000:
            return 40  # Major exit zone
        else:
            return 50  # Peak, major distribution
    
    def send_telegram_alert(self, trade_data: Dict, token_info: Dict, timing_analysis: Dict):
        """Send formatted alert to Telegram"""
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            logger.warning("Telegram credentials not configured")
            return
        
        try:
            action = trade_data["action"]
            symbol = token_info.get("symbol", "UNKNOWN")
            name = token_info.get("name", "Unknown")
            mc = token_info.get("market_cap", 0)
            price = token_info.get("price", 0)
            liquidity = token_info.get("liquidity", 0)
            
            # Format market cap
            if mc >= 1_000_000:
                mc_str = f"${mc/1_000_000:.2f}M"
            elif mc >= 1_000:
                mc_str = f"${mc/1_000:.1f}K"
            else:
                mc_str = f"${mc:.0f}"
            
            # Format liquidity
            if liquidity >= 1_000_000:
                liq_str = f"${liquidity/1_000_000:.2f}M"
            elif liquidity >= 1_000:
                liq_str = f"${liquidity/1_000:.1f}K"
            else:
                liq_str = f"${liquidity:.0f}"
            
            # Build message
            emoji = "🟢" if action == "BUY" else "🔴" if action == "SELL" else "🔄"
            
            message = f"""
{emoji} <b>GAKE {action} ALERT!</b> {emoji}

💎 <b>Token:</b> ${symbol} ({name})
🔗 <b>Mint:</b> <code>{trade_data['token_mint'][:8]}...{trade_data['token_mint'][-8:]}</code>

📊 <b>Market Data:</b>
├ Market Cap: {mc_str}
├ Price: ${price:.8f}
└ Liquidity: {liq_str}

⏰ <b>Timing:</b> {timing_analysis['time_since_action']} min ago

{timing_analysis['recommendation']}

<b>Analysis:</b>
{timing_analysis['reason']}

<b>Recommended Action:</b>
{timing_analysis['optimal_entry']}

<b>Risk Level:</b> {timing_analysis['risk_level']}

🔍 <a href="https://dexscreener.com/solana/{trade_data['token_mint']}">DexScreener</a> | <a href="https://solscan.io/token/{trade_data['token_mint']}">Solscan</a>

⚠️ <b>Remember:</b>
• DON'T blindly copy trade
• Use stop loss (-20%)
• Take profits gradually
• DYOR before entry

<i>Powered by Gake Tracker v1.0</i>
"""
            
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message.strip(),
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            }
            
            response = self.session.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Telegram alert sent successfully for {action} {symbol}")
            else:
                logger.error(f"Failed to send Telegram alert: {response.text}")
                
        except Exception as e:
            logger.error(f"Error sending Telegram alert: {e}")
    
    def check_for_rebuy(self, token_mint: str, action: str) -> bool:
        """Check if this is a rebuy (buying token previously sold)"""
        if action != "BUY":
            return False
        
        # Check if token exists in positions history
        if token_mint in token_positions:
            last_action = token_positions[token_mint].get("last_action")
            if last_action == "SELL":
                return True
        
        return False
    
    def monitor_wallet(self):
        """Main monitoring loop"""
        logger.info(f"🚀 Starting Gake Wallet Monitor for: {GAKE_WALLET}")
        logger.info(f"📱 Telegram notifications: {'Enabled' if TELEGRAM_BOT_TOKEN else 'Disabled'}")
        
        while True:
            try:
                transactions = self.get_recent_transactions(limit=10)
                
                for tx in transactions:
                    sig = tx.get("signature")
                    
                    # Skip if already processed
                    if sig in transaction_cache:
                        continue
                    
                    # Add to cache
                    transaction_cache.add(sig)
                    
                    # Get transaction details
                    tx_details = self.get_transaction_details(sig)
                    
                    if not tx_details:
                        continue
                    
                    # Analyze transaction
                    trade_data = self.analyze_transaction(tx_details)
                    
                    if not trade_data:
                        continue
                    
                    # Check for rebuy
                    is_rebuy = self.check_for_rebuy(
                        trade_data["token_mint"],
                        trade_data["action"]
                    )
                    
                    if is_rebuy:
                        trade_data["action"] = "REBUY"
                        logger.info(f"🔄 REBUY detected for {trade_data['token_mint']}")
                    
                    # Get token information
                    token_info = self.get_token_info(trade_data["token_mint"])
                    
                    # Calculate timing analysis
                    timing_analysis = self.calculate_entry_timing(
                        trade_data["action"],
                        token_info,
                        trade_data["timestamp"]
                    )
                    
                    # Log the action
                    logger.info(
                        f"{trade_data['action']} detected: "
                        f"{token_info['symbol']} @ ${token_info['market_cap']/1_000_000:.2f}M MC"
                    )
                    
                    # Send Telegram alert
                    self.send_telegram_alert(trade_data, token_info, timing_analysis)
                    
                    # Update position tracking
                    token_positions[trade_data["token_mint"]] = {
                        "last_action": trade_data["action"],
                        "timestamp": trade_data["timestamp"],
                        "market_cap": token_info["market_cap"]
                    }
                
                # Clean old cache (keep last 100 transactions)
                if len(transaction_cache) > 100:
                    transaction_cache.clear()
                
                # Wait before next check (30 seconds for responsiveness)
                time.sleep(30)
                
            except KeyboardInterrupt:
                logger.info("Monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
                time.sleep(60)  # Wait longer on error

def main():
    """Main entry point"""
    
    # Validate environment variables
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("⚠️ TELEGRAM_BOT_TOKEN not set. Notifications disabled.")
    
    if not TELEGRAM_CHAT_ID:
        logger.warning("⚠️ TELEGRAM_CHAT_ID not set. Notifications disabled.")
    
    # Start tracker
    tracker = GakeTracker()
    tracker.monitor_wallet()

if __name__ == "__main__":
    main()
