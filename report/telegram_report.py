from datetime import datetime

def send_report(sniper, market):

    now = datetime.now().strftime("%d-%m-%Y %H:%M")

    print(f"""
🎯 HỆ THỐNG RADA – BÁO CÁO SNIPER
🕒 {now}
📈 {market["status"]}
📊 {market["trend"]}
""")

    for i, s in enumerate(sniper, 1):

        print(f"""
🔹 #{i}: {s["symbol"]}

Giá: {round(s["close"].iloc[-1],2)}
Entry: {s["entry"]}
Target: {s["target"]}
Stop: {s["stop"]}
Score: {s["sniper_score"]}
""")
