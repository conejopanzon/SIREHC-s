from PIL import Image, ImageDraw, ImageFont

def create_medical_background():
    """Crea una imagen de fondo con temática médica"""
    width, height = 500, 600
    img = Image.new('RGB', (width, height), color='#E8F4F8')
    draw = ImageDraw.Draw(img)
    
    # Colores
    primary_color = '#1F6E78'
    accent_color = '#E74C3C'
    light_color = '#FFFFFF'
    
    # Círculo decorativo grande (arriba)
    draw.ellipse([50, 30, 150, 130], outline=primary_color, width=3)
    
    # Símbolo de caduceo médico (simplificado)
    # Línea vertical central
    draw.line([(width//2, 150), (width//2, 280)], fill=primary_color, width=3)
    
    # Serpientes (círculos)
    draw.ellipse([(width//2-40, 160), (width//2-20, 180)], outline=accent_color, width=2)
    draw.ellipse([(width//2+20, 160), (width//2+40, 180)], outline=accent_color, width=2)
    draw.ellipse([(width//2-40, 260), (width//2-20, 280)], outline=accent_color, width=2)
    draw.ellipse([(width//2+20, 260), (width//2+40, 280)], outline=accent_color, width=2)
    
    # Cruz roja (símbolo médico)
    cross_x = width // 2
    cross_y = 360
    draw.rectangle([cross_x-15, cross_y-35, cross_x+15, cross_y+35], fill=accent_color)
    draw.rectangle([cross_x-35, cross_y-15, cross_x+35, cross_y+15], fill=accent_color)
    
    # Líneas decorativas
    draw.line([(30, 450), (width-30, 450)], fill=primary_color, width=2)
    draw.line([(30, 460), (width-30, 460)], fill=primary_color, width=2)
    
    # Rectángulos pequeños decorativos (abajo)
    for i in range(5):
        x = 50 + (i * 80)
        draw.rectangle([x, 490, x+30, 530], outline=primary_color, width=2)
    
    img.save('medical_bg.png')
    print("✓ Imagen médica generada: medical_bg.png")

if __name__ == '__main__':
    create_medical_background()
