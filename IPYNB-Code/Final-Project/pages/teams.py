from library import *
import UI

if __name__ == "__main__":
    UI.clear_background()
    UI.make_footer()

    with open(f'{PATH}/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.markdown('<h1 style="text-align: center; color: white;">Meet Our Teams</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: white;">Kelompok 2</h2>', unsafe_allow_html=True)

    pande_bytes = Path(IMGDIR / 'pande.jpg').read_bytes() #Membaca file gambar
    encoded_pande = base64.b64encode(pande_bytes).decode() #Mengencode file gambar

    dimas_bytes = Path(IMGDIR / 'dimas.jpg').read_bytes() #Membaca file gambar
    encoded_dimas = base64.b64encode(dimas_bytes).decode() #Mengencode file gambar

    wahyu_bytes = Path(IMGDIR / 'wahyu.jpg').read_bytes() #Membaca file gambar
    encoded_wahyu = base64.b64encode(wahyu_bytes).decode() #Mengencode file gambar

    st.markdown(f"""
<div class="row">
    <div class="column">
        <img src="data:image/jpg;base64,{encoded_dimas}" alt="Dimas" style="width:100%;border-radius:15px">
        <h3 style='text-align: center; color: white; font-weight:10; font-size:15px; opacity:0.7'>I Wayan Dimas Wirahadi Saputra <br> NIM. 2108561112</h3>
    </div>
    <div class="column">
        <img src="data:image/jpg;base64,{encoded_pande}" alt="Pande Dani" style="width:100%;border-radius:15px">
        <h3 style='text-align: center; color: white; font-weight:10; font-size:15px; opacity:0.7'>Pande Gede Dani Wismagatha <br> NIM. 2108561022</h3>
    </div>
    <div class="column">
        <img src="data:image/jpg;base64,{encoded_wahyu}" alt="Wahyu" style="width:100%; border-radius:15px">
        <h3 style='text-align: center; color: white; font-weight:10; font-size:15px; opacity:0.7'>I Gede Ngurah Wahyu Ananta <br>
        NIM. 2108561102</h3>
    </div>
</div>""", unsafe_allow_html=True)
