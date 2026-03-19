def send_report(sniper, market, sectors):

    print("\n📈 Trạng thái thị trường:", market["status"])
    print("📊 Xu hướng thị trường:", market["trend"])
    print("⏱ Nhịp thị trường:", market["phase"])
    print("• Độ rộng thị trường:", market["breadth"])
    print("• Tỷ lệ cổ phiếu tăng:", f'{market["advancers"]:.1f}%')

    print("\n🔥 TOP NGÀNH MẠNH")
    for i, (name, score) in enumerate(sectors[:3], 1):
        print(f"{i}. {name} ({round(score,2)})")

    print("\n------------------------------------")

    for i, s in enumerate(sniper, 1):

        print(f"\n🔹 Mục tiêu #{i}: {s['symbol']}")

        print(f"""
• Giá hiện tại: {round(s['close'].iloc[-1],2)}
• Giá vào dự kiến: {s.get("entry")}
• Mục tiêu chốt lời: {s.get("tp")}
• Cắt lỗ: {s.get("sl")}
• Trạng thái: {s.get("action","THEO DÕI")}
• Ngành: {s.get("sector")}
• Cổ phiếu dẫn dắt ngành: {s.get("leader")}
• Xu hướng đa khung: {s.get("trend_multi_tf")}
• Khả năng bứt phá: {s.get("breakout_prob")}
• Trạng thái cung: {s.get("supply")}
• Mô hình VCP: {s.get("vcp")}
• Mô hình AI: {s.get("ai_pattern")}
• Dòng tiền tổ chức: {s.get("smart_money")}
• Dòng tiền thông minh: {s.get("smart_money")}
• Super Breakout: {s.get("super_breakout")}
• Early Breakout: {s.get("early_breakout")}
• Dòng tiền cá voi: {s.get("whale")}
• Super Stock: {s.get("super_stock")}
• Xếp hạng: {s.get("rank")}
• Meta Score: {s.get("meta_score")}
• Sức mạnh tương đối: {s.get("rs")}
• Cảnh báo rủi ro: {s.get("risk")}
""")

    print("\n✅ DONE")
