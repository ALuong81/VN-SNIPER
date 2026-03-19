  from datetime import datetime


def send_report(sniper, market, sectors):

    print("\nSTEP 3: REPORT\n")

    print(f"📈 Trạng thái thị trường: {market.get('status','UNKNOWN')}")
    print(f"📊 Xu hướng thị trường: {market.get('trend','UNKNOWN')}")
    print(f"⏱ Nhịp thị trường: {market.get('phase','UNKNOWN')}")
    print(f"• Độ rộng thị trường: {market.get('breadth','UNKNOWN')}")
    print(f"• Tỷ lệ cổ phiếu tăng: {market.get('adv_ratio','0')}%\n")

    print("🔥 TOP NGÀNH MẠNH\n")

    for i, (sec, score) in enumerate(sectors, 1):
        print(f"{i}. {sec} ({round(score,2)})")

    print("\n------------------------------------\n")

    for i, s in enumerate(sniper, 1):

        print(f"🔹 Mục tiêu #{i}: {s['symbol']}\n")

        print(f"• Giá hiện tại: {round(s['close'].iloc[-1],2)}")
        print(f"• Giá vào dự kiến: {s.get('entry')}")
        print(f"• Mục tiêu chốt lời: {s.get('tp')}")
        print(f"• Cắt lỗ: {s.get('sl')}")

        print(f"• Ngành: {s.get('sector')}")
        print(f"• Cổ phiếu dẫn dắt ngành: {s.get('leader')}")
        print(f"• Xu hướng đa khung: {s.get('trend_multi_tf')}")
        print(f"• Khả năng bứt phá: {s.get('breakout_prob')}")
        print(f"• Trạng thái cung: {s.get('supply')}")
        print(f"• Mô hình AI: {s.get('ai_pattern')}")
        print(f"• Dòng tiền thông minh: {s.get('smart_money')}")
        print(f"• Dòng tiền cá voi: {s.get('whale')}")

        print(f"• Meta Score: {s.get('meta_score')}")
        print(f"• Sức mạnh tương đối: {s.get('rs')}")
        print(f"• Cảnh báo rủi ro: {s.get('risk')}")

        print()
