import reflex as rx
import httpx


class State(rx.State):

    matriz: str = ""
    vector: str = ""
    resultado: str = ""

    def set_matriz(self, value):
        self.matriz = value

    def set_vector(self, value):
        self.vector = value

    async def resolver(self):

        try:

            matriz = [
                [float(x) for x in fila.split()]
                for fila in self.matriz.strip().split("\n")
            ]

            vector = [
                float(x)
                for x in self.vector.strip().split("\n")
            ]

            payload = {
                "A": matriz,
                "b": vector
            }

            async with httpx.AsyncClient() as client:

                response = await client.post(
                    "http://127.0.0.1:8001/api/v1/cholesky",
                    json=payload,
                    timeout=30
                )

            if response.status_code != 200:
                self.resultado = response.text
                return

            data = response.json()

            solucion = "\n".join(
                [
                    f"x{i+1} = {valor:.6f}"
                    for i, valor in enumerate(data["solution"])
                ]
            )

            matriz_l = "\n".join(
                [
                    "   ".join(
                        f"{num:.4f}"
                        for num in fila
                    )
                    for fila in data["L"]
                ]
            )

            self.resultado = f"""
=========================================
MÉTODO CHOLESKY
=========================================

Método:
{data['method']}

Versión:
{data['version']}

Tamaño de matriz:
{data['matrix_size']} x {data['matrix_size']}

Tiempo de ejecución:
{data['execution_time_ms']} ms

Número de condición:
{data['condition_number']}

=========================================
SOLUCIÓN
=========================================

{solucion}

=========================================
MATRIZ L
=========================================

{matriz_l}
"""

        except Exception as e:

            self.resultado = f"""
ERROR

{str(e)}
"""


def index():

    return rx.container(

        rx.vstack(

            rx.heading(
                "Método Crout-Cholesky",
                size="9"
            ),

            rx.text(
                "Resolución de sistemas lineales mediante factorización Cholesky"
            ),

            rx.divider(),

            rx.heading(
                "Matriz A",
                size="5"
            ),

            rx.text_area(
                placeholder=
                "25 15 -5\n"
                "15 18 0\n"
                "-5 0 11",

                value=State.matriz,

                on_change=State.set_matriz,

                width="700px",
                height="220px"
            ),

            rx.heading(
                "Vector b",
                size="5"
            ),

            rx.text_area(
                placeholder=
                "350\n"
                "400\n"
                "200",

                value=State.vector,

                on_change=State.set_vector,

                width="700px",
                height="150px"
            ),

            rx.button(
                "Resolver Sistema",
                size="4",
                on_click=State.resolver
            ),

            rx.divider(),

            rx.heading(
                "Resultado",
                size="6"
            ),

            rx.text_area(
                value=State.resultado,
                read_only=True,
                width="900px",
                height="400px"
            ),

            spacing="5",
            width="100%"
        ),

        padding="40px"
    )


app = rx.App()
app.add_page(index)