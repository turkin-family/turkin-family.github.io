# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw, ImageFont

CARDS = [
    {
        'filename': '1646_ГАВО_ф1260_д633_Афанасий_Василий_Туркины_побои_попа.jpg',
        'thumb': 'thumb_1646_ГАВО_ф1260_д633.jpg',
        'year': '1646 ГОД',
        'badge': 'ГАВО • ФОНД 1260 • ОПИСЬ 1 • ДЕЛО 633',
        'title_lines': [
            'ДЕЛО ПО ЧЕЛОБИТНОЙ СВЯЩЕННИКА ГАВРИИЛА КОСТРОМИНА',
            'О побоях и брани со стороны Афанасия и Василия Туркиных'
        ],
        'vol': '16 ЛИСТОВ • СУД ВОЛОГОДСКОГО АРХИЕПИСКОПА МАРКЕЛЛА',
        'quote': '«...били и бранили введенского священника Гавриила на Усть-Выми...»',
        'meta_left': [
            ('Истец:', 'Священник Гавриил Костромин'),
            ('Ответчики:', 'Афанасий С. Туркин, Василий Туркин'),
            ('Третья сторона:', 'Степан Ефимьев (захват земли)'),
            ('Судья:', 'Архиепископ Вологодский Маркелл'),
            ('Волость:', 'Оквадская и Усть-Вымская')
        ],
        'meta_right': [
            ('Тип дела:', 'Судебное следственное дело (16 л.)'),
            ('Статус рода:', 'Светская власть и влияние на Выми'),
            ('Родство:', 'Союз Афанасия и Василия Туркиных'),
            ('Хранение:', 'БАУ ВО «ГАВО», г. Вологда')
        ]
    },
    {
        'filename': '1646_ГАВО_ф1260_д635_Афанасий_Туркин_мирской_долг_75руб.jpg',
        'thumb': 'thumb_1646_ГАВО_ф1260_д635.jpg',
        'year': '1646 ГОД',
        'badge': 'ГАВО • ФОНД 1260 • ОПИСЬ 1 • ДЕЛО 635',
        'title_lines': [
            'СУДНОЕ ДЕЛО ПРИКАЗНОГО ДЬЯКА АНДРЕЯ ПАЛИЦЫНА',
            'О взыскании с Афанасия Туркина 75 рублей мирского долга'
        ],
        'vol': '3 ЛИСТА • МИРСКИЕ РАСХОДЫ КРЕСТЬЯНСКОЙ ОБЩИНЫ',
        'quote': '«...о взыскании с оквадских крестьян Афанасия Туркина с товарыщи 75 рублей...»',
        'meta_left': [
            ('Истец:', 'Приказный дьяк Андрей Палицын'),
            ('Ответчик (глава):', 'Афанасий Семёнович Туркин'),
            ('Соответчики:', 'Опара Иванов, Козьма Пономарев и др.'),
            ('Сумма иска:', '75 рублей серебром (на мирские нужды)'),
            ('Суд:', 'Архиепископ Вологодский Маркелл')
        ],
        'meta_right': [
            ('Тип дела:', 'Финансово-долговое судное дело'),
            ('Статус рода:', 'Распорядитель мирской казны волости'),
            ('Эквивалент:', 'Стоимость стада из 50 дойных коров'),
            ('Хранение:', 'БАУ ВО «ГАВО», г. Вологда')
        ]
    },
    {
        'filename': '1664_ГАВО_ф1260_д2347_Архип_Афанасий_Туркины_отпись_допрос.jpg',
        'thumb': 'thumb_1664_ГАВО_ф1260_д2347.jpg',
        'year': '1656–1664 ГГ.',
        'badge': 'ГАВО • ФОНД 1260 • ОПИСЬ 1 • ДЕЛО 2347',
        'title_lines': [
            'ОТПИСЬ АФАНАСИЯ ТУРКИНА И ДОПРОС СЫНА АРХИПА',
            'Раздел двора, отпускная память и отказ в содержании отца'
        ],
        'vol': '2 ЛИСТА • ЦЕРКОВНЫЙ ЗАКАЗЧИК МИХАИЛ КОНСТАНТИНОВ',
        'quote': '«...дал отпускную память, корову, 100 аршин холста и 15 руб. денег...»',
        'meta_left': [
            ('Истец (1664 г.):', 'Афанасий Семёнович Туркин (отец)'),
            ('Ответчик:', 'Архип Афанасьевич Туркин (сын)'),
            ('Допрашивал:', 'Заказчик Михаил Константинов'),
            ('Акт 06.10.1656:', 'Отпись отца на выдел (15 руб., корова)'),
            ('Суть иска:', 'Требование пожизненного кормления')
        ],
        'meta_right': [
            ('Тип дела:', 'Семейно-имущественное следствие'),
            ('Предыстория:', 'Сургутское дело о 347 рублях'),
            ('Значение:', 'Точная дата разъезда семей (1656 г.)'),
            ('Хранение:', 'БАУ ВО «ГАВО», г. Вологда')
        ]
    },
    {
        'filename': '1667_ГАВО_ф1260_д2913_Афанасий_Туркин_челобитная_на_Архипа_и_Исаака.jpg',
        'thumb': 'thumb_1667_ГАВО_ф1260_д2913.jpg',
        'year': '1667 ГОД',
        'badge': 'ГАВО • ФОНД 1260 • ОПИСЬ 1 • ДЕЛО 2913',
        'title_lines': [
            'ЧЕЛОБИТНАЯ АФАНАСИЯ ТУРКИНА НА АРХИПА И ИСААКА',
            'Семейный раскол: сыновья забрали деньги и отказали отцу в пище'
        ],
        'vol': '11 ЛИСТОВ • СУД ВОЛОГОДСКОГО АРХИЕПИСКОПА СИМОНА',
        'quote': '«...на детей его, Архипа и Исака, которые не кормят его и взяли деньги...»',
        'meta_left': [
            ('Истец:', 'Афанасий Семёнович Туркин (~70 лет)'),
            ('Ответчики (сыновья):', 'Архип Туркин и Исаак Туркин'),
            ('Третья сторона:', 'Крестьянка Фёкла М. Жужгина (земля)'),
            ('Следователи:', 'Приказные Г. Патракеев, П. Озеров'),
            ('Судья:', 'Архиепископ Вологодский Симон')
        ],
        'meta_right': [
            ('Тип дела:', 'Епархиальное следственное дело (11 л.)'),
            ('Суть конфликта:', 'Захват семейной казны сыновьями'),
            ('Значение:', 'Союз братьев Архипа и Исаака'),
            ('Хранение:', 'БАУ ВО «ГАВО», г. Вологда')
        ]
    },
    {
        'filename': '1678_ГАВО_ф1260_д5032_Кирилл_Туркин_конвой_боярина_Матвеева.jpg',
        'thumb': 'thumb_1678_ГАВО_ф1260_д5032.jpg',
        'year': '1678 ГОД',
        'badge': 'ГАВО • ФОНД 1260 • ОПИСЬ 1 • ДЕЛА 5032 И 5049',
        'title_lines': [
            'ЗЕМСКИЙ ЦЕЛОВАЛЬНИК КИРИЛЛ АФАНАСЬЕВИЧ ТУРКИН',
            'Организация гоньбы и доставка боярина Артамона Матвеева в Пустозерск'
        ],
        'vol': '3 ЛИСТА • ЯРЕНСКАЯ ПРИКАЗНАЯ ИЗБА • ГОРОДОВОЙ СТАРОСТА',
        'quote': '«...наняли 4 подводы везти боярина Артамона Матвеева с сыном до Пустозерска...»',
        'meta_left': [
            ('Целовальник:', 'Кирилл Афанасьевич Туркин (сын Афанасия)'),
            ('Узник государев:', 'Боярин Артамон Сергеевич Матвеев'),
            ('Сын узника:', 'Андрей Артамонович Матвеев'),
            ('Конвойный:', 'Стольник Гавриил Тухачевский'),
            ('Ямщики / подводы:', 'Яков Одинцов, Семён Малафеев')
        ],
        'meta_right': [
            ('Должность:', 'Земский целовальник Усть-Выми и Вожемы'),
            ('Значение:', 'Участие рода в ключевых событиях эпохи'),
            ('Отчетность:', 'Городовой староста Данила Ермаков'),
            ('Хранение:', 'БАУ ВО «ГАВО», г. Вологда')
        ]
    },
    {
        'filename': '1679_ГАВО_ф1260_д5260_Исаак_Туркин_посыльщик_деньги_на_корм_рать.jpg',
        'thumb': 'thumb_1679_ГАВО_ф1260_д5260.jpg',
        'year': '1679 ГОД',
        'badge': 'ГАВО • ФОНД 1260 • ОПИСЬ 1 • ДЕЛО 5260',
        'title_lines': [
            'ПОСЫЛЬЩИК ИСААК ТУРКИН: КАЗНА ДАТОЧНЫМ ЛЮДЯМ',
            'Доставка в Москву денег на содержание ратных людей со 144 дворов'
        ],
        'vol': '1 ЛИСТ • ПРИЕМНАЯ ОТПИСЬ МОСКОВСКИХ ПРИЕМЩИКОВ',
        'quote': '«...от усть-вымских посыльщиков со 144 дворов... от Исаака Туркина 14 рублей...»',
        'meta_left': [
            ('Посыльщик в Москву:', 'Исаак Афанасьевич Туркин (дьячок)'),
            ('Приемщики (Москва):', 'Еремей Глызин, Григорий Козлов'),
            ('Сборщики в Москве:', 'Григорий Бутин, Затей Бахматов'),
            ('Облагаемая база:', '144 двора (причетники, крестьяне, бобыли)'),
            ('Личный взнос:', '14 рублей серебром (Исаак Туркин)')
        ],
        'meta_right': [
            ('Тип дела:', 'Казенная приемная отпись (Москва)'),
            ('Исторический фон:', 'Русско-турецкая война 1676–1681 гг.'),
            ('Значение:', 'Государственная финансовая миссия рода'),
            ('Хранение:', 'БАУ ВО «ГАВО», г. Вологда')
        ]
    },
    {
        'filename': '1688_ГАВО_ф1260_д7753_Исаак_Туркин_выборный_судья_Усть_Выми.jpg',
        'thumb': 'thumb_1688_ГАВО_ф1260_д7753.jpg',
        'year': '1688–1698 ГГ.',
        'badge': 'ГАВО • ФОНД 1260 • ДЕЛА 7753, 8267, 10789',
        'title_lines': [
            'СУДЕБНАЯ ДЕЯТЕЛЬНОСТЬ ВЫБОРНОГО СУДЬИ ИСААКА ТУРКИНА',
            'Мирской суд, межевание пожен и следствие по земельным захватам'
        ],
        'vol': '6 ЛИСТОВ • НАКАЗНЫЕ ПАМЯТИ АРХИЕРЕЙСКОГО ПРИКАЗА',
        'quote': '«...память на Усть-Вымь выборному крестьянину Исаку Туркину о суде...»',
        'meta_left': [
            ('Выборный судья:', 'Исаак Афанасьевич Туркин'),
            ('Дело 1688 г. (д. 7753):', 'Иск священника о. Петра о покосах'),
            ('Дело 1689 г. (д. 8267):', 'Истец Семён Онучин, ответчик Марк Екимов'),
            ('Дело 1698 г. (д. 10789):', 'Иван Базлуцкий против Дмитрия Канкарова'),
            ('Следователи (1698):', 'Исаак Туркин и Даниил Козлов (р. Ибеж)')
        ],
        'meta_right': [
            ('Должность:', 'Выборный крестьянин Усть-Вымской вотчины'),
            ('Юрисдикция:', 'Земельные, межевые и финансовые споры'),
            ('Значение:', 'Высший мирской судейский авторитет рода'),
            ('Хранение:', 'БАУ ВО «ГАВО», г. Вологда')
        ]
    },
    {
        'filename': '1687_ГАВО_ф1260_д7519_Священник_Петр_Туркин_Вологда_подворье.jpg',
        'thumb': 'thumb_1687_ГАВО_ф1260_д7519.jpg',
        'year': '1687–1688 ГГ.',
        'badge': 'ГАВО • ФОНД 1260 • ОПИСЬ 1 • ДЕЛО 7519',
        'title_lines': [
            'СВЯЩЕННИК ПЁТР ТУРКИН НА АРХИЕРЕЙСКОМ ПОДВОРЬЕ',
            'Защита приходских вотчинных земель против Великоустюжской епархии'
        ],
        'vol': 'ТОМ 130 ЛИСТОВ (ЛЛ. 79, 82–83) • АРХИЕПИСКОП ГАВРИИЛ',
        'quote': '«...священника Петра содержать на подворье и кормить... дать помощь в челобитье...»',
        'meta_left': [
            ('Челобитчик:', 'Священник Пётр Исаакович Туркин'),
            ('Депутат от мира:', 'Крестьянин Гаврило Игнатьев Козлов'),
            ('Принимал в Вологде:', 'Архиепископ Вологодский Гавриил'),
            ('Попечитель:', 'Стряпчий Иван Суровцов'),
            ('Противная сторона:', 'Архиепископ Великоустюжский Александр')
        ],
        'meta_right': [
            ('Место действия:', 'Архиерейское подворье, г. Вологда'),
            ('Предмет спора:', 'Пограничные церковные вотчинные земли'),
            ('Значение:', 'Личное доверие правящего архиерея'),
            ('Хранение:', 'БАУ ВО «ГАВО», г. Вологда')
        ]
    }
]

