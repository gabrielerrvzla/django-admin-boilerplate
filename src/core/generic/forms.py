from crispy_forms.layout import HTML


class Link(HTML):
    """
    A button that goes back to the previous page.
    """

    def __init__(self, label: str, url: str, css_class: str = None):
        super().__init__(f'<a href="{url}" class="{css_class}">{label}</a>')
