import sys                                       #
import random                                       
import time                                     
from difflib import SequenceMatcher                                     
import json                                     
import os                                       
import operator                                     

def slow(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


DATA_FILE = "data.json"         
LEARNED_FILE = "learned.json"   

for file in [DATA_FILE, LEARNED_FILE]:
    if not os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f:
            json.dump({}, f)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(LEARNED_FILE, "r", encoding="utf-8") as f:
    learned = json.load(f)

memory = {**data, **learned}

def similar(question, memory, threshold=0.6):
    best = None
    max_ratio = 0
    for recorded in memory:
        ratio = SequenceMatcher(None, question.lower(),
                                recorded.lower()).ratio()
        if ratio > max_ratio:
            max_ratio = ratio
            best = recorded

    if max_ratio >= threshold:
        return best
    else:
        return None

transactions = {
    "+": operator.add,
    "-": operator.sub,
    "/": operator.truediv,
    "*": operator.mul,
}

def calculation(expr):
    expr = expr.replace(" ", "")

    for op in transactions:
        if op in expr:
            pieces = expr.split(op)
            if len(pieces) == 2:
                try:
                    a = float(pieces[0])
                    b = float(pieces[1])
                    return transactions[op](a, b)
                except:
                    return "Hatalı matematiksel ifade!"
    return None


slow("Selam! Ben mini yapay zekâ asistanınım. Bana soru sorabilirsin. Çıkmak için 'exit' yaz.")

while True:
    question = input("\nSen: ").strip()

    if question.lower() in ["çık", "exit", "quit"]:
        slow("Görüşürüz! Bir şeye ihtiyacın olursa buradayım.")
        break

    # Kaydedilen tüm soruları listele
    if question.lower() in ["list", "liste", "sorular"]:
        if memory:
            slow("Şu ana kadar öğrendiğim sorular:", delay=0.05)
            for i, s in enumerate(memory, 1):
                slow(f"{i}. {s}", delay=0.02)
        else:
            slow("Henüz hiçbir şey öğrenmedim!")
        continue

    # Hesaplama
    result = calculation(question)
    if result is not None:
        slow(f"Sonuç: {result}")
        continue

    # Daha önce öğrenilen bir şey mi?
    same = similar(question, memory)

    if same:
        slow(f"Asistan: {memory[same]}")
    else:
        # Öğrenme modu
        answer = input(
            "Bunu bilmiyorum. Bana cevabını öğret: ").strip()
        memory[question] = answer
        learned[question] = answer

        with open(LEARNED_FILE, "w", encoding="utf-8") as f:
            json.dump(learned, f, ensure_ascii=False, indent=4)

        slow("Tamamdır! Bunu artık hatırlıyorum.")

