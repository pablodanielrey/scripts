

import owncloud
import sys
import logging

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    user = sys.argv[1]
    password = sys.argv[2]
    dni = sys.argv[3]
    initPass = sys.argv[4]

    oc = owncloud.Client('https://owncloud.econo.unlp.edu.ar', verify_certs=False, debug=True)
    try:
        oc.login(user, password)
        try:
            if oc.user_exists(dni):
                oc.set_user_attribute(dni, 'password', initPass)
            else:
                oc.create_user(dni, initPass)

        finally:
            oc.logout()

    except Exception as e:
        logging.exception(e)
