from tools.encryption_util.encryption import EncryptionUtil
from dotenv import load_dotenv
import os

#-------------------------------------------------------------------#
# Default loader variables environment 
# For change the default env go to root directory and change .env file
#-------------------------------------------------------------------#
def load_env(app):
    load_dotenv()
    # Stage Mode 
    app.config['STAGE'] = os.environ['STAGE']

    # MongoDB Configuration
    app.config['MONGO_INITDB_ROOT_USERNAME'] = os.environ["MONGO_INITDB_ROOT_USERNAME"]
    app.config['MONGO_INITDB_ROOT_PASSWORD'] = os.environ["MONGO_INITDB_ROOT_PASSWORD"]
    app.config['MONGO_DB_HOST']= os.environ["MONGO_DB_HOST"]
    app.config['MONGO_DB_PORT']= os.environ["MONGO_DB_PORT"]

    # Json Config 
    app.config['JSON_AS_ASCII'] = False

    # Mail Configuration
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 465))
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

    # Frontend Configuration
    app.config['FRONTEND_URL'] = os.environ.get('FRONTEND_URL')

    # Security Configuration
    if (os.environ.get('RECOVERYKEY') == 'False'):
        app.config['SECURITYKEY'] = EncryptionUtil.generate_encryption_key()
    else:
        app.config['SECURITYKEY'] = os.environ.get('SECURITYKEY')

    if (os.environ.get('FIRSTBOOT') == 'True'):
        EncryptionUtil.grf("./","recovery.key")

    # Security Flask
    app.config['SECRETKEY'] = os.environ.get('SECRETKEY')

    # Organization Configuration
    app.config['ORGANIZATION_MODE'] = os.environ.get('ORGANIZATION_MODE')
    app.config['ORGANIZATION_DB'] = os.environ.get('ORGANIZATION_DB')
    app.config['ORGANIZATION_NAME'] = os.environ.get('ORGANIZATION_NAME')
    app.config['ORGANIZATION_ADDRESS'] = os.environ.get('ORGANIZATION_ADDRESS')
    app.config['ORGANIZATION_CITY'] = os.environ.get('ORGANIZATION_CITY')
    app.config['ORGANIZATION_ZIPCODE'] = os.environ.get('ORGANIZATION_ZIPCODE')
    app.config['ORGANIZATION_COUNTRY'] = os.environ.get('ORGANIZATION_COUNTRY')
    app.config['ORGANIZATION_PHONE'] = os.environ.get('ORGANIZATION_PHONE')
    app.config['ORGANIZATION_EMAIL'] = os.environ.get('ORGANIZATION_EMAIL')



