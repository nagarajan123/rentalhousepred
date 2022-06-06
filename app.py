
# importing the necessary dependencies
from flask import Flask, render_template, request
from flask_cors import cross_origin
import pickle
import numpy as np
import sklearn

app = Flask(__name__) # initializing a flask app
# app=application
@app.route('/')  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def rent_predict():
    if request.method == 'POST':
      
        try:
            #  reading the inputs given by the user
            area=float(request.form['area'])
            furnishing = str(request.form['furnishing'])
            if(furnishing=="Unfurnished"):
                furnishing=0
            elif(furnishing=="Semifurnished"):
                furnishing=1
            else:
                furnishing=2
            floor_number = int(request.form['floor_number'])
            floor_type = str(request.form['floor_type'])
            if(floor_type=="vitrified"):
                floor_type=1
            elif(floor_type=="ceramic"):
                floor_type=2
            elif(floor_type=="granite"):
                floor_type=3

            gate_community = str(request.form["gate_community"])
            if(gate_community=='Yes'):
                gate_community=1
            else:
                gate_community=0

            corner_pro = str(request.form["corner_pro"])
            if(corner_pro=='Yes'):
                corner_pro=1
            else:
                corner_pro=0
            parking = int(request.form['parking'])

            wheelchairadption = str(request.form["wheelchairadption"])
            if(wheelchairadption=='No'):
                wheelchairadption=0
            else:
                wheelchairadption=1

            petfacility = str(request.form["petfacility"])
            if(petfacility=='No'):
                petfacility=0
            else:
                petfacility=1

            aggDur = int(request.form["aggDur"])
            noticeDur = int(request.form["noticeDur"])
            lightbill = int(request.form["lightbill"])
            powerbackup = str(request.form["powerbackup"])
            if(powerbackup=='No'):
                powerbackup=0
            else:
                powerbackup=1
            propertyage = str(request.form["propertyage"])
            if(propertyage=="1 to 5 Year Old"):
                propertyage=1
            elif(propertyage=="5 to 10 Year Old"):
                propertyage=2
            elif(propertyage=="10+ Year Old"):
                propertyage=3
            others = int(request.form['others'])
            #parking = int(request.form['parking'])
            maintenance_amt = int(request.form['maintenance_amt'])
            brok_amt = int(request.form['brok_amt'])
            brok_amt2 = np.log(brok_amt)
            deposit_amt = int(request.form['deposit_amt'])
            deposit_amt2 = np.log(deposit_amt)
            total_rooms = int(request.form['total_rooms'])
            location_encoded = str(request.form['location_encoded'])
            if(location_encoded=="Adinath Colony"):
                location_encoded =11000
            if(location_encoded=="Akurdi"):
                location_encoded =17522.22
            if(location_encoded=="Alandi"):
                location_encoded =7750
            if(location_encoded=="Alandi Road"):
                location_encoded =9500
            if(location_encoded=="Amanora Victory Tower"):
                location_encoded =17500
            if(location_encoded=="Ambedkar Nagar"):
                location_encoded =18500
            mnt_amt_encoded= 0.791255
            avalable_for_encoded = str(request.form['avalable_for_encoded'])
            if avalable_for_encoded=="All":
                avalable_for_encoded =1
            elif avalable_for_encoded=="Family":
                avalable_for_encoded=2
            elif avalable_for_encoded=="Bachelors(Men)":
                avalable_for_encoded=3
            elif avalable_for_encoded=="Bachelors(Women)":
                avalable_for_encoded=4
            
            filename = 'rent_rf_grid_regressor_model.pkl'
            loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            print("*******")
            # predictions using the loaded model file
            prediction=loaded_model.predict([[area,furnishing,floor_number,floor_type,gate_community,corner_pro,wheelchairadption,petfacility,aggDur,noticeDur,
                lightbill,powerbackup,propertyage,others,maintenance_amt,brok_amt,deposit_amt2,total_rooms,location_encoded,mnt_amt_encoded,avalable_for_encoded]])
            print('prediction is', prediction)
            # showing the prediction results in a UI
            return render_template('results.html',prediction=round(prediction[0]))
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
       
    else:
        return render_template('index.html')



if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app