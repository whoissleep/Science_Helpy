from huggingface_hub import InferenceClient

class ChatModel:
    def __init__(self, api_key, model_id):        
        """
        Initialize the chat model.

        Parameters
        ----------
        api_key : str
            An API key from the Hugging Face Hub.
        model_id : str
            The ID of the model to use for the chat.

        Attributes
        ----------
        client : InferenceClient
            The client to use for inference.
        model_id : str
            The ID of the model to use for the chat.
        messages_template : list
            A list of messages to send to the model. The messages are formatted
            as a list of dictionaries, where each dictionary contains the following
            keys:
                - role: The role of the message. Can be "system" or "user".
                - content: The content of the message.
        """
        
        self.client = InferenceClient(api_key=api_key)
        self.model_id = model_id
        self.messages_template = [
            {"role": "system", "content": "Ты - профессиональный специалист, который помогает пользователю с исследованием статей. Отвечай на то, что они хотят, основываясь на контексте: {rag_context}"},
            {"role": "user", "content": "{context}"}
        ]

    def send_message(self, text, rag_context=''):
        """
        Send a message to the model.

        Parameters
        ----------
        text : str
            The text of the message to send.
        rag_context : str
            The context of the message, which is used to generate the response.

        Returns
        -------
        str
            The response from the model.
        """
        messages = [
            {"role": "system", "content": self.messages_template[0]["content"].format(rag_context=rag_context)},
            {"role": "user", "content": self.messages_template[1]["content"].format(context=text)}
        ]

        stream = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            temperature=0.7,
            max_tokens=512,
            top_p=0.6,
            stream=True
        )

        response_text = ''.join(chunk['choices'][0]['delta']['content'] for chunk in stream)
        return response_text
    

###TEST PLACE
###DONT USE THIS CODE IF IT DONT HAVE "DONE AND READY FOR PROD"