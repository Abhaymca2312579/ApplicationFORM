from flask import Flask, render_template, request, redirect, flash, session
from pymongo import MongoClient

app = Flask(__name__)

# ✅ Use a secure secret key for flash messages
app.secret_key = "supersecretkey123"  # Change this to something secure

# ✅ Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://abhay:Abhaysingh%40123@abhaycluster.9ptuz.mongodb.net/JobApplications?retryWrites=true&w=majority")
db = client["JobApplications"]
collection = db["applications"]

@app.route("/", methods=["GET", "POST"])
def google_form():
    if request.method == "POST":
        data = {
            "name": request.form.get("name", ""),
            "email": request.form.get("email", ""),
            "phone": request.form.get("phone", ""),
            "date_of_apply": request.form.get("date_of_apply", ""),
            "profile": request.form.get("profile", ""),
            "company_name": request.form.get("company_name", ""),
            "mode": request.form.get("mode", ""),
            "referral": request.form.get("referral", "No"),
            "referral_id": request.form.get("referral_id") if request.form.get("referral") == "Yes" else None
        }
        
        # ✅ Insert data into MongoDB
        collection.insert_one(data)

        # ✅ Flash success message
        flash("✅ Application submitted successfully!", "success")

        # ✅ Redirect to home page
        return redirect("/")
    
    return render_template("form.html")

# ✅ Route to View Data
@app.route("/data")
def view_data():
    documents = list(collection.find())
    return render_template("data.html", documents=documents)

if __name__ == "__main__":
    app.run(debug=True)
