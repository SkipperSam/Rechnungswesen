from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import date
import os

def create_invoice_pdf(data, rechnungsnummer):
    outdir = "Rechnungen"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    pdfname = f"{outdir}/Rechnung_{rechnungsnummer}.pdf"
    c = canvas.Canvas(pdfname, pagesize=A4)
    width, height = A4

    # --- LOGO einfügen (größer, rechts, höher) ---
    logo_path = os.path.join(os.path.dirname(__file__), "Logo.png")
    if os.path.exists(logo_path):
        LOGO_WIDTH = 180
        LOGO_HEIGHT = 90
        x_logo = width - 50 - LOGO_WIDTH
        y_logo = height - 40 - LOGO_HEIGHT  # 10pt höher als bisher
        c.drawImage(logo_path, x_logo, y_logo, width=LOGO_WIDTH, height=LOGO_HEIGHT, mask='auto')

    # --- Empfängeradresse (Kunde) ---
    y_empfaenger = height - 141

    # Absender klein, eine Zeile, unmittelbar über dem Empfänger
    absender = "Porta Podologie Andrea Hellermann, Zur Schalksmühle 17, 32457 Porta Westfalica"
    c.setFont("Helvetica", 8)
    c.drawString(50, y_empfaenger + 14, absender)

    # Empfängeradresse (Kunde)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y_empfaenger, data['kunde_name'])
    c.setFont("Helvetica", 11)
    c.drawString(50, y_empfaenger - 15, data['kunde_strasse'])
    c.drawString(50, y_empfaenger - 30, data['kunde_plzort'])

    # --- Kopfbereich (großer Abstand zur Überschrift "Rechnung") ---
    y = y_empfaenger - 80  # Großer Abstand

    # "Rechnung" linksbündig
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, y, "Rechnung")

    # Rechnungsnummer und Datum in einer Zeile (Datum rechts)
    c.setFont("Helvetica", 12)
    c.drawString(50, y - 35, f"Rechnungsnummer: {rechnungsnummer}")
    c.drawRightString(width - 50, y - 35, f"Datum: {date.today().strftime('%d.%m.%Y')}")

    # IK unter das Datum
    c.setFont("Helvetica", 11)
    c.drawRightString(width - 50, y - 50, "IK: 390509925")

    # "Leistungsempfänger" und "Privatrezept" fett auf gleicher Höhe unter Rechnungsnummer/Datum/IK
    y_le = y - 78
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_le, "Leistungsempfänger")
    if data.get("privatrezept"):
        info_x_right = width - 50
        c.drawRightString(info_x_right, y_le, "Privatrezept")

    # Kundendaten leicht eingerückt unter Leistungsempfänger
    y_kunde = y_le - 18
    x_kunde = 70
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_kunde, y_kunde, data['kunde_name'])
    c.setFont("Helvetica", 11)
    c.drawString(x_kunde, y_kunde - 15, data['kunde_strasse'])
    c.drawString(x_kunde, y_kunde - 30, data['kunde_plzort'])

    # Privatrezept-Infos (Verordnungsdatum, Diagnose) unter der Privatrezept-Überschrift, rechtsbündig
    if data.get("privatrezept"):
        y_privatrezept = y_le - 18
        info_x_right = width - 50
        c.setFont("Helvetica", 11)
        c.drawRightString(info_x_right, y_privatrezept, f"Verordnungsdatum: {data.get('verordnungsdatum', '')}")
        y_privatrezept -= 15
        c.drawRightString(info_x_right, y_privatrezept, f"Diagnose: {data.get('diagnose', '')}")

    # Weiter mit Artikelliste: Abstand weniger stark, damit Text & Leistungen höher rücken
    y = y_kunde - 60  # Abstand reduziert (statt -90), damit alles höher rückt

    # Umsatzsteuerbefreiungstext über den Leistungen
    c.setFont("Helvetica", 11)
    c.drawString(50, y, "Die abgerechneten Leistungen sind gemäß § 4 Nr. 14 UStG umsatzsteuerbefreit.")
    y -= 28

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Leistungen:")
    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(60, y, "Name")
    c.drawString(200, y, "Datum")
    c.drawString(290, y, "Anzahl")
    c.drawString(340, y, "Einzelpreis")
    c.drawString(420, y, "MwSt")
    c.drawString(470, y, "Gesamt")
    y -= 10
    c.line(50, y, width - 50, y)
    y -= 12
    c.setFont("Helvetica", 11)
    summe = 0
    mwst_sum = 0

    for a in data.get("artikel_liste", []):
        preis = a["preis"]
        mwst = a["mwst"]
        leistungsdaten = a.get("leistungsdaten", [])
        if not leistungsdaten and a.get("leistungsdatum"):
            leistungsdaten = [a["leistungsdatum"]]
        for leistungsdatum in leistungsdaten:
            gesamt = preis
            mwst_betrag = gesamt * mwst / 100
            summe += gesamt
            mwst_sum += mwst_betrag
            c.drawString(60, y, f"{a['name'][:18]:18}")
            c.drawString(200, y, f"{leistungsdatum[:10]}")
            c.drawRightString(325, y, "1")
            c.drawRightString(400, y, f"{preis:7.2f} €")
            c.drawRightString(450, y, f"{mwst:4.1f}%")
            c.drawRightString(530, y, f"{gesamt:8.2f} €")
            y -= 15
            if y < 120:
                c.showPage()
                y = height - 100

    y -= 5
    c.line(50, y, width - 50, y)
    y -= 15

    # Gesamtsumme und MwSt
    c.setFont("Helvetica-Bold", 11)
    c.drawString(340, y, f"Zwischensumme:")
    c.drawRightString(530, y, f"{summe:.2f} €")
    y -= 15
    c.setFont("Helvetica", 11)
    c.drawString(340, y, f"enthaltene MwSt:")
    c.drawRightString(530, y, f"{mwst_sum:.2f} €")
    y -= 15
    y_gesamtsumme = y
    c.setFont("Helvetica-Bold", 12)
    c.drawString(340, y_gesamtsumme, f"Gesamtsumme:")
    c.drawRightString(530, y_gesamtsumme, f"{summe:.2f} €")

    # Zahlungsstatus auf gleicher Höhe wie Gesamtsumme
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_gesamtsumme, "Zahlung:")

    y = y_gesamtsumme - 20
    c.setFont("Helvetica", 11)
    if data.get("bezahlt"):
        c.drawString(80, y, "Zahlung dankend erhalten.")
    else:
        c.drawString(80, y, "Bitte innerhalb von 10 Tagen auf das unten angegebene Konto überweisen.")

    # --------- Fußzeile ---------
    # Höhe der Fußzeile (ca. 32mm vom unteren Rand)
    footer_y = 15 * mm

    # Linksbündig
    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, footer_y + 16, "Andrea Hellermann Porta Podologie")
    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, footer_y + 6, "Zur Schalksmühle 17")
    c.drawString(20 * mm, footer_y - 4, "32457 Porta Westfalica")

    # Zentriert
    center_x = width / 2
    c.setFont("Helvetica", 10)
    c.drawCentredString(center_x, footer_y + 16, "Tel.: 0571 9719350")
    c.drawCentredString(center_x, footer_y + 6, "info@porta-podologie.de")
    c.drawCentredString(center_x, footer_y - 4, "www.porta-podologie")

    # Rechtsbündig
    right_x = width - 20 * mm
    c.setFont("Helvetica", 10)
    c.drawRightString(right_x, footer_y + 16, "Andrea Hellermann")
    c.setFont("Helvetica", 10)
    c.drawRightString(right_x, footer_y + 6, "Commerzbank Minden")
    c.drawRightString(right_x, footer_y - 4, "DE06 4904 0043 0312 3023 00")
    c.drawRightString(right_x, footer_y - 14, "COBADEFFXXX")

    # Zentriert darunter: Seitenzahl und Dokumentenbezeichnung
    c.setFont("Helvetica", 9)
    page_info = f"Seite 1 von 1"
    c.drawCentredString(center_x, footer_y - 22, f"{page_info}")

    c.showPage()
    c.save()
    return pdfname