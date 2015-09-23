# -*- coding: utf-8 -*-
from decimal import Decimal

 
def transform(trnsfstr):
    trnsfstr = ' '.join(trnsfstr.split())
    trnsfstr = trnsfstr.capitalize()
    return trnsfstr


def triad(number, mass, sort):
    tens = number % Decimal('100')
    tens = int(tens / Decimal('10'))
    ed = number % Decimal('10')
    word = mass[0]
    if tens == 1:
        if ed == 0:
            third_number = u'десять'
        elif ed == 1:
            third_number = u'одиннадцать'
        elif ed == 2:
            third_number = u'двенадцать'
        elif ed == 3:
            third_number = u'тринадцать'
        elif ed == 4:
            third_number = u'четырнадцать'
        elif ed == 5:
            third_number = u'пятнадцать'
        elif ed == 6:
            third_number = u'шестнадцать'
        elif ed == 7:
            third_number = u'семнадцать'
        elif ed == 8:
            third_number = u'восемьнадцать'
        elif ed == 9:
            third_number = u'девятнадцать'
        else:
            third_number = ''
    else:
        if ed == 1:
            if sort == 'w': 
                third_number = u'одна'
                word = mass[1]
            else:
                third_number = u'один'
                word = mass[1]
        elif ed == 2:
            if sort == 'w':
                third_number = u'две'
                word = mass[2]
            else:
                third_number = u'два'
        elif ed == 3:
            third_number = u'три'
            word = mass[2]
        elif ed == 4:
            third_number = u'четыре'
            word = mass[2]
        elif ed == 5:
            third_number = u'пять'
        elif ed == 6:
            third_number = u'шесть'
        elif ed == 7:
            third_number = u'семь'
        elif ed == 8:
            third_number = u'восемь'
        elif ed == 9:
            third_number = u'девять'
        else:
            third_number = ''
    hundred = int(number / Decimal('100'))
    if hundred == 1:
        first_number = u'сто'
    elif hundred == 2:
        first_number = u'двести'
    elif hundred == 3:
        first_number = u'триста'
    elif hundred == 4:
        first_number = u'четыреста'
    elif hundred == 5:
        first_number = u'пятьсот'
    elif hundred == 6:
        first_number = u'шестьсот'
    elif hundred == 7:
        first_number = u'семьсот'
    elif hundred == 8:
        first_number = u'восемьсот'
    elif hundred == 9:
        first_number = u'девятьсот'
    else:
        first_number = ''
    if tens == 2:
        second_number = u'двадцать'
    elif tens == 3:
        second_number = u'тридцать'
    elif tens == 4:
        second_number = u'сорок'
    elif tens == 5:
        second_number = u'пятьдесят'
    elif tens == 6:
        second_number = u'шестьдесят'
    elif tens == 7:
        second_number = u'семьдесят'
    elif tens == 8:
        second_number = u'восемьдесят'
    elif tens == 9:
        second_number = u'девяносто'
    else:
        second_number = ''
    return first_number + ' ' + second_number + ' ' + third_number + ' ' + word
 

def summ(sum1):
    hundred = ['', '', '', '']
    thousand = [u'тысяч', u'тысяча', u'тысячи']
    million = [u'миллионов', u'миллион', u'миллиона']
    billion = [u'миллиардов', u'миллиард', u'миллиарда']
    sort1 = ['m']
 
    number1 = sum1 / Decimal('1000000')
    part1 = int(number1)
    number2 = part1
    number2 = sum1 - number2 * Decimal('1000000')
    part2 = int(number2)
    billionpart = int(part1 / Decimal('1000'))
    if billionpart == 0:
        billion_word = ''
    else:
        billion_word = triad(billionpart, billion, sort1)
    mill = part1 % Decimal('1000')
    if mill == 0:
        mill_word = ''
    else: 
        mill_word = triad(mill, million, sort1)
    thous = int(part2 / Decimal('1000'))
    sort1 = 'w'
    if thous == 0:
        thous_word = ''
    else:
        thous_word = triad(thous, thousand, sort1)
 
    hundredpart = part2 % 1000
    if hundredpart == 0:
        hundred_word = ''
    else:
        sort1 = 'm'
        hundred_word = triad(hundredpart, hundred, sort1)
    
    if sum1 < 1:
        null_word = u'ноль рублей'
    else:
        null_word = ''
    copeck_word = sum1 % Decimal('1')
    copeck_word = int(copeck_word*100)
    copeck_word = str(copeck_word)
    trnsfstr = billion_word + ' ' + mill_word + ' ' + thous_word + ' ' + hundred_word + ' ' + null_word + u'руб.' \
        + ' ' + copeck_word + ' ' + u'коп.'
    trnsfstr = transform(trnsfstr)
 
    return trnsfstr
