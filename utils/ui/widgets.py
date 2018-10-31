from tkinter import ttk


class AutocompleteCombobox(ttk.Combobox):
    """
    - Exposes set_possible_values() method to set autocomplete source
    - Needs to have `textvariable` configured
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._possible_values = kwargs.get("values", [])

    def set_possible_values(self, values):
        self._possible_values = list(values)
        self._filter_matching()

    def configure(self, *args, **kwargs):
        """
        TODO: "untrace" when textvariable is reconfigured
        """
        var = kwargs.get("textvariable")
        if var is not None:
            var.trace("w", lambda *args: self._filter_matching())
        return super().configure(*args, **kwargs)

    def _filter_matching(self):
        current = self.get()
        if not current:
            self.configure(values=self._possible_values)
            return

        matched = [
            value for value in self._possible_values if current.lower() in value.lower()
        ]
        self.configure(values=matched)
