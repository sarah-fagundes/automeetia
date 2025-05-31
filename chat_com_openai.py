from openai import OpenAI

def generate_response(openai_client, system_prompt_text, user_prompt_text):
    try:

        response = openai_client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system_prompt_text},
                {"role": "user", "content": user_prompt_text}
            ],

            temperature=0.7
        )

        returned_text = response.choices[0].message.content.strip()

        return returned_text

    except Exception as e:
        print("Ocorreu um erro:", str(e))
        return None



if __name__ == "__main__":
    openai_client = OpenAI(api_key='')  # Certifique-se de substituir por uma chave de API válida.
    system_prompt_text = "Você é um assistente prestativo."
    user_prompt_text = "Explique a teoria da relatividade em termos simples."

    result = generate_response(openai_client, system_prompt_text, user_prompt_text)

    if result:
        print("Resultado Final:", result)
    else:
        print("Falha ao obter uma resposta do modelo.")
