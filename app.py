import requests
from bs4 import BeautifulSoup
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State

# Função para realizar a busca no Google
def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    search_results = soup.find_all("div", class_="g")
    results = []
    for result in search_results:
        title = result.find("h3").text
        link = result.find("a")["href"]
        results.append({"title": title, "link": link})
    return results

# Criação do aplicativo Dash
app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center",
        "justify-content": "center",
        "height": "100vh",
        "font-family": "Arial, sans-serif"
    },
    children=[
        html.H1("Meu Google - By: tondevpy", style={"margin-bottom": "20px"}),
        dcc.Input(
            id="search-input",
            type="text",
            placeholder="Digite sua busca",
            style={"width": "300px", "margin-bottom": "10px"}
        ),
        html.Button("Buscar", id="search-button", style={"padding": "8px 16px"}),
        html.Div(id="search-results", style={"margin-top": "20px"}),
        html.Div(id="page-count")
    ]
)

@app.callback(
    [Output("search-results", "children"), Output("page-count", "children")],
    [Input("search-button", "n_clicks")],
    [State("search-input", "value")]
)
def perform_search(n_clicks, search_input):
    if n_clicks is not None and search_input:
        results = search_google(search_input)
        if results:
            result_items = [
                html.Div(
                    [
                        html.H3(result["title"], style={"margin-bottom": "5px"}),
                        html.A(result["link"], href=result["link"], target="_blank", style={"color": "blue"})
                    ],
                    style={"margin-bottom": "15px"}
                ) for result in results
            ]
            page_count = html.P(f"Total de resultados encontrados: {len(results)}", style={"font-weight": "bold"})
            return result_items, page_count
        else:
            return html.Div("Nenhum resultado encontrado."), None
    return "", None

if __name__ == "__main__":
    app.run_server(debug=True)
