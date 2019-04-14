from flask import Flask, request, render_template, redirect
import cgi
import re

app=Flask(__name__)

app.config['DEBUG']=True


def validate(form_input):
    #check for presence of input
    form_value = form_input
    error = ''
    if not form_input:
        error = "Please enter the correct {name} !?"

    elif len(form_value) < 3 or len(form_value) > 20:  # check for length
        error = "I need something between (3-20) characters"

    elif " " in form_value:  # check for spaces
        error = "Enter {name} without spaces"
    return error
    
   


#routes to home screen showing form 
@app.route('/', methods=['POST','GET'])
def make_home():
    if request.method == 'POST':
        # variables to contain form inputs
        user_name = request.form['username']
        password = request.form['password']
        password_validate = request.form['password_validate']
        email = request.form['email']
        # #variables to contain error messages
        user_name_error=""
        password_error=""
        verify_pass_error=""
        compare_pass_error=""
        email_error=""
        # #checks for validation of username, password, and verify password
        user_name_error= validate(user_name).format(name="Username")
        password_error = validate(password).format(name="Password")
        verify_pass_error = validate(password_validate).format(name="Verify Password")
        
        # #compare password to verify password
        
        if password != password_validate:
            password_error="Passwords do not match!!"
            
        #check for email input
        if email:
            #check for @ and . symbols
            if not re.search(r"([a-z]+[@]+[a-z]+[.]+[a-z])", email):
                email_error="Please enter a real email address!"
            else:
                email_error = validate(email).format(
                    name="Email")  # complete email validation
        #checks for empty error messages. If the validation passed the welcome page will be generated 
        if not (user_name_error or
                password_error or
                verify_pass_error or 
                compare_pass_error or
                email_error
            ):
            return redirect('welcome?user_name={0}'.format(user_name))
        return render_template('signup-page.html',
                               username_error=user_name_error,
                               password_error=password_error,
                               verify_pass_error=verify_pass_error,
                               compare_pass_error=compare_pass_error,
                               email_error=email_error,
                                user_name=user_name,
                            )    
    return render_template('signup-page.html', title="User Sign Up Page")

@app.route('/welcome')
def welcome_user():
    user_name=request.args.get('user_name')
    return render_template('welcome.html', user_name=user_name)

app.run()