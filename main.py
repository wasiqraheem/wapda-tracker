import flet as ft
from datetime import datetime, date, time, timedelta, timezone


def main(page: ft.Page):
    page.title = "WAPDA Multi-Meter Advanced Tracker"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = "auto"

    current_meter_name = ""

    # =========================================================
    # INPUT FIELDS
    # =========================================================

    prev_reading_input = ft.TextField(
        label="Previous Month Reading",
        keyboard_type=ft.KeyboardType.NUMBER
    )

    prev_units_input = ft.TextField(
        label="Previous Month Units Consumed",
        keyboard_type=ft.KeyboardType.NUMBER
    )

    prev_bill_input = ft.TextField(
        label="Previous Month Bill (Rs.)",
        keyboard_type=ft.KeyboardType.NUMBER
    )

    prev_date_input = ft.TextField(
        label="Previous Month Date",
        read_only=True,
        hint_text="Click to select date",
        on_click=lambda e: open_previous_date_picker()
    )

    current_reading_input = ft.TextField(
        label="Enter Current Reading",
        keyboard_type=ft.KeyboardType.NUMBER
    )

    current_date_input = ft.TextField(
        label="Current Reading Date",
        read_only=True,
        hint_text="Click to select date",
        on_click=lambda e: open_current_date_picker()
    )

    current_time_input = ft.TextField(
        label="Current Reading Time",
        read_only=True,
        hint_text="Click to select time",
        on_click=lambda e: open_time_picker()
    )

    # =========================================================
    # DETAIL SCREEN
    # =========================================================

    current_meter_title = ft.Text(
        "Select a Meter",
        size=24,
        weight=ft.FontWeight.BOLD
    )

    last_current_status = ft.Text(
        "",
        size=14,
        color=ft.Colors.BLUE_GREY_700,
        weight=ft.FontWeight.BOLD
    )

    result_text = ft.Text(
        "",
        size=16,
        color=ft.Colors.GREEN_700,
        weight=ft.FontWeight.W_500
    )

    # =========================================================
    # DASHBOARD
    # =========================================================

    meter1_summary_text = ft.Text(
        "Loading Meter 1...",
        size=14,
        color=ft.Colors.BLACK
    )

    meter2_summary_text = ft.Text(
        "Loading Meter 2...",
        size=14,
        color=ft.Colors.BLACK
    )

    # Combined total for both meters
    both_meters_total_text = ft.Text(
        "Loading total...",
        size=16,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLACK
    )

    # =========================================================
    # DATE PICKERS
    # =========================================================

    previous_date_picker = ft.DatePicker(
        first_date=date(2000, 1, 1),
        last_date=date(2100, 12, 31),
        on_change=lambda e: previous_date_selected(e)
    )

    current_date_picker = ft.DatePicker(
        first_date=date(2000, 1, 1),
        last_date=date(2100, 12, 31),
        on_change=lambda e: current_date_selected(e)
    )

    # =========================================================
    # TIME PICKER
    # =========================================================

    current_time_picker = ft.TimePicker(
        on_change=lambda e: current_time_selected(e)
    )

    page.overlay.append(previous_date_picker)
    page.overlay.append(current_date_picker)
    page.overlay.append(current_time_picker)

    # =========================================================
    # PREVIOUS DATE PICKER
    # =========================================================

    def open_previous_date_picker():

        try:
            if prev_date_input.value:
                selected_date = datetime.strptime(
                    prev_date_input.value,
                    "%Y-%m-%d"
                ).date()

                previous_date_picker.value = datetime.combine(
                    selected_date, time.min
                )
            else:
                previous_date_picker.value = datetime.combine(
                    date.today(), time.min
                )

        except Exception:
            previous_date_picker.value = datetime.combine(
                    date.today(), time.min
                )

        previous_date_picker.open = True
        page.update()

    def _event_datetime_pakistan(raw_value):
        """Convert Flet DatePicker event data to Pakistan local time.

        Flet may send the selected midnight as a UTC ISO timestamp.
        For Pakistan (UTC+05:00), that can otherwise appear as the
        previous calendar date.
        """
        if not raw_value:
            return None

        if isinstance(raw_value, datetime):
            if raw_value.tzinfo is not None:
                return raw_value.astimezone(
                    timezone(timedelta(hours=5))
                ).replace(tzinfo=None)
            return raw_value

        if isinstance(raw_value, str):
            text = raw_value.strip()

            # Plain date: no conversion is needed.
            if len(text) >= 10 and text[4] == "-" and text[7] == "-":
                if "T" not in text and " " not in text:
                    return datetime.strptime(text[:10], "%Y-%m-%d")

            # ISO datetime, including values ending in Z.
            try:
                iso_text = text.replace("Z", "+00:00")
                dt = datetime.fromisoformat(iso_text)
                if dt.tzinfo is not None:
                    dt = dt.astimezone(
                        timezone(timedelta(hours=5))
                    ).replace(tzinfo=None)
                return dt
            except ValueError:
                pass

        return None

    def previous_date_selected(e):
        raw_value = getattr(e, "data", None)
        selected_dt = _event_datetime_pakistan(raw_value)

        if selected_dt:
            prev_date_input.value = selected_dt.strftime("%Y-%m-%d")
            page.update()

    # =========================================================
    # CURRENT DATE PICKER
    # =========================================================

    def open_current_date_picker():

        try:
            if current_date_input.value:

                selected_date = datetime.strptime(
                    current_date_input.value,
                    "%Y-%m-%d"
                ).date()

                current_date_picker.value = datetime.combine(
                    selected_date, time.min
                )

            else:

                current_date_picker.value = datetime.combine(
                    date.today(), time.min
                )

        except Exception:

            current_date_picker.value = datetime.combine(
                    date.today(), time.min
                )

        current_date_picker.open = True
        page.update()

    def current_date_selected(e):
        raw_value = getattr(e, "data", None)
        selected_dt = _event_datetime_pakistan(raw_value)

        if selected_dt:
            current_date_input.value = selected_dt.strftime("%Y-%m-%d")
            page.update()

    # =========================================================
    # TIME PICKER
    # =========================================================

    def open_time_picker():

        try:

            if current_time_input.value:

                selected_time = datetime.strptime(
                    current_time_input.value,
                    "%H:%M:%S"
                ).time()

                current_time_picker.value = selected_time

            else:

                now = datetime.now()

                current_time_picker.value = time(
                    now.hour,
                    now.minute,
                    now.second
                )

        except Exception:

            now = datetime.now()

            current_time_picker.value = time(
                now.hour,
                now.minute,
                now.second
            )

        current_time_picker.open = True
        page.update()

    def current_time_selected(e):
        raw_value = getattr(e, "data", None)

        if raw_value:
            try:
                if isinstance(raw_value, str):
                    text = raw_value.strip()

                    # If Flet sends an ISO datetime, convert UTC to
                    # Pakistan local time before extracting the time.
                    if "T" in text or "Z" in text or "+" in text[8:]:
                        selected_dt = _event_datetime_pakistan(text)
                        if selected_dt:
                            current_time_input.value = selected_dt.strftime(
                                "%H:%M:%S"
                            )
                    else:
                        # Normal TimePicker value, e.g. 14:30:00.
                        time_text = text[:8]
                        datetime.strptime(time_text, "%H:%M:%S")
                        current_time_input.value = time_text
                else:
                    current_time_input.value = raw_value.strftime(
                        "%H:%M:%S"
                    )

                page.update()
                return

            except (ValueError, TypeError, AttributeError):
                pass

        # Final fallback: use the picker's value directly.
        if current_time_picker.value:
            current_time_input.value = current_time_picker.value.strftime(
                "%H:%M:%S"
            )
            page.update()

    # =========================================================
    # UPDATE DASHBOARD SUMMARY
    # =========================================================

    async def update_main_dashboard_summary():

        # Combined totals
        m1_total_units = None
        m1_total_bill = None
        m2_total_units = None
        m2_total_bill = None

        # =====================================================
        # METER 1
        # =====================================================

        m1_r = await page.shared_preferences.get(
            "Meter 1_last_curr_reading"
        )

        m1_t = await page.shared_preferences.get(
            "Meter 1_last_curr_time"
        )

        m1_base_r = await page.shared_preferences.get(
            "Meter 1_prev_reading"
        )
        m1_base_u = await page.shared_preferences.get(
            "Meter 1_prev_units"
        )
        m1_base_b = await page.shared_preferences.get(
            "Meter 1_prev_bill"
        )

        if m1_r and m1_t:

            try:

                u_used = (
                    float(m1_r) -
                    float(m1_base_r or 0)
                )

                estimated_bill = None
                if m1_base_u and m1_base_b and float(m1_base_u) > 0:
                    estimated_bill = u_used * (float(m1_base_b) / float(m1_base_u))

                m1_total_units = u_used
                m1_total_bill = estimated_bill

                if estimated_bill is not None:
                    meter1_summary_text.value = (
                        f"Last Reading: {m1_r} Units\n"
                        f"Checked: {m1_t}\n"
                        f"Total Consumed: {u_used:.2f} Units\n"
                        f"Estimated Bill: Rs. {estimated_bill:,.2f}"
                    )
                else:
                    meter1_summary_text.value = (
                        f"Last Reading: {m1_r} Units\n"
                        f"Checked: {m1_t}\n"
                        f"Total Consumed: {u_used:.2f} Units\n"
                        f"Estimated Bill: Not available"
                    )

            except ValueError:

                meter1_summary_text.value = (
                    f"Last Reading: {m1_r} Units\n"
                    f"Checked: {m1_t}"
                )

        else:

            meter1_summary_text.value = (
                "No history found. Tap below to manage."
            )

        # =====================================================
        # METER 2
        # =====================================================

        m2_r = await page.shared_preferences.get(
            "Meter 2_last_curr_reading"
        )

        m2_t = await page.shared_preferences.get(
            "Meter 2_last_curr_time"
        )

        m2_base_r = await page.shared_preferences.get(
            "Meter 2_prev_reading"
        )
        m2_base_u = await page.shared_preferences.get(
            "Meter 2_prev_units"
        )
        m2_base_b = await page.shared_preferences.get(
            "Meter 2_prev_bill"
        )

        if m2_r and m2_t:

            try:

                u_used = (
                    float(m2_r) -
                    float(m2_base_r or 0)
                )

                estimated_bill = None
                if m2_base_u and m2_base_b and float(m2_base_u) > 0:
                    estimated_bill = u_used * (float(m2_base_b) / float(m2_base_u))

                m2_total_units = u_used
                m2_total_bill = estimated_bill

                if estimated_bill is not None:
                    meter2_summary_text.value = (
                        f"Last Reading: {m2_r} Units\n"
                        f"Checked: {m2_t}\n"
                        f"Total Consumed: {u_used:.2f} Units\n"
                        f"Estimated Bill: Rs. {estimated_bill:,.2f}"
                    )
                else:
                    meter2_summary_text.value = (
                        f"Last Reading: {m2_r} Units\n"
                        f"Checked: {m2_t}\n"
                        f"Total Consumed: {u_used:.2f} Units\n"
                        f"Estimated Bill: Not available"
                    )

            except ValueError:

                meter2_summary_text.value = (
                    f"Last Reading: {m2_r} Units\n"
                    f"Checked: {m2_t}"
                )

        else:

            meter2_summary_text.value = (
                "No history found. Tap below to manage."
            )

        # =====================================================
        # BOTH METERS TOTAL
        # =====================================================
        if (m1_total_units is not None and m2_total_units is not None
                and m1_total_bill is not None and m2_total_bill is not None):
            combined_units = m1_total_units + m2_total_units
            combined_bill = m1_total_bill + m2_total_bill
            both_meters_total_text.value = (
                f"Total Consumed: {combined_units:.2f} Units\n"
                f"Total Estimated Bill: Rs. {combined_bill:,.2f}"
            )
        else:
            both_meters_total_text.value = (
                "Total Consumed: Not available\n"
                "Total Estimated Bill: Not available"
            )

        page.update()

    # =========================================================
    # CALCULATE & SAVE
    # =========================================================

    async def on_calculate_click(e):

        nonlocal current_meter_name

        try:

            # -------------------------------------------------
            # INPUT VALUES
            # -------------------------------------------------

            prev_r = float(
                prev_reading_input.value
            )

            prev_u = float(
                prev_units_input.value
            )

            prev_b = float(
                prev_bill_input.value
            )

            new_curr_r = float(
                current_reading_input.value
            )

            # -------------------------------------------------
            # PREVIOUS DATE
            # -------------------------------------------------

            base_date = datetime.strptime(
                prev_date_input.value,
                "%Y-%m-%d"
            )

            # -------------------------------------------------
            # CURRENT DATE
            # -------------------------------------------------

            selected_date = datetime.strptime(
                current_date_input.value,
                "%Y-%m-%d"
            ).date()

            # -------------------------------------------------
            # CURRENT TIME
            # -------------------------------------------------

            selected_time = datetime.strptime(
                current_time_input.value,
                "%H:%M:%S"
            ).time()

            # Combine date and time
            now_time = datetime.combine(
                selected_date,
                selected_time
            )

            # -------------------------------------------------
            # VALIDATION
            # -------------------------------------------------

            if new_curr_r < prev_r:

                result_text.value = (
                    "Error: New reading cannot be "
                    "less than base!"
                )

                page.update()
                return

            if prev_u <= 0:

                result_text.value = (
                    "Error: Previous units must be > 0!"
                )

                page.update()
                return

            if now_time < base_date:

                result_text.value = (
                    "Error: Current reading date/time "
                    "cannot be before previous month date!"
                )

                page.update()
                return

            # =================================================
            # PREVIOUS SNAPSHOT
            # =================================================

            old_curr_r_str = (
                await page.shared_preferences.get(
                    f"{current_meter_name}_last_curr_reading"
                )
            )

            old_curr_time_str = (
                await page.shared_preferences.get(
                    f"{current_meter_name}_last_curr_time"
                )
            )

            # =================================================
            # CALCULATIONS
            # =================================================

            calculated_per_unit_rate = (
                prev_b / prev_u
            )

            total_days_from_base = (
                now_time - base_date
            ).days

            if total_days_from_base <= 0:
                total_days_from_base = 1

            total_units_from_base = (
                new_curr_r - prev_r
            )

            per_day_units_base = (
                total_units_from_base /
                total_days_from_base
            )

            total_cost_from_base = (
                total_units_from_base *
                calculated_per_unit_rate
            )

            # =================================================
            # INTERVAL COMPARISON
            # =================================================

            intermediate_report = ""

            if old_curr_r_str and old_curr_time_str:

                try:

                    old_curr_r = float(
                        old_curr_r_str
                    )

                    old_curr_time = datetime.strptime(
                        old_curr_time_str,
                        "%Y-%m-%d %H:%M:%S"
                    )

                    if now_time >= old_curr_time:

                        time_delta = (
                            now_time -
                            old_curr_time
                        )

                        total_seconds = int(
                            time_delta.total_seconds()
                        )

                        delta_days = (
                            total_seconds // 86400
                        )

                        remaining_seconds = (
                            total_seconds % 86400
                        )

                        delta_hours = (
                            remaining_seconds // 3600
                        )

                        delta_minutes = (
                            (remaining_seconds % 3600)
                            // 60
                        )

                        inter_units = (
                            new_curr_r -
                            old_curr_r
                        )

                        inter_cost = (
                            inter_units *
                            calculated_per_unit_rate
                        )

                        intermediate_report = (
                            "\n\n"
                            "INTERVAL COMPARISON:\n"
                            f"Since Last Check "
                            f"({old_curr_time_str}):\n"
                            f"Time Passed: "
                            f"{delta_days} days, "
                            f"{delta_hours} hours, "
                            f"{delta_minutes} minutes\n"
                            f"Units Consumed: "
                            f"{inter_units:.2f}\n"
                            f"Price: Rs. "
                            f"{inter_cost:.2f}"
                        )

                    else:

                        intermediate_report = (
                            "\n\n"
                            "INTERVAL COMPARISON:\n"
                            "Current date/time is earlier "
                            "than previous snapshot."
                        )

                except ValueError:

                    intermediate_report = ""

            # =================================================
            # SAVE PREVIOUS MONTH DATA
            # =================================================

            await page.shared_preferences.set(
                f"{current_meter_name}_prev_reading",
                prev_reading_input.value
            )

            await page.shared_preferences.set(
                f"{current_meter_name}_prev_units",
                prev_units_input.value
            )

            await page.shared_preferences.set(
                f"{current_meter_name}_prev_bill",
                prev_bill_input.value
            )

            await page.shared_preferences.set(
                f"{current_meter_name}_prev_date",
                prev_date_input.value
            )

            # =================================================
            # SAVE CURRENT READING
            # =================================================

            current_timestamp_str = (
                now_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            await page.shared_preferences.set(
                f"{current_meter_name}_last_curr_reading",
                str(new_curr_r)
            )

            await page.shared_preferences.set(
                f"{current_meter_name}_last_curr_time",
                current_timestamp_str
            )

            # =================================================
            # RESULT
            # =================================================

            result_text.value = (
                f"MONTHLY SUMMARY FOR "
                f"{current_meter_name}:\n"
                f"Current Time: "
                f"{current_timestamp_str}\n"
                f"Total Days: "
                f"{total_days_from_base}\n"
                f"Total Units: "
                f"{total_units_from_base:.2f}\n"
                f"Per Day: "
                f"{per_day_units_base:.2f}\n"
                f"Rate: Rs. "
                f"{calculated_per_unit_rate:.2f}/unit\n"
                f"Bill: Rs. "
                f"{total_cost_from_base:.2f}"
                f"{intermediate_report}\n\n"
                f"Saved!"
            )

            last_current_status.value = (
                f"Last Checked: "
                f"{new_curr_r} Units on "
                f"{current_timestamp_str}"
            )

            await update_main_dashboard_summary()

        except ValueError:

            result_text.value = (
                "Please enter valid numeric values!"
            )

            page.update()

    # =========================================================
    # SHOW METER SCREEN
    # =========================================================

    async def show_meter_screen(meter_name):

        nonlocal current_meter_name

        current_meter_name = meter_name

        current_meter_title.value = meter_name

        # -----------------------------------------------------
        # LOAD PREVIOUS READING
        # -----------------------------------------------------

        prev_reading_input.value = (
            await page.shared_preferences.get(
                f"{meter_name}_prev_reading"
            ) or ""
        )

        # -----------------------------------------------------
        # LOAD PREVIOUS UNITS
        # -----------------------------------------------------

        prev_units_input.value = (
            await page.shared_preferences.get(
                f"{meter_name}_prev_units"
            ) or ""
        )

        # -----------------------------------------------------
        # LOAD PREVIOUS BILL
        # -----------------------------------------------------

        prev_bill_input.value = (
            await page.shared_preferences.get(
                f"{meter_name}_prev_bill"
            ) or ""
        )

        # -----------------------------------------------------
        # LOAD PREVIOUS DATE
        # -----------------------------------------------------

        prev_date_input.value = (
            await page.shared_preferences.get(
                f"{meter_name}_prev_date"
            ) or ""
        )

        # -----------------------------------------------------
        # LOAD LAST CURRENT READING
        # -----------------------------------------------------

        old_r = await page.shared_preferences.get(
            f"{meter_name}_last_curr_reading"
        )

        old_t = await page.shared_preferences.get(
            f"{meter_name}_last_curr_time"
        )

        if old_r and old_t:

            last_current_status.value = (
                f"Last Checked: {old_r} Units "
                f"on {old_t}"
            )

        else:

            last_current_status.value = (
                "No previous snapshot found."
            )

        # -----------------------------------------------------
        # CURRENT DATE & TIME
        # -----------------------------------------------------

        current_date_input.value = (
            datetime.now().strftime(
                "%Y-%m-%d"
            )
        )

        current_time_input.value = (
            datetime.now().strftime(
                "%H:%M:%S"
            )
        )

        current_reading_input.value = ""

        result_text.value = ""

        meter_ui.visible = True
        main_menu.visible = False

        page.update()

    # =========================================================
    # BACK TO DASHBOARD
    # =========================================================

    def show_main_menu(e=None):

        main_menu.visible = True
        meter_ui.visible = False

        page.update()

    # =========================================================
    # CLEAR METER DATA
    # =========================================================

    async def clear_meter_data(meter_name):

        data_types = [
            "prev_reading",
            "prev_units",
            "prev_bill",
            "prev_date",
            "last_curr_reading",
            "last_curr_time"
        ]

        # -----------------------------------------------------
        # DELETE ONLY SELECTED METER DATA
        # -----------------------------------------------------

        for data_type in data_types:

            key = (
                f"{meter_name}_{data_type}"
            )

            await page.shared_preferences.remove(
                key
            )

        # -----------------------------------------------------
        # RESET CURRENT FORM IF SAME METER IS OPEN
        # -----------------------------------------------------

        if current_meter_name == meter_name:

            prev_reading_input.value = ""
            prev_units_input.value = ""
            prev_bill_input.value = ""
            prev_date_input.value = ""
            current_reading_input.value = ""

            current_date_input.value = (
                datetime.now().strftime(
                    "%Y-%m-%d"
                )
            )

            current_time_input.value = (
                datetime.now().strftime(
                    "%H:%M:%S"
                )
            )

            last_current_status.value = (
                "No previous snapshot found."
            )

            result_text.value = ""

        # -----------------------------------------------------
        # UPDATE DASHBOARD
        # -----------------------------------------------------

        await update_main_dashboard_summary()

    # =========================================================
    # CLOSE CLEAR DIALOG
    # =========================================================

    def close_clear_dialog():

        clear_dialog.open = False

        page.update()

    # =========================================================
    # CONFIRM CLEAR METER DATA
    # =========================================================

    async def confirm_clear_meter_data(meter_name):

        clear_dialog.open = False

        await clear_meter_data(
            meter_name
        )

        page.snack_bar = ft.SnackBar(
            content=ft.Text(
                f"{meter_name} data cleared successfully."
            )
        )

        page.snack_bar.open = True

        page.update()

    # =========================================================
    # SHOW CLEAR CONFIRMATION
    # =========================================================

    def show_clear_confirmation(meter_name):

        clear_dialog.title = ft.Text(
            f"Clear {meter_name} Data?"
        )

        clear_dialog.content = ft.Text(
            f"This will permanently delete ALL saved "
            f"data of {meter_name}.\n\n"
            f"The following data will be deleted:\n\n"
            f"• Previous month reading\n"
            f"• Previous month units\n"
            f"• Previous month bill\n"
            f"• Previous month date\n"
            f"• Last current reading\n"
            f"• Last current date/time\n\n"
            f"Data of the other meter will NOT be affected.\n\n"
            f"This action cannot be undone."
        )

        clear_dialog.actions = [

            ft.TextButton(
                "Cancel",
                on_click=lambda e: close_clear_dialog()
            ),

            ft.ElevatedButton(
                f"Yes, Clear {meter_name}",
                on_click=lambda e: page.run_task(
                    confirm_clear_meter_data,
                    meter_name
                ),
                bgcolor=ft.Colors.RED_700,
                color=ft.Colors.WHITE
            )
        ]

        clear_dialog.open = True

        page.update()

    # =========================================================
    # CLEAR DATA DIALOG
    # =========================================================

    clear_dialog = ft.AlertDialog(
        modal=True,

        title=ft.Text(
            "Clear Meter Data?"
        ),

        content=ft.Text(
            "Please confirm."
        ),

        actions_alignment=ft.MainAxisAlignment.END
    )

    page.overlay.append(clear_dialog)

    # =========================================================
    # MAIN DASHBOARD
    # =========================================================

    main_menu = ft.Column(
        [

            ft.Text(
                "WAPDA Dashboard",
                size=28,
                weight=ft.FontWeight.BOLD
            ),

            ft.Text(
                "Current status of your residential meters:",
                size=14
            ),

            ft.Container(height=10),

            # =================================================
            # BOTH METERS TOTAL CARD
            # =================================================

            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Both Meters Total",
                            size=20,
                            weight=ft.FontWeight.BOLD
                        ),
                        both_meters_total_text
                    ],
                    spacing=8
                ),
                padding=20,
                border_radius=10
            ),

            # =================================================
            # METER 1 CARD
            # =================================================

            ft.Container(
                content=ft.Column(
                    [

                        ft.Text(
                            "Meter 1 Summary",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_900
                        ),

                        meter1_summary_text,

                        ft.ElevatedButton(
                            "Open Meter 1",
                            on_click=lambda e: page.run_task(
                                show_meter_screen,
                                "Meter 1"
                            ),
                            bgcolor=ft.Colors.BLUE_700,
                            color=ft.Colors.WHITE
                        )
                    ],
                    spacing=10
                ),

                padding=20,

                bgcolor=ft.Colors.BLUE_50,

                border_radius=10
            ),

            # =================================================
            # METER 2 CARD
            # =================================================

            ft.Container(
                content=ft.Column(
                    [

                        ft.Text(
                            "Meter 2 Summary",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_900
                        ),

                        meter2_summary_text,

                        ft.ElevatedButton(
                            "Open Meter 2",
                            on_click=lambda e: page.run_task(
                                show_meter_screen,
                                "Meter 2"
                            ),
                            bgcolor=ft.Colors.GREEN_700,
                            color=ft.Colors.WHITE
                        )
                    ],
                    spacing=10
                ),

                padding=20,

                bgcolor=ft.Colors.GREEN_50,

                border_radius=10
            ),

            ft.Divider(),

            # =================================================
            # DATA MANAGEMENT
            # =================================================

            ft.Text(
                "Data Management",
                size=18,
                weight=ft.FontWeight.BOLD
            ),

            ft.Text(
                "Clear saved data separately for each meter.",
                size=13,
                color=ft.Colors.BLUE_GREY_700
            ),

            ft.Row(
                [

                    ft.ElevatedButton(
                        "Clear Meter 1 Data",
                        icon=ft.Icons.DELETE_FOREVER,
                        on_click=lambda e:
                            show_clear_confirmation(
                                "Meter 1"
                            ),
                        bgcolor=ft.Colors.RED_700,
                        color=ft.Colors.WHITE
                    ),

                    ft.ElevatedButton(
                        "Clear Meter 2 Data",
                        icon=ft.Icons.DELETE_FOREVER,
                        on_click=lambda e:
                            show_clear_confirmation(
                                "Meter 2"
                            ),
                        bgcolor=ft.Colors.RED_700,
                        color=ft.Colors.WHITE
                    )
                ],

                spacing=10,

                wrap=True
            )
        ],

        spacing=15
    )

    # =========================================================
    # METER DETAIL UI
    # =========================================================

    meter_ui = ft.Column(
        [

            ft.Row(
                [

                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=show_main_menu
                    ),

                    ft.TextButton(
                        "Back to Dashboard",
                        on_click=show_main_menu
                    )
                ]
            ),

            current_meter_title,

            last_current_status,

            ft.Divider(),

            prev_reading_input,

            prev_units_input,

            prev_bill_input,

            prev_date_input,

            ft.Divider(),

            current_reading_input,

            current_date_input,

            current_time_input,

            ft.Text(
                "Current date and time are automatically "
                "set to now. Click the fields to change them.",
                size=12,
                color=ft.Colors.BLUE_GREY_600
            ),

            ft.ElevatedButton(
                "Calculate & Save Data",
                on_click=lambda e: page.run_task(
                    on_calculate_click,
                    e
                ),
                bgcolor=ft.Colors.BLUE,
                color=ft.Colors.WHITE
            ),

            ft.Divider(),

            result_text,

            ft.ElevatedButton(
                "Go Back to Dashboard",
                on_click=show_main_menu,
                bgcolor=ft.Colors.GREY_400,
                color=ft.Colors.BLACK
            )
        ],

        visible=False,

        spacing=15
    )

    # =========================================================
    # ADD UI
    # =========================================================

    page.add(
        main_menu,
        meter_ui
    )

    # =========================================================
    # LOAD DASHBOARD
    # =========================================================

    page.run_task(
        update_main_dashboard_summary
    )


# =============================================================
# START APP
# =============================================================

ft.app(target=main)
