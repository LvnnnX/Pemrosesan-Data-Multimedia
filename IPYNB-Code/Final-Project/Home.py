from library import *
import dataholder as dh
import process as prc
import UI

if __name__== '__main__':
    UI.clear_background()
    UI.make_footer()

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: white;'>Program Audio Sentimen Analysis</h1>", unsafe_allow_html=True) #Judul Program
  
    with st.form(key='my_form', clear_on_submit=True):
        files = st.file_uploader("Upload your audio file", type=['wav', 'mp3'], accept_multiple_files=True)
        submitted = st.form_submit_button('Submit')

        if not files and submitted:
            st.error('Please upload your audio file')

        elif files and submitted:
            st.success('Upload success!')
            for file in files:
                name = dh.save_file(file)
                # st.write(f'File {file.name} berhasil diupload')
                predictions = prc.get_prediction(audio_name=file.name, path=TMPDIR)
                
                fix_prediction = np.argmax(predictions)

                result = 'Happy' if fix_prediction == 1 else 'Sad'
                color = 'green' if fix_prediction == 1 else 'red'
                st.markdown(f'<h2 style="text-align: center; color: white;">{file.name} is <font style="color:{color};">{round(max(predictions[0])*100,2)}% {result}</font></h2>', unsafe_allow_html=True)
                st.audio(file)
                # st.write(f'{(predictions)}') 
                # st.dataframe(df) 

                df = pd.DataFrame(predictions[0], columns=['Score'])
                df.index = ['Sad','Happy']

                st.bar_chart(data=df, x=['Sad','Happy'], height=300, width=300, use_container_width=True)
                
                # fig, ax = plt.subplots(figsize=(5,5))
                # ax = plt.pie(df.Score, labels=['Sad','Happy'], autopct='%1.1f%%', startangle=90)
                # ax = plt.title(f'Prediction {file.name}', fontsize=16)

                # st.pyplot(fig)
        dh.delfile(TMPDIR)
    