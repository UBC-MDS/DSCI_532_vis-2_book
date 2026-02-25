from shiny import App, ui

# Block 1 synthesis — Bootstrap 5 + page_fillable + inline CSS + styled header
# Demonstrates all Block 1 UI patterns in one coherent app (no data dependencies).

# Header: Bootstrap classes only — bg-primary is theme-aware.
# d-flex + justify-content-between pushes badge to the right without custom CSS.
header = ui.div(
    ui.div(
        ui.h1("Dashboard Explorer", class_="mb-0 fs-3"),
        ui.p("Bootstrap 5 · Shiny UI patterns", class_="mb-0 opacity-75 small"),
    ),
    ui.tags.span("v1.0", class_="badge bg-light text-dark"),
    class_="bg-primary text-white p-4 mb-0 d-flex justify-content-between align-items-center",
)

app_ui = ui.page_fillable(
    header,
    ui.layout_columns(
        # --- Card 1: Bootstrap utility classes ---
        ui.card(
            ui.card_header("Bootstrap utility classes"),
            ui.div(
                ui.p("Spacing, colour, and flex — no custom CSS needed:", class_="text-muted small mb-3"),
                # Status badge in a flex row
                ui.div(
                    ui.span("Status", class_="fw-semibold"),
                    ui.tags.span("Active", class_="badge bg-success ms-2"),
                    class_="d-flex align-items-center mb-2",
                ),
                # Muted helper text
                ui.p("Secondary info", class_="text-muted small mb-2"),
                # Light bordered panel — border + rounded + bg-light, all Bootstrap
                ui.div("Bordered panel", class_="border rounded p-2 bg-light text-center text-muted small"),
            ),
        ),
        # --- Card 2: Inline CSS — brand colour only ---
        ui.card(
            ui.card_header("Inline CSS — targeted tweaks"),
            ui.div(
                ui.p("Use style= only for values Bootstrap can't express:", class_="text-muted small mb-3"),
                # Custom brand colour has no Bootstrap equivalent → style=
                ui.div(
                    "Brand accent panel",
                    class_="text-white p-3 rounded mb-2 fw-semibold",
                    style="background-color: #6f42c1;",
                ),
                # Fine-grained font metrics outside Bootstrap's scale
                ui.p(
                    "Fine print — 0.72 rem, tracked",
                    style="font-size: 0.72rem; letter-spacing: 0.05em; color: #6B7280;",
                ),
            ),
        ),
        # --- Card 3: page_fillable note ---
        ui.card(
            ui.card_header("page_fillable"),
            ui.div(
                ui.p("Cards fill the viewport vertically.", class_="text-muted small mb-3"),
                ui.div(
                    ui.p("Each card stretches to use available space.", class_="mb-1"),
                    ui.p("Set fill=False on an item to opt out.", class_="mb-0 text-muted small"),
                    class_="border-start border-primary border-3 ps-3",
                ),
            ),
        ),
        col_widths=[4, 4, 4],
    ),
)


def server(input, output, session):
    pass


app = App(app_ui, server)
