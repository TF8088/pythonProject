import os

from poo.pdf_poo import PDF
from datetime import date


def create_pdf_passengers(start_port, end_port, ship_name, routes, *forced_stops):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    pdf_path = os.path.join(script_dir, f'{start_port}_{end_port}_{date.today()}.pdf')

    pdf = PDF("Nautilus Logistics", start_port, end_port, ship_name, forced_stops)

    pdf.add_page()

    pdf.cell(0, 10, 'Route Information', 0, 1, 'C')

    pdf.ln(10)

    pdf.add_route_table(routes)

    pdf.add_qr_code_page()

    pdf.output(pdf_path)


def create_pdf(start_port, end_port, ship_name, routes, budget, travel_time, max_days, *forced_stops):

    script_dir = os.path.dirname(os.path.abspath(__file__))

    pdf_path = os.path.join(script_dir, f'{start_port}_{end_port}_{date.today()}.pdf')

    pdf = PDF("Nautilus Logistics", start_port, end_port, ship_name, forced_stops, budget=budget,
              travel_time=travel_time, max_days=max_days)

    pdf.add_page()

    pdf.cell(0, 10, 'Route Information', 0, 1, 'C')

    pdf.ln(10)

    pdf.add_route_table(routes)

    pdf.add_qr_code_page()

    pdf.output(pdf_path)

