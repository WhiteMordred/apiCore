from flask_mail import Mail, Message 
from flask import Flask, render_template, current_app
import os
from jinja2 import Template
from dotenv import load_dotenv
load_dotenv(".env.mail")


def mailconfig(app):
    return Mail(app)

def cssloader():
    css_paths = [
        os.path.join(current_app.root_path, 'templates', 'components', 'css', 'vendor.min.css'),
        os.path.join(current_app.root_path, 'templates', 'components', 'css', 'site.css'),
        os.path.join(current_app.root_path, 'templates', 'components', 'css', 'app.min.css')
    ]
    css_content = ""
    for path in css_paths:
        try:
            with open(path, 'r') as css_file:
                css_content += css_file.read() + "\n"
        except Exception as e:
            print(f"Failed to load CSS file {path}: {e}")
    return css_content

def jsloader():
    js_paths = [
        os.path.join(current_app.root_path, 'templates', 'components', 'js','vendor.min.js'),
        os.path.join(current_app.root_path, 'templates', 'components', 'js','site.js'),
        os.path.join(current_app.root_path, 'templates', 'components', 'js', 'app.min.js')
    ]
    js_content = ""
    for path in js_paths:
        try:
            with open(path, 'r') as js_file:
                js_content += js_file.read() + "\n"
        except Exception as e:
            print(f"Failed to load JS file {path}: {e}")
    return js_content

def registrationMailOrganization(registration):
    try:
        css_content = cssloader()
        js_content = jsloader()
        html_body = render_template('register_mail.jinja',
                                    frontend_url=registration['frontend_url'], 
                                    url=registration['verification_url'],
                                    organization_id=registration['organization_id'],
                                    organization_name=registration['organization_name'],
                                    css_content=css_content, js_content=js_content)
        msg = Message('Organization Verification Email',
                      sender=current_app.config["MAIL_USERNAME"],
                      recipients=[registration['email']],
                      html=html_body)
        mail = current_app.extensions.get('mail')
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

def registrationMailUser(registration):
    try:
        css_content = cssloader()
        js_content = jsloader()
        html_body = render_template('register_user_mail.jinja', 
                                    url=registration['verification_url'],
                                    username=registration['username'],
                                    css_content=css_content, js_content=js_content)
        msg = Message('User Verification Email',
                      sender=current_app.config["MAIL_USERNAME"],
                      recipients=[registration['email']],
                      html=html_body)
        mail = current_app.extensions.get('mail')
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

def verificationMail(verification):
    try:
        html_body = render_template('verification_mail.jinja', 
                                    url=verification['verification_url'],
                                    organization_id=verification['organization_id'],
                                    organization_name=verification['organization_name'],
                                    username=verification['username'])
        msg = Message('Verification Email',
                      sender=current_app.config["MAIL_USERNAME"],
                      recipients=[verification['email']],
                      html=html_body)
        mail = current_app.extensions.get('mail')
        mail.send(msg)
        print("Email sent to: " + verification['email'])
    except Exception as e:
        print(f"Failed to send email: {e}")
