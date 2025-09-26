# # 1
# from math import factorial
# from functools import lru_cache
#
# def calculate_combinations():
#     # Частоты букв в слове "КОМБИНАТОРИКА"
#     letters = {
#         'К': 2, 'О': 2, 'М': 1, 'Б': 1,
#         'И': 2, 'Н': 1, 'А': 2, 'Т': 1, 'Р': 1
#     }
#     letters_list = list(letters.items())
#
#     @lru_cache(maxsize=None)
#     def dp(index, remaining):
#         if index == len(letters_list):
#             return 1 if remaining == 0 else 0
#         total = 0
#         char, max_count = letters_list[index]
#         max_possible = min(max_count, remaining)
#         for count in range(0, max_possible + 1):
#             comb = factorial(remaining) // (factorial(count) * factorial(remaining - count))
#             total += dp(index + 1, remaining - count) * comb
#         return total
#
#     return dp(0, 6)
#
# result = calculate_combinations()
# print(result)

#1
# from itertools import permutations
#
# word = "КОМБИНАТОРИКА"
# length = 6
#
# # Получаем все возможные перестановки длины 5 (учитывая порядок)
# all_perms = permutations(word, length)
#
# # Убираем дубликаты (так как в слове есть повторяющиеся буквы)
# unique_perms = set(all_perms)
#
# print(f"Количество уникальных перестановок из {length} букв: {len(unique_perms)}")

#2
import math

# 1) Количество кратчайших путей в сетке 20x18 без ограничений
# Кратчайший путь состоит из 20 шагов вправо (R) и 18 шагов вверх (U)
# Общее количество шагов: 20 + 18 = 38
# Количество путей = C(38, 20) = 38! / (20! * 18!)
result_1 = math.comb(38, 20)

# 2) Количество кратчайших путей без двух подряд идущих шагов вверх (U)
# Сначала расставляем все 20 шагов вправо (R), создавая 21 возможных промежутков
# (перед первым R, между R и после последнего R)
# Нужно разместить 18 шагов U в эти 21 промежутков, не более одного U в каждый промежуток
# Количество способов = C(21, 18) = 21! / (3! * 18!)
result_2 = math.comb(21, 18)

print("Количество путей в сетке 20×18 без ограничений:", result_1)
print("Количество путей без двух подряд идущих вертикальных участка:", result_2)

