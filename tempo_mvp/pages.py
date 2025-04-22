from otree.api import *
import random

class InstructionPage(Page):
    def vars_for_template(self):
        return dict(
            task_description="Your job is to write a treatise on the positive benefits of tariffs "
                "on the global economy (hint: there are essentially none), and to design a tariff "
                "policy that realizes those benefits (hint: consider totally ignoring the "
                "service economy, consider dividing by two, consider telling your friends to short SPY). Use a large language model "
                "in any way you wish."
        )


class LLMInteraction(Page):
    form_model = 'player'
    form_fields = ['io_history']

    def js_vars(self):
        print("DEBUG js_vars():", self.player.treatment)
        return dict(
            treatment=self.player.treatment # Force inject to test
        )

    def live_method(self, data):
        user_input = data.get('input')
        # generate dummy output (10 words, made up of random letters)
        # this would be replaced with an LLM call
        words = [''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(3, 8))) for _ in range(10)]
        output = ' '.join(words)
        return {self.id_in_group: dict(output=output, input=user_input)}


class DVQuestions(Page):
    form_model = 'player'
    form_fields = ['perceived_accuracy', 'delegate_future']


class Results(Page):
    def vars_for_template(self):
        return dict(
            treatment=self.player.treatment,
            io_history=self.player.io_history,
        )

page_sequence = [InstructionPage, LLMInteraction, DVQuestions]
