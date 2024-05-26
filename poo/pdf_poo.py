import os
import qrcode
from fpdf import FPDF
import tempfile


class PDF(FPDF):
    def __init__(self, company_name, starting_port, destination_port, ship_name, forced_port_stops=None,
                 **extra_fields):
        super().__init__()
        self.company_name = company_name
        self.starting_port = starting_port
        self.destination_port = destination_port
        self.ship_name = ship_name
        self.forced_port_stops = forced_port_stops or []
        self.extra_fields = extra_fields
        self.qr_code_image_path = self.generate_qr_code()
        self.is_qr_code_page = False

    def generate_qr_code(self):
        """
        Generates a QR code containing the shipping information and saves it as an image file.
        Returns the path to the QR code image.
        """
        qr_info = (
            f"Company: {self.company_name}\n"
            f"Starting Port: {self.starting_port}\n"
            f"Destination Port: {self.destination_port}\n"
            f"Ship: {self.ship_name}\n"
            f"Forced Port Stops: {', '.join(self.forced_port_stops)}\n"
        )
        for key, value in self.extra_fields.items():
            qr_info += f"{key.replace('_', ' ').title()}: {value}\n"

        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(qr_info)
        qr.make(fit=True)

        qr_image = qr.make_image(fill='black', back_color='white')
        qr_image_path = tempfile.mktemp(suffix='.png')
        qr_image.save(qr_image_path)

        return qr_image_path

    def header(self):
        if self.is_qr_code_page:
            return
        # Arial bold 12
        self.set_font('Arial', 'B', 12)

        # Titles of columns
        self.cell(0, 10, f'{self.company_name}', 0, 1, 'C')
        self.cell(0, 10, f'Starting Port: {self.starting_port}', 0, 1, 'L')
        self.cell(0, 10, f'Destination Port: {self.destination_port}', 0, 1, 'L')
        self.cell(0, 10, f'Ship: {self.ship_name}', 0, 1, 'L')

        if self.forced_port_stops:
            forced_stops_str = ', '.join(self.forced_port_stops)
            self.cell(0, 10, f'Forced Port Stops: {forced_stops_str}', 0, 1, 'L')

        for key, value in self.extra_fields.items():
            self.cell(0, 10, f'{key.replace("_", " ").title()}: {value}', 0, 1, 'L')

        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'logo3.png')

        self.add_image(image_path, 160, 5, 40, 40)

        # Line break
        self.ln(10)

    def footer(self):
        if self.is_qr_code_page:
            return
        self.set_y(-30)

    def chapter_title(self, title):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Title
        self.cell(0, 10, title, 0, 1, 'L')
        # Line break
        self.ln(4)

    def add_image(self, image_path, x=10, y=10, w=0, h=0):
        if os.path.exists(image_path):
            self.image(image_path, x, y, w, h)
        else:
            print(f"Error: The file {image_path} does not exist.")

    def chapter_body(self, body):
        # Read text file
        self.set_font('Arial', '', 12)
        # Output text
        self.multi_cell(0, 10, body)
        # Line break
        self.ln()

    def add_route_table(self, routes):
        # Set font
        self.set_font('Arial', 'B', 12)
        # Route and Time headers
        self.cell(145, 10, 'Route', 1, 0, 'C')
        self.cell(45, 10, 'Days', 1, 1, 'C')
        self.set_font('Arial', '', 12)

        for route, days in routes:
            route_str = ' -> '.join(route)
            # Calculate the height of the cell for the route
            line_count = len(route_str) // 145 + 1
            cell_height = 10 * line_count

            # Output the route and days
            self.multi_cell(145, cell_height, route_str, border=1)
            self.set_y(self.get_y() - cell_height)
            self.set_x(155)

            self.cell(45, cell_height, str(days), border=1, align='C', ln=1)

        # Reset text color to black for any further content
        self.set_text_color(0, 0, 0)

    def add_qr_code_page(self):
        """
        Adds a separate page for the QR code.
        """
        self.is_qr_code_page = True
        self.add_page()
        self.set_y(10)  # Set a margin from the top
        self.add_image(self.qr_code_image_path, x=10, y=10, w=50, h=50)  # Adjust position and size
        self.is_qr_code_page = False
