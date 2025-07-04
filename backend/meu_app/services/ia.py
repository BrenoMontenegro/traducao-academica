import requests
import json

session = requests.Session()

def gerar_insight_local(texto):
    prompt = f"Leia o texto e gere um insight breve, claro e relevante em português do Brasil:\n\n{texto}"

    try:
        response = session.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 400,
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

    except requests.exceptions.RequestException as e:
        return f"[Erro de conexão]: {str(e)}"
    except Exception as e:
        return f"[Erro inesperado]: {str(e)}"
