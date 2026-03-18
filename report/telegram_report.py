def send_report(sniper, market, sectors):

    print(f"""
📈 Trạng thái thị trường: {market["status"]}
📊 Xu hướng thị trường: {market["trend"]}
⏱ Nhịp thị trường: {market["timing"]}
• Độ rộng thị trường: {market["breadth"]}
• Tỷ lệ cổ phiếu tăng: {market["ratio"]}%

🔥 TOP NGÀNH MẠNH
""")

    for i, (sec, val) in enumerate(sectors, 1):
        print(f"{i}. {sec} ({round(val,2)})")

    print("\n------------------------------------")

    for i, s in enumerate(sniper, 1):

        price = round(s["close"].iloc[-1], 2)

        print(f"""
🔹 Mục tiêu #{i}: {s["symbol"]}

• Giá hiện tại: {price}
• Giá vào dự kiến: {round(price*1.01,2)}
• Mục tiêu chốt lời: {round(price*1.2,2)}
• Cắt lỗ: {round(price*0.92,2)}
• Trạng thái: THEO DÕI - THỊ TRƯỜNG XẤU
• Ngành: {s["sector"]}
• Cổ phiếu dẫn dắt ngành: CÓ
• Xu hướng đa khung: {s["trend_multi_tf"]}
• Khả năng bứt phá: {s["breakout_prob"]}
• Trạng thái cung: {s["supply"]}
• Mô hình VCP: {s["vcp"]}
• Mô hình AI: {s["ai_pattern"]}
• Dòng tiền tổ chức: {s["smart_money"]}
• Dòng tiền thông minh: {s["smart_money"]}
• Super Breakout: {s["super_breakout"]}
• Early Breakout: {s["early_breakout"]}
• Dòng tiền cá voi: {s["whale"]}
• Super Stock: {s["super_stock"]}
• Xếp hạng: {s["rank"]}
• Meta Score: {s["meta_score"]}
• Sức mạnh tương đối: {s["rs"]}
• Cảnh báo rủi ro: {s["risk"]}
""")
