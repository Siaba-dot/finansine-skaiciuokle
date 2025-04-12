import streamlit as st
import tempfile

# Funkcija sugeneruoti HTML turinį
def generate_html(pajamos, busto_isl, transporto_isl, maisto_isl, paskolos_isl, kitos_isl,
                  laisvi_pinigai, norimas_pirkinys, ar_gali_igyvendinti, sutaupoma_per_men, menesiu_reikia):
    
    html_content = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Jūsų finansinis skaičiavimas</title>
    </head>
    <body>
        <h1 style="text-align:center;">Ar galite sau leisti savo norą?</h1>
        <h2>1. Pajamos ir išlaidos:</h2>
        <ul>
            <li><strong>Mėnesinės pajamos:</strong> {pajamos:.2f} €</li>
            <li><strong>Būsto išlaidos:</strong> {busto_isl:.2f} €</li>
            <li><strong>Transporto išlaidos:</strong> {transporto_isl:.2f} €</li>
            <li><strong>Maisto išlaidos:</strong> {maisto_isl:.2f} €</li>
            <li><strong>Paskolų įmokos:</strong> {paskolos_isl:.2f} €</li>
            <li><strong>Kitos išlaidos:</strong> {kitos_isl:.2f} €</li>
        </ul>
        <p><strong>Laisvų pinigų po visų išlaidų:</strong> {laisvi_pinigai:.2f} € per mėnesį.</p>

        <h2>2. Norimas pirkinys:</h2>
        <p><strong>Prekės ar paslaugos kaina:</strong> {norimas_pirkinys:.2f} €</p>

        <h2>3. Rezultatas:</h2>
        <p><strong>{ar_gali_igyvendinti}</strong></p>

        <h2>4. Taupymo planas:</h2>
        <p><strong>Atidedama taupymui per mėnesį:</strong> {sutaupoma_per_men:.2f} €</p>
        <p><strong>Per kiek laiko susitaupysite:</strong> {menesiu_reikia:.2f} mėnesio (-ių)</p>

        <br><br>
        <p style="text-align:center; font-size:10px;">Sigita sprendimai | sigitasprendimai.lt</p>

        <br><br>
        <p style="font-size:12px; color:gray; text-align:center;">
        🛡️ Privatumo informacija: Ši skaičiuoklė nerenka ir nesaugo jokių asmens duomenų. 
        Visi įvesti duomenys lieka tik jūsų įrenginyje ir nėra perduodami trečiosioms šalims.
        </p>
    </body>
    </html>
    """
    return html_content

# Streamlit puslapis
st.set_page_config(page_title="Finansinė skaičiuoklė", page_icon="💰")
st.title("Ar galiu sau leisti šį norą? Ir per kiek laiko susitaupysiu? 💸")

# Įvedimo laukai
st.header("1. Įveskite savo finansinius duomenis:")

pajamos = st.number_input("Mėnesinės pajamos (€):", min_value=0.0, step=1.0)
busto_isl = st.number_input("Būsto išlaidos (nuoma, paskola, komunaliniai) (€):", min_value=0.0, step=1.0)
transporto_isl = st.number_input("Transporto išlaidos (kuras, bilietai) (€):", min_value=0.0, step=1.0)
maisto_isl = st.number_input("Maisto išlaidos (€):", min_value=0.0, step=1.0)
paskolos_isl = st.number_input("Paskolų įmokos (€):", min_value=0.0, step=1.0)
kitos_isl = st.number_input("Kitos išlaidos (€):", min_value=0.0, step=1.0)

st.header("2. Norimos prekės ar paslaugos kaina:")
norimas_pirkinys = st.number_input("Prekės/paslaugos kaina (€):", min_value=0.0, step=1.0)

st.header("3. (Pasirinktinai) Kiek galite taupyti kiekvieną mėnesį?")
sutaupoma_per_men = st.number_input("Atidedama taupymui kiekvieną mėnesį (€):", min_value=0.0, step=1.0)

if st.button("Skaičiuoti"):
    bendros_isl = busto_isl + transporto_isl + maisto_isl + paskolos_isl + kitos_isl
    laisvi_pinigai = pajamos - bendros_isl

    st.subheader("Rezultatai:")

    if laisvi_pinigai >= norimas_pirkinys:
        atsakymas = f"Puiku! Jūs galite įsigyti šią prekę/paslaugą iš karto. Laisvų pinigų lieka {laisvi_pinigai:.2f} € per mėnesį."
        st.success(atsakymas)
    else:
        atsakymas = f"Šiuo metu negalite įsigyti šios prekės/paslaugos. Laisvų pinigų per mėnesį lieka {laisvi_pinigai:.2f} €."
        st.warning(atsakymas)

    # Taupymo skaičiavimas
    if sutaupoma_per_men > 0:
        menesiu_reikia = norimas_pirkinys / sutaupoma_per_men
        st.info(f"Jei taupytumėte po {sutaupoma_per_men:.2f} € kas mėnesį, susitaupytumėte per {menesiu_reikia:.2f} mėnesio (-ių).")
    else:
        menesiu_reikia = 0
        st.info("Jei norite sužinoti, per kiek laiko susitaupytumėte, įveskite sumą, kurią galite taupyti kas mėnesį.")

    # Sugeneruoti HTML turinį
    html_content = generate_html(
        pajamos, busto_isl, transporto_isl, maisto_isl, paskolos_isl, kitos_isl,
        laisvi_pinigai, norimas_pirkinys, atsakymas, sutaupoma_per_men, menesiu_reikia
    )

    # Parsisiuntimo mygtukas
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
        tmpfile.write(html_content.encode('utf-8'))
        tmpfile.seek(0)
        st.download_button(label="Atsisiųsti rezultatą HTML formatu",
                           data=tmpfile.read(),
                           file_name="finansinis_skaiciavimas.html",
                           mime='text/html')

    st.caption("Skaičiavimus pateikė 'Sigita sprendimai' | sigitasprendimai.lt")
