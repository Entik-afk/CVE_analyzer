from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import csv



load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

history = [
    {"role": "system", "content": "Jsi expert na kyberbezpečnost. Odpovídej stručně a prakticky." }
]

while True:
    dotaz = input("Dotaz: ")
    if dotaz.lower() == "exit":
        break

    if dotaz.startswith("/explain"):
        system_prompt = """Jsi lektor kyberbezpečnosti. Vysvětluj jednoduše." 
        Odpověz POUZE ve validním JSON formátu.
        NEPŘIDÁVEJ žádný další text.
        Formát:

        {
            "hrozba": "...",
            "riziko": "...",
            "doporučení": "..."
        }
        
        """
        dotaz = dotaz.replace("/explain", "").strip()
        typ = "explain"

    elif dotaz.startswith("/analyze"):
        system_prompt = """
        Jsi bezpečnostní analyzátor.

        Analyzuj text a najdi bezpečnostní hrozby.

        Odpověz POUZE ve validním JSON formátu.
        NEPŘIDÁVEJ žádný další text.

        Formát:

        {
            "hrozba": "...",
            "riziko": "...",
            "doporučení": "..."
        }
        """
        dotaz = dotaz.replace("/analyze", "").strip()
        typ = "analyze"

    elif dotaz.startswith("/advise"):
        system_prompt = """Dej praktické bezpečnostní rady.
         Odpověz POUZE ve validním JSON formátu.
        NEPŘIDÁVEJ žádný další text.
        Formát:
        {
            "hrozba": "...",
            "riziko": "...",
            "doporučení": "..."
        }
        
        
        """
        dotaz = dotaz.replace("/advise", "").strip()
        typ = "advise"

    else:
        system_prompt = """Jsi expert na kyberbezpečnost. Odpovídej stručně a prakticky.
         Odpověz POUZE ve validním JSON formátu.
        NEPŘIDÁVEJ žádný další text.
        Formát:
        {
            "hrozba": "...",
            "riziko": "...",
            "doporučení": "..."
        }
        
        
        """
        typ = "general"

    # Aktualizujeme system prompt do historie před dotazem
    history.append({"role": "system", "content": system_prompt})
    history.append({"role": "user", "content": dotaz})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        max_tokens=200,
        temperature=0.7,
    )

    odpoved = response.choices[0].message.content
    print("AI:", odpoved)
    
    try:
        data = json.loads(odpoved)
        print("Hrozba:", data.get("hrozba"))
        print("Riziko:", data.get("riziko"))
        print("Doporučení:", data.get("doporučení"))

        with open("output.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            if data:
                writer.writerow([typ, dotaz, data.get("hrozba"), data.get("riziko"), data.get("doporučení")])
            else:
                writer.writerow([typ, dotaz ,odpoved, "", "", ""])
    except json.JSONDecodeError:
        print("Odpověď není validní JSON.")

    

    history.append({"role": "assistant", "content": odpoved})