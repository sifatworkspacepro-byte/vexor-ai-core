from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import json
import os

class VexorServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana,cardano,dogecoin"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                raw_data = json.loads(response.read().decode('utf-8'))
                
                report = []
                for coin in raw_data:
                    symbol = coin['symbol'].upper()
                    price = coin['current_price']
                    l24 = coin['low_24h'] if coin['low_24h'] else price
                    h24 = coin['high_24h'] if coin['high_24h'] else price
                    
                    total_return = round(((price - l24) / l24) * 100, 2) if l24 else 0
                    volatility = round(((h24 - l24) / price) * 100, 2) if price else 0
                    
                    if total_return > 2.0 and volatility < 6.0:
                        status = "🟢 MINIMUM RISK (Alpha Trend)"
                    elif total_return < -1.0 or volatility > 8.0:
                        status = "🔴 ESCAPE RISK (High Volatility)"
                    else:
                        status = "🟡 NEUTRAL STATE (Consolidation)"
                        
                    report.append({
                        "asset": symbol,
                        "price": price,
                        "return_24h": f"{total_return}%",
                        "volatility": f"{volatility}%",
                        "risk_state": status
                    })
                
                # স্ক্রিনে সুন্দর JSON ডাটা দেখাবে
                response_data = {"status": "SUCCESS", "engine": "VEXOR AI CORE v13.0", "data": report}
                self.wfile.write(json.dumps(response_data, indent=4).encode('utf-8'))
                
        except Exception as e:
            self.wfile.write(json.dumps({"status": "ERROR", "message": str(e)}).encode('utf-8'))

def run():
    # রেন্ডার সার্ভার যে পোর্ট দেবে, আমাদের অ্যাপ সেই পোর্টে চালু হবে
    port = int(os.environ.get("PORT", 10000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, VexorServer)
    print(f"🚀 Vexor AI Core Web Server Running on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
              
