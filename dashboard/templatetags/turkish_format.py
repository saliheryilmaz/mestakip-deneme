from django import template

register = template.Library()

@register.filter(name='turkish_format')
def turkish_format(value):
    """
    Sayıyı Türkçe formatta gösterir: 18.400,00
    Binlik ayırıcı: nokta (.)
    Ondalık ayırıcı: virgül (,)
    """
    if value is None:
        return '0,00'
    
    try:
        # Decimal veya float'ı float'a çevir
        if hasattr(value, '__float__'):
            num = float(value)
        else:
            num = float(value)
        
        # Negatif işareti kontrol et
        is_negative = num < 0
        num = abs(num)
        
        # İki ondalık basamakla formatla
        num_str = f"{num:.2f}"
        
        # Nokta ve virgülü ayır
        parts = num_str.split('.')
        integer_part = parts[0]
        decimal_part = parts[1] if len(parts) > 1 else '00'
        
        # Binlik ayırıcıları ekle (nokta ile) - sağdan sola 3'er 3'er
        if len(integer_part) > 3:
            # Sağdan sola 3'er 3'er ayır
            formatted_parts = []
            for i in range(len(integer_part), 0, -3):
                start = max(0, i - 3)
                formatted_parts.insert(0, integer_part[start:i])
            integer_part = '.'.join(formatted_parts)
        
        # Virgül ile birleştir
        result = f"{integer_part},{decimal_part}"
        
        # Negatif işareti ekle
        if is_negative:
            result = f"-{result}"
        
        return result
    except (ValueError, TypeError, AttributeError):
        return str(value) if value else '0,00'

