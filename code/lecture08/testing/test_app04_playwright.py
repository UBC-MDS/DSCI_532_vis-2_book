from shiny.playwright import controller
from shiny.run import ShinyAppProc
from shiny.pytest import create_app_fixture
from playwright.sync_api import Page

app = create_app_fixture("app-04-button-playwright.py")


def test_initial_value_boxes(page: Page, app: ShinyAppProc) -> None:
    """All three value boxes show correct stats for the full dataset."""
    page.goto(app.url)

    controller.OutputText(page, "total_tippers").expect_value("244")
    controller.OutputText(page, "average_tip").expect_value("16.1%")
    controller.OutputText(page, "average_bill").expect_value("$19.79")


def test_dataframe_initial_structure(page: Page, app: ShinyAppProc) -> None:
    """Summary dataframe has correct columns and one row per day (4 days)."""
    page.goto(app.url)

    tips_data = controller.OutputDataFrame(page, "tips_data")
    tips_data.expect_ncol(5)
    tips_data.expect_column_labels(
        ["day", "count", "avg_bill", "avg_tip", "avg_tip_pct"]
    )
    tips_data.expect_nrow(4)


def test_dataframe_cell_values(page: Page, app: ShinyAppProc) -> None:
    """Spot-check a known cell value in the summary dataframe."""
    page.goto(app.url)

    tips_data = controller.OutputDataFrame(page, "tips_data")
    # The tips dataset has 87 Saturday dinners
    tips_data.expect_cell("Sat", row=2, col=0)
    tips_data.expect_cell("87", row=2, col=1)


def test_checkbox_filter_lunch_only(page: Page, app: ShinyAppProc) -> None:
    """Deselecting Dinner filters to 68 lunch rows across 2 days."""
    page.goto(app.url)

    checkbox = controller.InputCheckboxGroup(page, "checkbox_group")
    checkbox.set(["Lunch"])
    checkbox.expect_selected(["Lunch"])

    text = controller.OutputText(page, "total_tippers")
    text.expect_value("68")

    # Only Thur and Fri have lunch sittings
    df = controller.OutputDataFrame(page, "tips_data")
    df.expect_nrow(2)


def test_checkbox_filter_dinner_only(page: Page, app: ShinyAppProc) -> None:
    """Deselecting Lunch filters to 176 dinner rows across 4 days."""
    page.goto(app.url)

    checkbox = controller.InputCheckboxGroup(page, "checkbox_group")
    checkbox.set(["Dinner"])

    controller.OutputText(page, "total_tippers").expect_value("176")
    controller.OutputDataFrame(page, "tips_data").expect_nrow(4)


def test_reset_button_restores_defaults(page: Page, app: ShinyAppProc) -> None:
    """Reset button returns all filters to their initial state."""
    page.goto(app.url)

    checkbox = controller.InputCheckboxGroup(page, "checkbox_group")
    reset_btn = controller.InputActionButton(page, "action_button")
    total_tippers = controller.OutputText(page, "total_tippers")

    # Change the filter, confirm it took effect
    checkbox.set(["Dinner"])
    total_tippers.expect_value("176")

    # Click reset and verify everything is restored
    reset_btn.click()
    total_tippers.expect_value("244")
    checkbox.expect_selected(["Lunch", "Dinner"])


def test_reset_button_restores_slider(page: Page, app: ShinyAppProc) -> None:
    """Reset button restores the slider to the full bill range."""
    page.goto(app.url)

    slider = controller.InputSliderRange(page, "slider")
    reset_btn = controller.InputActionButton(page, "action_button")

    # Narrow the slider range, then reset
    slider.set(("10", "30"), max_err_values=25)
    reset_btn.click()

    slider.expect_min("3.07")
    slider.expect_max("50.81")
