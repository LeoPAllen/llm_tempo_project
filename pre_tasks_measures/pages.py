from shared.timed_page import TimedPage


PRACTICE_OUTPUT = (
    'Animals like the arctic fox use camouflage, such as changing fur color from grey in '
    'the winter to brown in the summer, to blend into their environment.'
)


class PracticePage(TimedPage):
    form_model = 'player'
    form_fields = ['practice_io_history', 'practice_attention_check']

    def vars_for_template(self):
        return dict(
            practice_prompt=(
                'Summarize the main idea of the following paragraph: Camouflage is a vital survival '
                'strategy used by many species in the animal kingdom. It allows organisms to blend '
                'into their environments, reducing the likelihood of being detected by predators or '
                'prey. This biological adaptation takes many forms. In arctic regions, for example, '
                'the arctic fox changes the color of its fur with the seasons-white in the snowy '
                'winter and brown in the summer-to match its surroundings. In tropical rainforests, '
                'stick insects and leaf-tailed geckos closely resemble twigs, bark, or leaves, making '
                'them extremely difficult to spot. Some marine animals, like the octopus, can change '
                'both the color and texture of their skin in real time to mimic coral, sand, or rocks. '
                'These adaptations have evolved over thousands or even millions of years through '
                'natural selection: individuals that were slightly better camouflaged were more likely '
                'to survive and reproduce. Over generations, these traits became more common in the '
                "population. Camouflage doesn't only protect animals from predators-it can also help "
                'predators sneak up on prey. Tigers, for instance, use their striped fur to blend into '
                'tall grasses, helping them get close enough to ambush their target. Overall, camouflage '
                'is a dynamic and diverse evolutionary tool that plays a crucial role in the ongoing '
                'struggle for survival across many ecosystems.'
            ),
            llm_output=PRACTICE_OUTPUT,
        )

    def js_vars(self):
        return dict(practice_output=PRACTICE_OUTPUT)

    @staticmethod
    def live_method(player, data):
        return {player.id_in_group: dict(output=PRACTICE_OUTPUT, input=data.get('input', ''))}


class PreTaskMeasuresPage(TimedPage):
    form_model = 'player'
    form_fields = [
        'trust_automation_confident',
        'trust_automation_reliable',
        'trust_automation_trust',
        'need_for_cognition_effort',
        'need_for_cognition_enjoy',
        'need_for_cognition_avoid',
        'prior_llm_accuracy',
        'prior_algo_vs_human',
        'prior_llm_used_before',
        'prior_llm_judgment_conf',
        'self_rated_numeracy',
        'self_rated_reflection',
    ]


page_sequence = [PracticePage, PreTaskMeasuresPage]
