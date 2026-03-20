from shared.timed_page import TimedPage


class Conclusion(TimedPage):
    def vars_for_template(self):
        return dict(
            prolific_completion_url=self.session.config.get(
                'prolific_completion_url', ''
            ),
        )


page_sequence = [Conclusion]
