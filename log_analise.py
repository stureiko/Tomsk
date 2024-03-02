import pyautogui as pyg
import re


def get_log():
    return '''             СООБЩЕНИЯ О РЕЗУЛЬТАТАХ ВЫПОЛНЕННОГО РАСЧЕТА               
             --------------------------------------------               
                                                                        
 Выполняется расчет режима работы системы МГ                            
 Критерий - максимум производительности                                 
 Методика расчета энергозатрат 2002 года                                
 Новая методика расчета АВО                                             
 Новая методика расчета АВО                                             
 Элементов в исходной схеме 2099                                        
 В том числе : цехов КС    15    Pmax= 60.0                             
                     ЛУ   589                                           
 13км-22км     НП  Новый диаметр 1020.0 x 10.7                          
 0км-17км      БН  Новый диаметр 1020.0 x 11.8                          
 51км-56км     БН  Новый диаметр 1020.0 x 14.2                          
 32км-34км     НП  Новый диаметр 1020.0 x 10.6                          
 34км-39км 1   НП  Новый диаметр 1020.0 x 10.9                          
 39км-66км     НП  Новый диаметр 1020.0 x 11.4                          
 68км-71км     НП  Новый диаметр 1020.0 x 12.1                          
 71км-74км     НП  Новый диаметр 1020.0 x 12.2                          
 25км-28км     ЮН  Новый диаметр  720.0 x  7.0                          
 136км-137км 1 ЮН  Новый диаметр  720.0 x 12.0                          
 13км-14км 2   НБ  Новый диаметр  529.0 x 14.0                          
 ГРС-2г.Барнаул    Новый диаметр  426.0 x  7.0                          
 48км-49км 2   То  Новый диаметр  530.0 x 10.5                          
 0км-23км      МВ  Новый диаметр  720.0 x 10.5                          
 22км-32км     НП  Новый диаметр 1020.0 x 10.8                          
 РП-10 Артем       Новый диаметр   89.0 x  4.5                          
 ГРС-1 1н НВарт    Новый диаметр 1020.0 x 12.0                          
 4км-13км      НП  Новый диаметр 1020.0 x 10.4                          
 ГРС1,3г.Кем1      Новый диаметр  426.0 x 16.0                          
 Куйбышев          Новый диаметр  100.0 x  6.0                          
 19.12.0    1-2НП  Новый диаметр 1020.0 x 14.0                          
 Вх  Парабель  ПК  Новый диаметр 1020.0 x 16.0                          
 ГРС24 Шефер       Новый диаметр   76.0 x  5.0                          
                     ПЗГ  149                                           
                     П/Р    7                                           
 Удаляем из схемы проходную КС Тюкалинск СО ! (K)                       
 Удаляем из схемы проходную КС Ивановска ОН ! (K)                       
 Удаляем из схемы проходную КС Чанская   ОН ! (K)                       
 Удаляем из схемы проходную КС Кожурли 1 ОН ! (K)                       
 Удаляем из схемы проходную КС Чулымская ОН ! (K)                       
 Удаляем из схемы проходную КС Новосибир ОН ! (K)                       
 Удаляем из схемы проходную КС Карасульск   ! (K)                       
 Удаляем из схемы проходную КС Абатская     ! (K)                       
 Всего удалено из схемы проходных КС   8 !                              
 #Максимальное число параллельных КС   1 !                              
 В расчетной схеме число КС    6                                        
               Паспортов КС    2                                        
                        П/Р    3                                        
 Число параллельных цепочек    0                                        
          из них объединены    0                                        
                         ЛУ  341                                        
                     Вершин  459                                        
                        Дуг  492                                        
 Расчетная структура ГТС построена.                                     
 # Обратный поток газа через КС (П/Р) запрещён !                        
 # Алгоритмы ускорения расчета включены частично !                      
 Число дуг в схеме без ПодМГ       492                                  
 Число дуг (ЛУ) в расчетной схеме  342                                  
                 в т.ч. фиктивных    1                                  
 Число вершин в расчетной схеме    309                                  
 В ГТС несвязных схем  1                                                
 Схема  1                                                               
 Вход   НВ ГПК                                                          
 Вход   Бог2Цвх пр                                                      
 Max небаланс на Володин 1 ПК                                           
 Выполнена  1 итерация. Небаланс  36.85  4.72 22.33  27.94 20.25  0.00  
 Max небаланс на Проскок 1 ПК                                           
 Выполнена  2 итерация. Небаланс  20.86  4.73  0.63   1.64  0.00  0.00  
 Max небаланс на Володин 1 ПК                                           
 Выполнена  3 итерация. Небаланс  11.28  3.40  0.19   0.30  7.94  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена  4 итерация. Небаланс   4.91  2.48  0.15   0.89  0.85  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена  5 итерация. Небаланс   2.99  2.74  0.03   0.00  0.46  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена  6 итерация. Небаланс   3.03  2.72  0.01   0.00  0.00  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена  7 итерация. Небаланс   3.10  2.72  0.00   0.00  0.00  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена  8 итерация. Небаланс   3.14  2.72  0.00   0.00  0.00  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена  9 итерация. Небаланс   3.18  2.72  0.00   0.00  0.00  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена 10 итерация. Небаланс   3.20  2.71  0.00   0.00  0.00  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена 11 итерация. Небаланс   3.21  2.71  0.00   0.00  0.46  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена 12 итерация. Небаланс   3.22  2.71  0.00   0.00  0.46  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена 13 итерация. Небаланс   3.23  2.71  0.00   0.00  0.00  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена 14 итерация. Небаланс   3.23  2.71  0.00   0.00  0.00  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена 15 итерация. Небаланс   3.24  2.71  0.00   0.00  0.44  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена 16 итерация. Небаланс   3.24  2.71  0.00   0.00  0.44  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена 17 итерация. Небаланс   3.25  2.71  0.00   0.00  0.00  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена 18 итерация. Небаланс   3.25  2.71  0.00   0.00  0.41  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена 19 итерация. Небаланс   3.24  2.71  0.00   0.00  0.41  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена 20 итерация. Небаланс   3.25  2.71  0.00   0.00  0.00  0.00  
 Max небаланс на Алексан 1 НП                                           
 Выполнена 21 итерация. Небаланс   4.12  2.11  0.05   0.23  1.07  0.00  
 Max небаланс на Володин 1 ПК                                           
 Выполнена 22 итерация. Небаланс   6.30  1.08  0.22   1.05  4.10  0.00  
 Max небаланс на Володин 1 ПК                                           
 Выполнена 23 итерация. Небаланс   4.27  0.75  0.02   0.16  0.11  0.00  
 Max небаланс на Володин 1 ПК                                           
 Выполнена 24 итерация. Небаланс   2.93  0.51  0.02   0.09  0.01  0.00  
 Max небаланс на Володин 1 ПК                                           
 Выполнена 25 итерация. Небаланс   1.93  0.35  0.01   0.06  0.01  0.00  
 Max небаланс на Володин 1 ПК                                           
 Выполнена 26 итерация. Небаланс   1.28  0.24  0.01   0.04  0.01  0.00  
 Max небаланс на Володин 1 ПК                                           
 Выполнена 27 итерация. Небаланс   0.89  0.16  0.01   0.03  0.01  0.00  
 Max небаланс на Володин 1 ПК                                           
 Выполнена 28 итерация. Небаланс   0.64  0.11  0.02   0.03  0.01  0.00  
 Max небаланс на Володин 1 ПК                                           
 Выполнена 29 итерация. Небаланс   0.50  0.08  0.01   0.03  0.00  0.00  
 Max небаланс на Володин 1 ПК                                           
 Выполнена 30 итерация. Небаланс   0.32  0.05  0.00   0.01  0.00  0.00  
 Расчет сети выполнен за 30 итераций !                                  
 Внимание ! Расчет выполнен с нарушением ограничений !                  
 N узла =  254                    P < PMIN                              
 Значение расчетное =      1.000 Ограничение =     25.000               
 N узла =    1   НВ ГПК           P > PMAX                              
 Значение расчетное =     59.712 Ограничение =     56.000               
 N узла =  113   Бог2Цвх пр       P > PMAX                              
 Значение расчетное =     84.334 Ограничение =     51.900               
 N узла =  219                    P > PMAX                              
 Значение расчетное =     54.141 Ограничение =     43.100               
 N узла =  220                    P > PMAX                              
 Значение расчетное =     53.397 Ограничение =     43.100               
 N ЛУ =   47   1717км-1727км СО PBЫXH KC (П/Р) > PMAX                   
 Значение расчетное =     58.547 Ограничение =     56.000               
 О ш и б к а !  Давление <= 1 ата на ПЗГ ГРС г. Горно  P=  -1.5 ата     
 Всего 16 шлейфов КС. Запас=   0.2321 млн.м3 !                          
'''


def analise_log(spam: str):
    err = re.search(r'Внимание ! Расчет выполнен с нарушением ограничений !', spam)
    if err:
        nodes = re.findall(r'N узла =\s+\d+', spam)
    print(nodes)


def main():
    analise_log(get_log())


if __name__ == '__main__':
    main()