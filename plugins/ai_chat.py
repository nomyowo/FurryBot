def chatService(client, question):
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": "假设你是一只狐狸，现在请用狐狸的身份去回答下面的问题"},
            {"role": "user", "content": question},
        ],
        stream=False
    )
    return "\n" + "思考过程：\n" + response.choices[0].message.model_extra['reasoning_content'] + "\n" + "\n回答：\n" + \
        response.choices[0].message.content
