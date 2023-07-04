from library import *

background = """
    <style>
    [data-testid="stAppViewContainer"]{
        
    }

    [data-testid="stHeader"]{
        background-color: rgb(0,0,0);
        opacity:0.0;
    }

    [data-testid="stToolbar"]{
        opacity:1;
    }

    [class="css-cio0dv egzxvld1"]{
        opacity:0.0;
    }

    [class="css-5uatcg edgvbvh5"]{
        align-items: center;
        justify-content: center;
        background-color: green;
    }

    [class="css-1dj0hjr e1fqkh3o5"]{
        font-size: 20px;
        text-transform: capitalize;
    }

    [class="css-lrlib e1fqkh3o9"]{
    
        text-transform: capitalize;
    }
    

    </style>
    """

def clear_background(prompt:str=background):
    st.markdown(prompt, unsafe_allow_html=True)
    

def make_footer():
    st.markdown(f"<p style='position:fixed;left:270px;bottom:0px;width:100%;background-color:transparent;color:white;text-align:left;z-index:99;padding:0px'>Developed with ❤ by Kelompok 2</p>",unsafe_allow_html=True)
    

def center_image(classname:str|None = None):
    css = """{
        justify-content: center;
        align-items: center;
        align-content: center;
    }
    """

    image = f"""
    <style>
    [class="{classname}"]{css}

    </style>
    """

    st.markdown(image, unsafe_allow_html=True)