from datetime import datetime
import pytz

def convert_utc_to_cairo(utc_datetime):
    """تحويل التوقيت من UTC إلى توقيت القاهرة"""
    if utc_datetime is None:
        return None
    
    # تعيين المنطقة الزمنية لمصر (القاهرة)
    cairo_tz = pytz.timezone('Africa/Cairo')
    utc_tz = pytz.UTC
    
    # إذا كان التاريخ لا يحتوي على معلومات المنطقة الزمنية، نعتبره UTC
    if utc_datetime.tzinfo is None:
        utc_datetime = utc_tz.localize(utc_datetime)
    
    # تحويل إلى توقيت القاهرة
    cairo_datetime = utc_datetime.astimezone(cairo_tz)
    return cairo_datetime

def format_cairo_datetime(utc_datetime, format_string='%Y-%m-%d %H:%M'):
    """تنسيق التاريخ والوقت بتوقيت القاهرة"""
    if utc_datetime is None:
        return 'غير محدد'
    
    cairo_datetime = convert_utc_to_cairo(utc_datetime)
    return cairo_datetime.strftime(format_string)

def get_current_cairo_time():
    """الحصول على الوقت الحالي بتوقيت القاهرة"""
    cairo_tz = pytz.timezone('Africa/Cairo')
    return datetime.now(cairo_tz)

def format_relative_time(utc_datetime):
    """عرض الوقت النسبي بالعربية (منذ كم دقيقة/ساعة/يوم)"""
    if utc_datetime is None:
        return 'غير محدد'
    
    cairo_datetime = convert_utc_to_cairo(utc_datetime)
    now_cairo = get_current_cairo_time()
    
    diff = now_cairo - cairo_datetime
    
    if diff.days > 0:
        if diff.days == 1:
            return 'منذ يوم واحد'
        elif diff.days < 7:
            return f'منذ {diff.days} أيام'
        elif diff.days < 30:
            weeks = diff.days // 7
            return f'منذ {weeks} أسبوع' if weeks == 1 else f'منذ {weeks} أسابيع'
        else:
            return cairo_datetime.strftime('%Y-%m-%d')
    
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    
    if hours > 0:
        return f'منذ {hours} ساعة' if hours == 1 else f'منذ {hours} ساعات'
    elif minutes > 0:
        return f'منذ {minutes} دقيقة' if minutes == 1 else f'منذ {minutes} دقائق'
    else:
        return 'منذ لحظات'