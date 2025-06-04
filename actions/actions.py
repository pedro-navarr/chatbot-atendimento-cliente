from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType

# Ação de fallback para quando o bot não entende
class ActionFallbackMessage(Action):
    def name(self) -> Text:
        return "action_fallback_message"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Desculpe, não entendi. Você pode reformular sua pergunta ou me dizer como posso ajudar?"
        )
        return []
    

# Consultar status de pedido 
class ActionConsultarStatus(Action):

    def name(self) -> Text:
        return "action_consultar_status"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        numero_pedido = tracker.get_slot("numero_pedido")

        if numero_pedido:

            if numero_pedido == "12345":
                dispatcher.utter_message(
                    text=f"O pedido {numero_pedido} está em trânsito e deve chegar em até 2 dias úteis."
                )
            elif numero_pedido == "67890":
                dispatcher.utter_message(
                    text=f"O pedido {numero_pedido} foi entregue ontem. Esperamos que tenha gostado!"
                )
            elif numero_pedido == "11223":
                dispatcher.utter_message(
                    text=f"O pedido {numero_pedido} está aguardando retirada na agência mais próxima."
                )
            else:
                dispatcher.utter_message(
                    text=f"Não encontramos informações detalhadas sobre o pedido {numero_pedido}. Por favor, verifique o número ou entre em contato com nosso suporte."
                )
        else:

            dispatcher.utter_message(text="Por favor, informe o número do seu pedido.")
            
        return []


# Informar preço de produto
class ActionInformarPreco(Action):

    def name(self) -> Text:
        return "action_informar_preco"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        produto = tracker.get_slot("produto")

        precos = {
            "notebook": "R$ 3.500,00",
            "celular": "R$ 2.000,00",
            "tablet": "R$ 1.200,00",
            "fone de ouvido": "R$ 250,00",
            "computador": "R$ 4.800,00",
            "monitor": "R$ 900,00",
        }

        if produto:
            produto_lower = produto.lower()
            if produto_lower in precos:
                preco = precos[produto_lower]
                dispatcher.utter_message(text=f"O preço do {produto} é {preco}.")
            else:
                dispatcher.utter_message(
                    text=f"Desculpe, não encontrei o preço para '{produto}'. No momento, temos preços para notebooks, celulares, tablets, fones de ouvido, computadores e monitores. Gostaria de saber sobre algum desses?"
                )
        else:
            dispatcher.utter_message(
                text="Por favor, me diga qual produto você gostaria de saber o preço."
            )

        return []


# Form de Agendamento de Atendimento
class ValidateAgendamentoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_agendamento_form"

    def validate_horario(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida o horário do agendamento."""
        horario_limite_inicio = 8
        horario_limite_fim = 18

        try:

            if 'h' in str(slot_value).lower():
                horario_num = int(str(slot_value).lower().replace('h', ''))
            else:
                horario_num = int(slot_value)

            if horario_limite_inicio <= horario_num <= horario_limite_fim:
                return {"horario": slot_value}
            else:
                dispatcher.utter_message(
                    text="Nosso horário de atendimento é das 8h às 18h. Por favor, escolha um horário dentro desse intervalo."
                )
                return {"horario": None} 
        except ValueError:
            dispatcher.utter_message(
                text="Esse não parece ser um horário válido. Por favor, tente um formato como '14h' ou '10'."
            )
            return {"horario": None}

    def validate_data(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida a data do agendamento (Exemplo simples)."""

        if isinstance(slot_value, str) and len(slot_value) > 2: # Evita strings muito curtas
             dispatcher.utter_message(
                 text=f"Entendido, a data escolhida foi {slot_value}."
             )
             return {"data": slot_value}
        else:
             dispatcher.utter_message(text="Essa data não parece válida. Por favor, informe a data completa.")
             return {"data": None}


# Agendar atendimento 
class ActionAgendarAtendimento(Action):

    def name(self) -> Text:
        return "action_agendar_atendimento"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        horario = tracker.get_slot("horario")
        data = tracker.get_slot("data")

        if horario and data:
            dispatcher.utter_message(
                text=f"Seu atendimento foi agendado para às {horario} do dia {data}. Em breve você receberá uma confirmação por e-mail."
            )
        elif horario:
            dispatcher.utter_message(
                text=f"Seu atendimento foi agendado para às {horario}. Por favor, confirme a data desejada."
            )
        else:
            dispatcher.utter_message(
                text="Houve um problema ao agendar. Por favor, tente novamente ou entre em contato com nosso suporte."
            )

        # Limpa os slots após o agendamento
        return [SlotSet("horario", None), SlotSet("data", None)]


# Form para Consulta de Status do Pedido
class ValidateConsultaStatusForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_consulta_status_form"
    def validate_numero_pedido(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida se o número do pedido parece um número válido."""
        
        if isinstance(slot_value, str) and slot_value.isdigit() and 3 <= len(slot_value) <= 10:
            return {"numero_pedido": slot_value}
        else:
            dispatcher.utter_message(text="Esse não parece um número de pedido válido. Por favor, digite apenas os números do seu pedido.")
            return {"numero_pedido": None}