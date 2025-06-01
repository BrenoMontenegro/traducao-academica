import requests
import json

def gerar_insight_local(texto):
    prompt = f"Analise criticamente o texto a seguir. Emita um insight original, claro e relevante:\n\n{texto}"

    try:
       
        requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": "Iniciando...",
                "options": {
                    "num_predict": 1
                }
            }
        )

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 150,
                    "temperature": 0.7
                }
            }
        )
        response.raise_for_status()

        try:
            data = response.json()
            return data.get("response", "").strip()
        except json.JSONDecodeError:
            return response.text.strip()

    except Exception as e:
        return f"[Erro ao gerar insight]: {str(e)}"
