import telebot
import pandas_ta as ta
import time
from datetime import datetime, timedelta
import pytz # Thư viện xử lý múi giờ Việt Nam
from vnstock import *

# --- THÔNG TIN CỦA BẠN ---
TOKEN = '8625301702:AAHLOJgz_fIkfA6WpU7Sr60KjRIzc7nmHR4'
CHAT_ID = '1736294695'

# DANH SÁCH 120 MÃ (VN100 + HNX + UPCOM)
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

bot = telebot.TeleBot(' 8625301702:AAHLOJgz_fIkfA6WpU7Sr60KjRIzc7nmHR4')
vn_tz = pytz.timezone('Asia/Ho_Chi_Minh') # Cài đặt múi giờ Việt Nam

def check_trading_time():
    now = datetime.now(vn_tz)
    # Kiểm tra từ thứ 2 đến thứ 6 (0-4) và từ 9h00 đến 14h59
    if now.weekday() < 5 and 9 <= now.hour < 15:
        return True
    return False

def soi_keo_phien_chinh(s):
    try:
        start_date = (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d')
        df = stock_historical_data(symbol=s, start_date=start_date, resolution='1D', type='stock')
        if df is None or df.empty: return

        df['MA20'] = ta.sma(df['close'], length=20)
        vol_avg = df['volume'].tail(20).mean()
        curr = df.iloc[-1]
        tr_high = df['high'].tail(30).max()
        tr_low = df['low'].tail(30).min()

        msg = ""
        if curr['close'] > tr_high and curr['volume'] > vol_avg * 1.5:
            msg = f"🔥 **{s}: SOS - BREAKOUT**\n📈 Giá: {curr['close']:,.0f}\n📊 Vol: {curr['volume']/vol_avg:.1f}x TB"
        elif curr['low'] < tr_low and curr['close'] > tr_low and curr['volume'] < vol_avg:
            msg = f"💎 **{s}: SPRING - RŨ BỎ**\n✅ Mua: {curr['close']:,.0f}\n🛡 Dừng lỗ: {curr['low']:,.0f}"

        if msg:
            if s == 'PC1': msg += "\n💡 *Giá vốn: 26.5*"
            bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
    except:
        pass

# --- KHỞI ĐỘNG ---
print("🤖 Bot Wyckoff đã sẵn sàng...")
bot.send_message(CHAT_ID, "✅ Bot đã kích hoạt chế độ trực chiến 9h - 15h!")

while True:
    if check_trading_time():
        print(f"⏰ Đang trong giờ giao dịch ({datetime.now(vn_tz).strftime('%H:%M')}). Quét 120 mã...")
        for s in WATCHLIST:
            soi_keo_phien_chinh(s)
            time.sleep(0.7)
        print("--- Xong 1 vòng. Nghỉ 5 phút ---")
        time.sleep(300) 
    else:
        now_str = datetime.now(vn_tz).strftime('%H:%M')
        print(f"😴 Ngoài giờ giao dịch ({now_str}). Bot đang ngủ đông...")
        # Nếu đang ngoài giờ, cứ 30 phút bot mới kiểm tra lại một lần để đỡ tốn pin/mạng
        time.sleep(1800) 
