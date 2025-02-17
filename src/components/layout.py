from dash import Dash, html
import dash_bootstrap_components as dpc

from src.components import (
    bar_chart,
    category_dropdown,
    month_dropdown,
    pie_chart,
    year_dropdown,
)

from ..data.source import DataSource


def create_layout(app: Dash, source: DataSource) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[
                    dpc.Row([
                        dpc.Col([year_dropdown.render(app, source),
                                month_dropdown.render(app, source),
                                category_dropdown.render(app, source)]),
                        dpc.Col([bar_chart.render(app, source),
                                pie_chart.render(app, source),
                                ], width=9),
                    ])

                ],
            ),

        ],
    )
