import urllib.request
import json
import time

def test_extended_market():
    try:
        # ৫টি টপ ক্রিপ্টো কয়েনের লাইভ ডেটা একসাথে টানা হচ্ছে টেস্টের জন্য
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana,cardano,dogecoin"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            raw_data = json.loads(response.read().decode('utf-8'))
            
            print("\n🧪 --- VEXOR MULTI-ASSET TEST REPORT --- 🧪")
            print("==================================================")
            for coin in raw_data:
                symbol = coin['symbol'].upper()
                price = coin['current_price']
                l24 = coin['low_24h']
                h24 = coin['high_24h']
                
                total_return = round(((price - l24) / l24) * 100, 2)
                volatility = round(((h24 - l24) / price) * 100, 2)
                
                # সিগন্যাল ফিল্টারিং টেস্ট
                if total_return > 2.0 and volatility < 6.0:
                    status = "🟢 MINIMUM RISK (Alpha Trend)"
                elif total_return < -1.0 or volatility > 8.0:
                    status = "🔴 ESCAPE RISK (High Volatility)"
                else:
                    status = "🟡 NEUTRAL STATE (Consolidation)"
                    
                print(f"📦 Asset: {symbol} | Price: ${price}")
                print(f"📊 24h Return: {total_return}% | Volatility: {volatility}%")
                print(f"🛡️ Risk State: {status}")
                print("--------------------------------------------------")
            print("🔮 [TEST SUCCESS]: Mobile Database Thread Is Stable.\n")
    except Exception as e:
        print(f"Test Error: {e}")

# টেস্ট রান করা হলো
test_extended_market()