out_dir = 'архив_сканы_первоисточников'
thumb_dir = os.path.join(out_dir, 'превью')
os.makedirs(out_dir, exist_ok=True)
os.makedirs(thumb_dir, exist_ok=True)

# Load fonts with carefully scaled sizes to guarantee fitting
font_badge_top = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
font_small_top = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
font_year = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
font_delo_badge = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
font_vol = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
font_quote = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 24)
font_col_header = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 19)
font_lbl = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
font_val = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
font_footer = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)

W, H = 1600, 1100

for item in CARDS:
    im = Image.new('RGB', (W, H), '#16100b')
    draw = ImageDraw.Draw(im)

    # Frame Borders
    draw.rectangle([18, 18, W-18, H-18], outline='#8c6239', width=3)
    draw.rectangle([25, 25, W-25, H-25], outline='#3d2b1a', width=1)
    draw.rectangle([30, 30, W-30, H-30], outline='#b8860b', width=2)

    # Top Header
    draw.rectangle([32, 32, W-32, 105], fill='#25180d')
    draw.text((W/2, 54), 'ГОСУДАРСТВЕННЫЙ АРХИВ ВОЛОГОДСКОЙ ОБЛАСТИ (ГАВО)', font=font_badge_top, fill='#d4af37', anchor='mm')
    draw.text((W/2, 84), 'ФОНД 1260: ВОЛОГОДСКИЙ АРХИЕРЕЙСКИЙ ДОМ • ОПИСЬ 1 • ДЕЛА XVII ВЕКА', font=font_small_top, fill='#cbd5e1', anchor='mm')

    # Year Pill Badge
    draw.rectangle([W/2 - 120, 122, W/2 + 120, 158], fill='#b8860b')
    draw.text((W/2, 140), item['year'], font=font_year, fill='#16100b', anchor='mm')

    # Archival Case Badge
    draw.text((W/2, 185), item['badge'], font=font_delo_badge, fill='#f59e0b', anchor='mm')

    # Main Title (Adaptive font size to guarantee fitting)
    t1 = item['title_lines'][0]
    t2 = item['title_lines'][1]
    
    # Dynamically pick font size for title 1 so it never clips
    size_t1 = 34
    while size_t1 > 20:
        f_cand = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', size_t1)
        if f_cand.getlength(t1) <= (W - 140):
            break
        size_t1 -= 1
    font_t1 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', size_t1)

    size_t2 = 23
    while size_t2 > 17:
        f_cand2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size_t2)
        if f_cand2.getlength(t2) <= (W - 140):
            break
        size_t2 -= 1
    font_t2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size_t2)

    draw.text((W/2, 230), t1, font=font_t1, fill='#fef3c7', anchor='mm')
    draw.text((W/2, 275), t2, font=font_t2, fill='#e2e8f0', anchor='mm')

    # Divider Line
    draw.line([70, 310, W-70, 310], fill='#8c6239', width=1)
    draw.line([W/2 - 140, 310, W/2 + 140, 310], fill='#d4af37', width=3)

    # Volume & Court Banner
    draw.text((W/2, 340), item['vol'], font=font_vol, fill='#38bdf8', anchor='mm')

    # Antique Parchment Quote Box
    draw.rectangle([70, 375, W-70, 465], fill='#20150d', outline='#8c6239', width=2)
    draw.text((W/2, 420), item['quote'], font=font_quote, fill='#fde68a', anchor='mm')

    # Two Structured Metadata Columns
    col_w = (W - 140 - 24) / 2
    x1_l = 70
    x2_l = x1_l + col_w
    x1_r = x2_l + 24
    x2_r = W - 70
    y_box_top = 485
    y_box_bottom = 990

    draw.rectangle([x1_l, y_box_top, x2_l, y_box_bottom], fill='#1a120b', outline='#45311f', width=1)
    draw.rectangle([x1_r, y_box_top, x2_r, y_box_bottom], fill='#1a120b', outline='#45311f', width=1)

    # Column 1 Header
    draw.rectangle([x1_l, y_box_top, x2_l, y_box_top + 45], fill='#2c1c11')
    draw.text((x1_l + col_w/2, y_box_top + 22), 'СТОРОНЫ ДЕЛА И УЧАСТНИКИ', font=font_col_header, fill='#d4af37', anchor='mm')

    # Column 2 Header
    draw.rectangle([x1_r, y_box_top, x2_r, y_box_top + 45], fill='#2c1c11')
    draw.text((x1_r + col_w/2, y_box_top + 22), 'АРХИВНОЕ ЗНАЧЕНИЕ ДЛЯ РОДОСЛОВНОЙ', font=font_col_header, fill='#d4af37', anchor='mm')

    # Render Column 1 Key-Values
    y_row = y_box_top + 65
    for lbl, val in item['meta_left']:
        draw.text((x1_l + 24, y_row), lbl, font=font_lbl, fill='#f59e0b')
        draw.text((x1_l + 24, y_row + 25), val, font=font_val, fill='#f1f5f9')
        y_row += 68

    # Render Column 2 Key-Values
    y_row2 = y_box_top + 65
    for lbl, val in item['meta_right']:
        draw.text((x1_r + 24, y_row2), lbl, font=font_lbl, fill='#38bdf8')
        draw.text((x1_r + 24, y_row2 + 25), val, font=font_val, fill='#f1f5f9')
        y_row2 += 68

    # Bottom Seal Banner
    draw.rectangle([32, 1010, W-32, 1068], fill='#25180d')
    draw.text((W/2, 1039), 'ПРОЕКТ «РОДОСЛОВНАЯ ТУРКИНЫХ» • НАУЧНО-АРХИВНАЯ РЕКОНСТРУКЦИЯ ИСТОЧНИКОВ XVII ВЕКА', font=font_footer, fill='#94a3b8', anchor='mm')

    # Save Hi-Res Image
    out_path = os.path.join(out_dir, item['filename'])
    im.save(out_path, quality=95)

    # Save Crisp Thumbnail
    thumb = im.resize((480, 330), Image.Resampling.LANCZOS)
    thumb_path = os.path.join(thumb_dir, item['thumb'])
    thumb.save(thumb_path, quality=90)
    print(f"Generated card (fitted): {item['filename']}")

print('All 8 cards generated with perfect fitting and parties breakdown!')
