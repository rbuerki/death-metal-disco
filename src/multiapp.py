"""Framework for running multiple Streamlit applications as a single app.

Usage (in 'main' app.py):
    def foo():
        st.title("Hello Foo")
    def bar():
        st.title("Hello Bar")
    app = MultiApp()
    app.add_app("Foo", foo)
    app.add_app("Bar", bar)
    app.run_app()

It is also possible keep each application in a separate file:
    import foo
    import bar
    app = MultiApp()
    app.add_app("Foo", foo.app)
    app.add_app("Bar", bar.app)
    app.run_app()
"""

from typing import Callable

import streamlit as st


class MultiApp:
    """Framework for combining multiple streamlit applications. Is to
    be used in the main app module.
    """

    def __init__(self):
        self.apps = []

    def add_app(self, title: str, app_function: Callable):
        """Adds a new application. The title str appears in the
        navigation selectbox, the app_func is the actual function to
        render this app.
        """
        self.apps.append({"title": title, "app_function": app_function})

    def run_app(self, *args):
        """Adds a 'Navigation' Selectbox to the sidebar from which
        the added apps can be selected and runs the actually selected
        application within the main app. Optional args can be passed.
        """
        app = st.sidebar.selectbox(
            "Navigation", self.apps, format_func=lambda app: app["title"]
        )

        app["app_function"](*args)
