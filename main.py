import i18n
from dash import Dash
import dash_bootstrap_components as dpc
import dash_bootstrap_templates as dpt


from src.components.layout import create_layout
from src.data.loader import load_transaction_data
from src.data.source import DataSource

LOCALE = "de"
DATA_PATH = "./data/transactions.csv"

dpt.load_figure_template("Solar")

def main() -> None:

    # set the locale and load the translations
    i18n.set("locale", LOCALE)
    i18n.load_path.append("locale")

    # load the data and create the data manager
    data = load_transaction_data(DATA_PATH, LOCALE)
    data = DataSource(data)

    app = Dash(external_stylesheets=[dpc.themes.SOLAR])
    app.title = i18n.t("general.app_title")
    app.layout = create_layout(app, data)

    server = app.server

    app.run(host="0.0.0.0", port=4000, debug=False)


if __name__ == "__main__":
    main()
