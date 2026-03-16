from shared.timed_page import TimedPage


class Conclusion(TimedPage):
    def vars_for_template(self):
        return dict(
            conclusion='Thank you for participating in the study.',
        )


page_sequence = [Conclusion]
