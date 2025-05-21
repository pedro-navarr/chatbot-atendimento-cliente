from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Consultar status de pedido
class ActionConsultarStatus(Action):

    def name(self) -> Text:
        return "action_consultar_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Seu pedido está em processamento. Em breve enviaremos novidades!")
        return []

# Informar preço de produto
class ActionInformarPreco(Action):

    def name(self) -> Text:
        return "action_informar_preco"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        produto = tracker.get_slot('produto')
        
        precos = {
            "notebook": "R$ 3.500,00",
            "celular": "R$ 2.000,00",
            "tablet": "R$ 1.200,00"
        }
        
        if produto and produto.lower() in precos:
            preco = precos[produto.lower()]
            dispatcher.utter_message(text=f"O preço do {produto} é {preco}.")
        else:
            dispatcher.utter_message(text="Desculpe, não encontrei o preço desse produto.")
        
        return []

# Agendar atendimento
class ActionAgendarAtendimento(Action):

    def name(self) -> Text:
        return "action_agendar_atendimento"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        horario = tracker.get_slot('horario')
        if horario:
            dispatcher.utter_message(text=f"Seu atendimento foi agendado para às {horario}.")
        else:
            dispatcher.utter_message(text="Por favor, informe um horário para agendarmos.")
        
        return []
