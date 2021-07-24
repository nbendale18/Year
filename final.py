import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False
# DB Management
import sqlite3 
conn = sqlite3.connect('Project.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def user_view_doctor(city):
    c.execute('SELECT * FROM doctor WHERE City =?',(city,))
    data = c.fetchall()
    return data

def create_doctor():
    c.execute('CREATE TABLE IF NOT EXISTS doctor (Name TEXT,Address TEXT,City TEXT)')

def add_doctor(Name,Address,City):
    c.execute('INSERT INTO doctor VALUES (?,?,?)',(Name,Address,City))
    conn.commit()

def view_doctor():
    c.execute('SELECT * FROM doctor')
    data = c.fetchall()
    return data

def remove_doctor(Name):
    c.execute('DELETE FROM doctor WHERE Name =(?)',(Name,))
    conn.commit()

def main():
    """Simple Login App"""

    st.title("Cardiovascular Disease Predictor")

    menu = ["Entry Level Authentication","Login","SignUp","Admin Login"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Entry Level Authentication":
        st.subheader("No Beauty Shines Brighter Than A Healthy Heart")
        # import Image from pillow to open images
        from PIL import Image
        img = Image.open("streamlit.png")
        # display image using streamlit
        # width is used to set the width of an image
        st.image(img, width=700)
    elif choice == "Login":
        st.subheader("Login Section")
        st.markdown("Enter Username And Password")
        
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:

                st.success("Logged In as {}".format(username))

                task = st.selectbox("Task",["Heart Disease Analysis","Stress Level Analysis","Find The Cardiologist",'User Profiles'])
                if task == "Heart Disease Analysis":
                    st.subheader("Heart Disease Analysis")
                    st.write("""**1. Select Age :**""")
                    age = st.slider('', 0, 100, 25)
                    st.write("""**You selected this option **""",age)

                    st.write("""**2. Select Gender :**""")
                    sex = st.selectbox("(1=Male, 0=Female)",["1","0"])
                    st.write("""**You selected this option **""",sex)

                    st.write("""**3. Select Chest Pain Type :**""")
                    Chest_pain = st.selectbox("(1=Typical angina pain, 2=Atypical angina pain,3=Non-anginal pain,4=Asymptomatic )",["1","2","3","4"])
                    st.write("""**You selected this option **""",Chest_pain)

                    st.write("""**4. Select Resting Blood Pressure :**""")
                    Resting_blood_pressure = st.slider('', 0, 200, 110)
                    st.write("""**You selected this option **""",Resting_blood_pressure)

                    st.write("""**5. Select Serum Cholestrol :**""")
                    Cholestrol = st.slider('', 0, 600, 115)
                    st.write("""**You selected this option **""",Cholestrol)

                    st.write("""**6.Maximum Heart Rate Achieved(THALACH) :**""")
                    Thalach = st.slider('', 0, 220, 115)
                    st.write("""**You selected this option **""",Thalach)

                    st.write("""**7. Excercice Induced Angina(Pain in chest while excercise) :**""")
                    EIA = st.selectbox("(1=Yes, 0=No )",["0","1"])
                    st.write("""**You selected this option **""",EIA)

                    st.write("""**8.Oldpeak(ST induced by excercise relative to rest) :**""")
                    Oldpeak = st.slider('', 0.00, 10.00, 2.00)
                    st.write("""**You selected this option **""",Oldpeak)

                    st.write("""**9.Slope(The slope of peak exercise ST segment)) :**""")
                    Slope = st.selectbox("(Select 0,1,2)",["0","1","2"])
                    st.write("""**You selected this option **""",Slope)

                    st.write("""**10.CA (Number of blood vessels coloured in fluroscopy) :**""")
                    CA = st.selectbox("(Select 0,1,2,3 or 4 )",["0","1","2","3","4"])
                    st.write("""**You selected this option **""",CA)

                    st.write("""**11.THAL :**""")
                    Thal = st.slider('', 0.00, 10.00, 3.00)
                    st.write("""**You selected this option **""",Thal)
                    submit = st.button('Submit')
                    if submit:
                        df = [age,sex,Chest_pain,Resting_blood_pressure,Cholestrol,Thalach,EIA,Oldpeak,Slope,CA,Thal]
                        heart = pd.read_csv("data/dataset.csv")
                        X = heart.iloc[:,0:11].values
                        Y = heart.iloc[:,[11]].values
                        print(X.shape)
                        print(Y.shape)
                        model = RandomForestClassifier()
                        model.fit(X, Y.ravel() )
                        print(df)
                        prediction = model.predict([df])
                        st.subheader('Prediction :')
                        df1=pd.DataFrame(prediction,columns=['0'])
                        df1.loc[df1['0'] == 0, 'Chances of Heart Disease'] = 'No'
                        df1.loc[df1['0'] == 1, 'Chances of Heart Disease'] = 'Yes'
                        st.write(df1)
                        prediction_proba = model.predict_proba([df])
                        st.subheader('Prediction Probability in % :')
                        st.write(prediction_proba * 100)

                elif task == "Stress Level Analysis":
                    st.subheader("Stress Level Analysis")
                    st.write('0 - Does not apply. \n \n 1 - Sometimes. \n \n 2 - Good part of time. \n \n 4 - Most of the time. \n \n Answer according to the aforementioned scale.')
                    #Anxiety
                    a1 = st.slider('Dryness of Mouth', min_value = 0, max_value = 3, step = 1)
                    a2= st.slider('Difficulty in Breathing' , min_value = 0, max_value = 3, step = 1)
                    a3 = st.slider('Experiencing Trembling' ,min_value = 0, max_value = 3, step = 1)
                    a4 = st.slider('Worrying , panicking about making a fool of yourself' , min_value = 0, max_value = 3, step = 1)
                    a5 = st.slider('Close to Panic' , min_value = 0, max_value = 3, step = 1)
                    a6 = st.slider('Aware of the action of the heart in the absence of physical exertion ' , min_value = 0, max_value = 3, step = 1)
                    a7 = st.slider('Felt scared without any good reason' , min_value = 0, max_value = 3, step = 1)
                    a = a1 + a2 + a3 + a4 + a5 + a6 + a7
                    aa = a * 2
                    #Depression
                    d1 = st.slider('Couldn’t experience positive feeling ', min_value = 0, max_value = 3, step = 1)
                    d2 = st.slider('Difficulty in working up the initiative to do things ',min_value = 0, max_value = 3, step = 1)
                    d3 = st.slider('Nothing to look forward to ', min_value = 0, max_value = 3, step = 1)
                    d4 = st.slider('Felt down-hearted and blue ', min_value = 0, max_value = 3, step = 1)
                    d5 = st.slider('Not feeling enthusiastic ', min_value = 0, max_value = 3, step = 1)
                    d6 = st.slider('Felt wasn’t worth much as a person ', min_value = 0, max_value = 3, step = 1)
                    d7 = st.slider('Felt life was meaningless', min_value = 0, max_value = 3, step = 1)
                    d = d1 + d2 + d3 + d4 + d5 + d6 + d7
                    dd = d * 2
                    submit = st.button('Submit')
                    if submit:
                        if aa < 7:
                            st.write('You do not have anxiety.')
                        elif ((aa >= 8) and (aa <= 9)):
                            st.write('You have mild anxiety.')
                        elif  ((aa >= 10) and (aa <= 14)):
                            st.write('You have moderate anxiety.')
                        elif  ((aa >= 15) and (aa <= 19)):
                            st.write('You have mild anxiety.')
                        else :
                            st.write('You have extremely severe anxiety. Consult a specialist.')
                        if dd < 9:
                            st.write('You do not have depression.')
                        elif ((dd >= 10) and (dd <= 13)):
                            st.write('You have mild depression.')
                        elif  ((dd >= 14) and (dd <= 20)):
                            st.write('You have moderate depression.')
                        elif  ((dd >= 21) and (dd <= 27)):
                            st.write('You have mild depression.')
                        else :
                            st.write('You have extremely severe depression. Consult a specialist.')
    

                elif task == "Find The Cardiologist":
                    st.subheader("Find The Cardiologist")
                    User_city=st.text_input("Enter your city : " )
                    if st.button("Search"):
                        Doc_result=user_view_doctor(User_city)
                        clean_db1=pd.DataFrame(Doc_result,columns=["Name","Address","City"])
                        st.dataframe(clean_db1)

                
                elif task == "User Profiles":
                    st.subheader("User Profiles")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                    st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")


    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
    
    elif choice== "Admin Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            if username == 'Admin' and password == '12345':
                st.success("Logged In as {}".format(username))
                task1 = st.selectbox("Tasks",["Add Doctor","Remove Doctor","View Doctor","View Data"])
                if task1 == "Add Doctor":
                    st.subheader("Add Doctor")
                    DName=st.text_input("Enter the name : ")
                    DAdd=st.text_input("Enter the address : ")
                    DCity=st.text_input("Enter the city : ")

                    if st.button("Add"):
                        create_doctor()
                        add_doctor(DName,DAdd,DCity)
                        st.success("Doctor was added successfully")
                
                if task1 == "Remove Doctor":
                    name=st.text_input("Enter the name of doctor to be removed : ")
                    if st.button("Remove"):
                        remove_doctor(name)
                        st.success("Doctor was removed Sucessfully")
                
                if task1 == "View Doctor":
                    doc_result = view_doctor()
                    clean_db = pd.DataFrame(doc_result,columns=["Name","Address","City"])
                    st.dataframe(clean_db)

                if task1 == "View Data":
                    heart = pd.read_csv("data/dataset.csv")
                    df=pd.DataFrame(heart[:303],columns=['age','cp','trestbps','chol'])
                    st.line_chart(df)
                    st.set_option('deprecation.showPyplotGlobalUse', False)

            else:
                st.warning("Incorrect Username/Password")

if __name__ == '__main__':
    main()



