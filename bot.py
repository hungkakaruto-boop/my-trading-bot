import telebot
import pandas_ta as ta
import time
from datetime import datetime, timedelta
import pytz
from vnstock import *

# --- THÔNG TIN CỦA BẠN ---
TOKEN = '8625301702:AAHLOJgz_fIkfA6WpU7Sr60KjRIzc7nmHR4'
CHAT_ID = '1736294695'

bot = telebot.TeleBot('8625301702:AAHLOJgz_fIkfA6WpU7Sr60KjRIzc7nmHR4')
vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')

# DANH SÁCH 120 MÃ TỔNG HỢP
WATCHLIST = [
    'ACB', 'BCM', 'BID', 'BVH', 'CTG', 'FPT', 'GAS', 'GVR', 'HDB', 'HPG', 
    'MBB', 'MSN', 'MWG', 'PLX', 'POW', 'SAB', 'SHB', 'SSB', 'SSI', 'STB', 
    'TCB', 'TPB', 'VCB', 'VHM', 'VIB', 'VIC', 'VNM', 'VPB', 'VRE', 'VJC',
    'DGC', 'DXG', 'DIG', 'PDR', 'NLG', 'KDH', 'KBC', 'GEX', 'VND', 'VCI', 
    'HCM', 'HSG', 'NKG', 'PVD', 'PVT', 'PC1', 'DBC', 'ANV', 'VHC', 'TCH', 
    'HAG', 'HHV', 'LCG', 'FCN', 'VGC', 'DPM', 'DCM', 'FRT', 'CTR', 'DGW',
    'REE', 'SCS', 'EIB', 'MSB', 'LPB', 'OCB', 'PNJ', 'SAM', 'VIX', 'GMD',
    'PVS', 'SHS', 'IDC', 'CEO', 'NTP', 'MBS', 'VCS', 'DTD', 'TNG', 'L14',
    'VGI', 'ACV', 'VEA', 'MCH', 'BSR', 'CSI', 'VTP', 'FOX', 'LTG', 'QNS',
    'ABB', 'BVB', 'NAB', 'VAB', 'KLB', 'OIL', 'PVC', 'DDV', 'VGT', 'SSH'
]

def soi_keo(s):
    try:
        start_date = (datetime.now(vn_tz) - timedelta(days=100)).strftime('%Y-%m-%d')
        df = stock_historical_data(symbol=s, start_date=start_date, resolution='1D', type='stock')
        if df is None or df.empty or len(df) < 30: return

        df['MA20'] = ta.sma(df['close'], length=20)
        vol_avg = df['volume'].tail(20).mean()
        curr = df.iloc[-1]
        prev = df.iloc[-2]
        
        tr_high = df['high'].tail(30).max()
        tr_low = df['low'].tail(30).min()

        msg = ""
        # 1. Bùng nổ SOS
        if curr['close'] > tr_high and curr['volume'] > vol_avg * 1.5:
            msg = f"🔥 **{s}: SOS - BREAKOUT MẠNH**\n📈 Giá: {curr['close']:,.0f}\n📊 Vol: {curr['volume']/vol_avg:.1f}x TB"
            
        # 2. Rũ bỏ Spring
        elif prev['low'] < tr_low and curr['close'] > tr_low and curr['volume'] < vol_avg:
            msg = f"💎 **{s}: SPRING - RŨ BỎ**\n✅ Điểm mua: {curr['close']:,.0f}\n🛡 Dừng lỗ: {curr['low']:,.0f}"

        if msg:
            if s == 'PC1': msg += "\n💡 *Lưu ý: Mốc giá vốn hiện tại đang ở 26.5*"
            bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
    except:
        pass

# --- LOGIC CHẠY TRÊN GITHUB ---
print("🚀 Bot bắt đầu chạy trên máy chủ GitHub...")
bot.send_message(CHAT_ID, "✅ Bot đã On-air trên Cloud! Bắt đầu quét liên tục đến 15h00.")

while True:
    now = datetime.now(vn_tz)
    
    # Nếu đến 15:00 (Hết phiên), tự động ngắt Bot để GitHub hoàn thành công việc
    if now.hour >= 15:
        bot.send_message(CHAT_ID, "🛑 Đã 15h00, hết phiên giao dịch. Bot tự động nghỉ ngơi đến sáng mai!")
        print("Hết giờ giao dịch. Kết thúc tiến trình.")
        break
    
    print(f"⏰ Đang quét 120 mã lúc {now.strftime('%H:%M')}...")
    for s in WATCHLIST:
        soi_keo(s)
        time.sleep(1) # Chờ 1s mỗi mã để không lỗi dữ liệu
        
    print("--- Xong 1 vòng. Nghỉ 10 phút... ---")
    time.sleep(600) # Nghỉ 10 phút rồi quét lại vòng mới
